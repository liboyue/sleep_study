import numpy as np
import os
import argparse

# import mne
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.distributed as dist
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import glog as log

import sleep_study as ss

torch.manual_seed(1)

def my_log(*a, **kw):
    if args.rank == 0:
        log.info(*a, **kw)
    else:
        log.debug(*a, **kw)


class EEG_dataset(Dataset):

    def __init__(self, root_dir, gpu=False, transform=None):

        root_dir = os.path.expanduser(root_dir)
        root_dir = os.path.abspath(root_dir)

        self.root_dir = root_dir
        self.file_list = os.listdir(self.root_dir)

        self.transform = transform

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):

        path = self.root_dir + '/' + self.file_list[idx]
        tmp = np.load(path)
        data, labels = torch.from_numpy(tmp['data']).float(), torch.from_numpy(tmp['labels']).long()
        log.debug(str(data.shape) + ', ' + str(labels.shape) + ', ' + str(idx) + ', ' + path)
        return data, labels


class Net(nn.Module):

    def __init__(self, n_hidden, sfreq, n_channels):

        super().__init__()

        self.conv = nn.Conv1d(n_channels, 3, 64, 16, 16)
        self.lstm = nn.LSTM(1437, n_hidden)
        self.fc = nn.Linear(n_hidden, len(ss.info.EVENT_DICT))

    def forward(self, data):

        out = self.conv(data)
        out = out.view((len(out), 1, -1))
        out = F.relu(out)

        out, _ = self.lstm(out)
        out = out.view((len(out), -1))

        out = self.fc(out)
        out = F.log_softmax(out, dim=1)

        return out


def predict(output, labels):
    pred = output.argmax(axis=1)
    return pred.eq(labels.data.view_as(pred)).cpu().tolist()

def my_collate(batch):
    data = [item[0] for item in batch]
    target = [item[1] for item in batch]
    return [data, target]


parser = argparse.ArgumentParser()
# Training args
parser.add_argument('--epochs',                 default=1,          type=int,                                       help='Number of epochs'                       )
parser.add_argument('--batch_size',             default=1,          type=int,                                       help='Batch size per worker'                  )
parser.add_argument('--lr',                     default=1e-3,       type=float,                                     help='Learning rate'                          )
parser.add_argument('--momentum',               default=0.9,        type=float,                                     help='Momentum'                               )
parser.add_argument('--weight_decay',           default=0,          type=float,                                     help='Weight decay'                           )
parser.add_argument('--num_workers',            default=0,          type=int,                                       help='Number of workers for data loader'      )
parser.add_argument('--disp_interval',          default=10,         type=int,                                       help='Print every number of batches'          )

# Distributed args
parser.add_argument('--backend',                default='nccl',     type=str,   choices=['nccl', 'gloo', 'mpi'],    help='Distributed backend'                    )
parser.add_argument('--cpu',                    default=False,      action='store_true',                            help='Use CPU'                                )
parser.add_argument('--deterministic',          default=False,      action='store_true',                            help='Use fixed random seed'                  )
parser.add_argument('--debug',                  default=False,      action='store_true',                            help='Debug mode'                             )
parser.add_argument('-v','--verbosity',         default='INFO',     type=str,   choices=['DEBUG', 'INFO', 'WARN'],  help='Verbosity of log'                       )

args = parser.parse_args()

# Load options from envs
for name in ['MASTER_ADDR', 'MASTER_PORT']:
    setattr(args, name.lower(), os.environ[name])

for name in ['RANK', 'WORLD_SIZE', 'LOCAL_RANK', 'WORLD_LOCAL_SIZE', 'WORLD_NODE_RANK']:
    setattr(args, name.lower(), int(os.environ[name]))

args.node_rank = args.world_node_rank

log.setLevel(args.verbosity)
my_log(args)
ss.init()

if not args.cpu:
    torch.cuda.set_device(args.local_rank)
    torch.backends.cudnn.benchmark = True

if args.deterministic:
    torch.manual_seed(args.rank)
    np.random.seed(args.rank)
    torch.backends.cudnn.deterministic = True
    torch.cuda.manual_seed(args.rank)

dist.init_process_group(backend=args.backend)


n_channels = 6
criterion = nn.NLLLoss()

model = Net(128, 256, n_channels)

if not args.cpu:
    model = model.cuda()

if args.cpu:
    model = torch.nn.parallel.DistributedDataParallel(model)
else:
    model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[args.rank])


optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum)

dataset = EEG_dataset('~/preprocessed')

sampler = torch.utils.data.distributed \
            .DistributedSampler(dataset, rank=args.rank,
                                num_replicas=args.world_size,
                                shuffle=True)

loader = DataLoader(dataset, batch_size=args.batch_size, sampler=sampler, 
                    collate_fn=my_collate, num_workers=args.num_workers)
                    # shuffle=True, pin_memory=True, num_workers=args.num_workers)


for epoch in range(args.epochs):
    running_acc = []
    running_loss = []

    for i, (data_batch, labels_batch) in enumerate(loader):

        loss_batch = 0
        pred = []

        for data, labels in zip(data_batch, labels_batch):

            if not args.cpu:
                data = data.cuda()
                labels = labels.cuda()

            optimizer.zero_grad()
            output = model(data)

            loss = criterion(output, labels) / args.batch_size
            loss.backward()

            loss_batch += loss
            pred += predict(output, labels)

        optimizer.step()

        running_acc += pred
        running_loss.append(loss_batch.item())

        if (i + 1) % args.disp_interval == 0:
            my_log('Rank %d, epoch %d, batch %d, running acc: %.2f, running loss: %.6f', args.rank, epoch + 1, i + 1, np.mean(running_acc), np.mean(running_loss))
            running_acc = []
            running_loss = []


    my_log('Rank %d, epoch %d finished, running acc: %.2f' % (args.rank, (epoch + 1), np.mean(running_acc)))

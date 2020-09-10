import os
import pandas as pd
from time import time

import sleep_study as ss

# rsync -av -e "ssh -A boyuel@linux.ece.cmu.edu ssh" ./sleep_study boyuel@mead.ece.local.cmu.edu:~/sleep_study_utils

def create_dataset(output_dir='~/sleep_study_dataset'):
    output_dir = os.path.abspath(os.path.expanduser(output_dir))

    def check_annotations(df):
        event_dict = {k.lower(): 0 for k in ss.info.EVENT_DICT.keys()}
        for x in df.description:
            try:
                event_dict[x.lower()] += 1
            except:
                pass
        return any(event_dict.values())

    to_remove = []
    to_keep = []
    total = len(ss.data.study_list)
    for i, name in enumerate(ss.data.study_list):
        if i % 100 == 0:
            print('Processing %d of %d' % (i, total))
        path = os.path.join(ss.data_dir, 'Sleep_Data', name + '.tsv')
        df = pd.read_csv(path, sep='\t')
        if check_annotations(df) == False:
            to_remove.append(name)
        else:
            to_keep.append(name)

    print('Processd %d files' % i)
    print('%d files have no labeled sleeping stage' % len(to_remove))

    path = os.path.join(output_dir, 'Sleep_Data')
    _ = os.popen('mkdir -p ' + path).read()

    output_path = os.path.join(output_dir, 'Sleep_Data.tar.xz')
    cmd = 'cd %s && tar -cf - Health_Data | xz -T0 > %s' % (ss.data_dir, output_path)
    _ = os.popen(cmd).read()
     
    total = len(to_keep)

    for i, name in enumerate(to_keep):
        cmd = 'cd %s/Sleep_Data && tar -cf - %s* | xz -T0 > %s/Sleep_Data/%s.tar.xz' % (ss.data_dir, name, output_dir, name)
        # print(cmd)

        print('Compressing %s.edf and %s.tsv, %d of %d' % (name, name, i + 1, total))

        start = time()
        _ = os.popen(cmd).read()
        end = time()
        print('Compressed, used %.2f seconds' % (end - start))



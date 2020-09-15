import numpy as np
import mne
import os
from multiprocessing import Pool
import sleep_study as ss


channels = [
        'EEG C3-M2',
        'EEG O1-M2',
        'EEG O2-M1',
        'EEG CZ-O1',
        'EEG C4-M1',
        'EEG F4-M1',
        ]


out_dir = '~/preprocessed'
out_dir = os.path.expanduser(out_dir)

mne.set_log_file('log.txt')
existing = [x[:-4] for x in os.listdir('preprocessed')]

def preprocess(i):
    # Potential problem: the order of channels are not considered
    print('Processing %d' % i)
    import sleep_study as ss
    ss.init()
    study = ss.data.study_list[i]
    if study in existing:
        return
    try:
        raw = ss.data.load_study(study, verbose=False)
        if not all([name in raw.ch_names for name in channels]):
            return
        events, event_ids = mne.events_from_annotations(raw, event_id=ss.info.EVENT_DICT, chunk_duration=30., verbose=None)
        sfreq = raw.info['sfreq']
        tmax = 30. - 1. / sfreq
        epochs = mne.Epochs(raw=raw, picks=channels, events=events, event_id=event_ids, tmin=0., tmax=tmax, baseline=None, verbose=None)
        epochs.load_data()
        if sfreq > 256:
            epochs = epochs.resample(256, npad='auto')
        data = epochs.get_data()
        labels = events[:, -1]
        np.savez_compressed(out_dir + '/' + study, data=data, labels = labels)
    except:
        pass



with Pool(10) as pool:
    pool.map(preprocess, range(3984))


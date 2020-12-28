import mne
import os
import pandas as pd
import numpy as np
from dateutil import parser
from datetime import timezone
import pywt
from scipy import signal, interpolate

import sleep_study as ss

study_list = None # Will be initialized after the module is initialized.

def clean_ch_names(ch_names):
    return [x.upper() for x in ch_names]

def init_study_list():
    path = os.path.join(ss.data_dir, 'Sleep_Data')
    return [x[:-4] for x in os.listdir(path) if x.endswith('edf')]

def init_age_file():
    new_fn = 'age_file.csv'
    age_path = os.path.join(ss.data_dir, 'Health_Data', ss.info.SLEEP_STUDY)   

    df = pd.read_csv(age_path, sep=',', dtype='str')
    df['FILE_NAME'] = df["STUDY_PAT_ID"].str.cat(df["SLEEP_STUDY_ID"], sep='_')

    df.to_csv(new_fn, columns=["FILE_NAME", "AGE_AT_SLEEP_STUDY_DAYS"], index=False)
    return os.path.abspath(new_fn)


def load_study(name, preload=False, exclude=[], verbose='CRITICAL'):
    path = os.path.join(ss.data_dir, 'Sleep_Data', name + '.edf')
    path = os.path.abspath(path)
    # file_size = os.stat(path).st_size / 1024 / 1024

    raw = mne.io.edf.edf.RawEDF(input_fname=path, exclude=exclude, preload=preload,
                                verbose=verbose)

    patient_id, study_id = name.split('_')

    tmp = ss.info.SLEEP_STUDY
    date = tmp[(tmp.STUDY_PAT_ID == int(patient_id))
             & (tmp.SLEEP_STUDY_ID == int(study_id))] \
                     .SLEEP_STUDY_START_DATETIME.values[0] \
                     .split()[0]

    time = str(raw.info['meas_date']).split()[1][:-6]

    new_datetime = parser.parse(date + ' ' + time + ' UTC') \
                         .replace(tzinfo=timezone.utc)

    raw.set_meas_date(new_datetime)
    # raw._raw_extras[0]['meas_date'] = new_datetime

    annotation_path = os.path.join(ss.data_dir, 'Sleep_Data', name + '.tsv')
    df = pd.read_csv(annotation_path, sep='\t')
    annotations = mne.Annotations(df.onset, df.duration, df.description,
                                  orig_time=new_datetime)

    raw.set_annotations(annotations)

    raw.rename_channels({name: name.upper() for name in raw.info['ch_names']})

    return raw

def get_sleep_eeg_and_stages(name, channels=ss.info.EEG_CH_NAMES, verbose=False, downsample=True):
    raw = ss.data.load_study(name)
    
    freq = int(raw.info['sfreq']) # 256, 400, 512
    n_samples = raw.n_times
    
    if verbose:
        print('sampling rate:', freq, 'Hz')
        print('channel names:', raw.info['ch_names'])
        print( )
        sleep_stage_stats = ss.data.sleep_stage_stats([study])
        print( )
    
    events, event_id = mne.events_from_annotations(raw, event_id = ss.info.EVENT_DICT, verbose=verbose)
    
    labels = []
    data = []
    
    for event in events:
        label, onset = event[[2, 0]]
        
        # get 30 seconds of data corresponding to the label
        indices = [onset, onset + ss.info.INTERVAL*freq]
        
        if indices[1] <= n_samples:
            interval_data = raw.get_data(channels, start=indices[0], stop=indices[1]) 
            data.append(interval_data) 
            labels.append(label)
            # sometimes the last interval seems to go over the length of the data and cause problems.
            # it's probably okay to just skip those for now.
   
    labels = np.array(labels)
    data = np.array(data)
        
    # Downsample to 128Hz
    if downsample:
        if freq % ss.info.REFERENCE_FREQ == 0:
            k = freq//ss.info.REFERENCE_FREQ
            data = data[:,:,::k]

        elif freq != ss.info.REFERENCE_FREQ:
            x = np.linspace(0, ss.info.INTERVAL, num=ss.info.INTERVAL*freq)
            new_x = np.linspace(0, ss.info.INTERVAL, num=ss.info.INTERVAL*ss.info.REFERENCE_FREQ)

            f = interpolate.interp1d(x, data, kind='linear', axis= -1, assume_sorted=True)
            data = f(new_x)   
    
    # data is (num events) by (num channels) by (30s x ss.info.REFERENCE_FREQ)            
    return np.array(data), labels

def get_demo_wavelet_features(data, n=4, level=2):
    
    def get_stats(x, axis=-1):
        stats = []
        stats.extend(np.expand_dims(np.mean(x, axis), 0))
        stats.extend(np.expand_dims(np.std(x, axis), 0))
        stats.extend(np.expand_dims(np.min(x, axis),0))
        stats.extend(np.expand_dims(np.max(x, axis),0))

        return np.array(stats)   
    
    coeffs = pywt.wavedec(data, 'db%d' % n, level=level, axis=-1)

    # coeffs is a list of length (level+1)
    # coeffs[i] is an array of size (data.shape[0] == num events) by (data.shape[1] == num channels) by (-1)
    res = []

    for i in range(len(coeffs)):
        stats = get_stats(coeffs[i]) # this has (num stats) by (num events) by (num channels)
        res.extend(stats)    

    return np.array(res).transpose((1, 2, 0))

def get_demo_wavelet_features_and_labels(name):
    data, labels = get_sleep_eeg_and_stages(name)
    features = get_demo_wavelet_features(data)
    
    return features, labels

def channel_stats(verbose=True):
    study_ch_names = {}

    for i, study in enumerate(study_list):

        if (i % 10 == 0) and verbose:
            print('Processing %d of %d' % (i, len(study_list)))

        raw = load_study(study)
        study_ch_names[study] = raw.ch_names

    names = {}
    for y in study_ch_names.values():
        for x in y:
            x = x.upper()
            try:
                names[x] += 1
            except:
                names[x] = 1

    names = {k: v for k, v in sorted(names.items(), key=lambda item: item[1], reverse=True)}

    print('\n'.join('%-20s %4d &  %.2f%%\\' % (k, v, v / len(study_list) * 100) for k, v in names.items()))
    return names


def sleep_stage_stats(studies=[]):
    res = {k.lower(): 0 for k in ss.info.EVENT_DICT}
    if len(studies)<1:
        studies = study_list
        
    for i, study in enumerate(studies):

        if (i + 1) % 100 == 0:
            print('Processed %d of %d' % (i + 1, len(studies)))

        annotation_path = os.path.join(ss.data_dir, 'Sleep_Data', study+ '.tsv')
        df = pd.read_csv(annotation_path, sep='\t')

        for event in df.description.tolist():
            try:
                res[event.lower()] += 1
            except:
                pass

    total = sum(res.values())

    print('Stage  Observations  Percentage')
    print('\n'.join(['%-2s     %7d        %6.3f%%' % (k.split()[-1], v, v / total * 100) for (k, v) in res.items()]))

    return res

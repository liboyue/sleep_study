import mne
import os
import pandas as pd
from dateutil import parser
from datetime import timezone

import sleep_study as ss

study_list = None # Will be initialized after the module is initialized.

def clean_ch_names(ch_names):
    return [x.upper() for x in ch_names]

def init_study_list():
    path = os.path.join(ss.data_dir, 'Sleep_Data')
    return [x[:-4] for x in os.listdir(path) if x.endswith('edf')]

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

def channel_stats():
    study_ch_names = {}

    for i, study in enumerate(study_list):

        if i % 10 == 0:
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

    print('\n'.join('%-20s %4d   %.2f%%' % (k, v, v / 3971 * 100) for k, v in names.items()))
    return names


def sleep_stage_stats():
    res = {k.lower(): 0 for k in ss.info.EVENT_DICT}

    for i, study in enumerate(study_list):

        if (i + 1) % 100 == 0:
            print('Processed %d of %d' % (i + 1, len(study_list)))

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




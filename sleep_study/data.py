import mne
import os
import pandas as pd
from dateutil import parser
from datetime import timezone

from . import data_dir, info


def load_study(name, preload=False, exclude=[], verbose='CRITICAL'):
    path = os.path.join(data_dir, 'Sleep_Data', name + '.edf')
    path = os.path.abspath(path)
    # file_size = os.stat(path).st_size / 1024 / 1024

    raw = mne.io.edf.edf.RawEDF(input_fname=path, exclude=exclude, preload=preload,
                                verbose=verbose)

    patient_id, study_id = name.split('_')

    tmp = info.SLEEP_STUDY
    date = tmp[(tmp.STUDY_PAT_ID == int(patient_id))
             & (tmp.SLEEP_STUDY_ID == int(study_id))] \
                     .SLEEP_STUDY_START_DATETIME[0] \
                     .split()[0]

    time = str(raw.info['meas_date']).split()[1][:-6]

    new_datetime = parser.parse(date + ' ' + time + ' UTC') \
                         .replace(tzinfo=timezone.utc)

    annotation_path = os.path.join(data_dir, 'Sleep_Data', name + '.tsv')
    df = pd.read_csv(annotation_path, sep='\t')
    annotations = mne.Annotations(df.onset, df.duration, df.description,
                                  orig_time=new_datetime)

    raw.info['meas_date'] = new_datetime
    raw.set_annotations(annotations)

    return raw

def init_study_list():
    path = os.path.join(data_dir, 'Sleep_Data')
    return [x[:-4] for x in os.listdir(path) if x.endswith('edf')]


study_list = init_study_list()


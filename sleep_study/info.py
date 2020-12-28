import os
import pandas as pd

import sleep_study as ss

EVENT_DICT = {
        'Sleep stage W' : 0,
        'Sleep stage N1': 1,
        'Sleep stage N2': 2,
        'Sleep stage N3': 3,
        'Sleep stage R' : 4,
        }

FREQ_BANDS = [
        [0.5, 4],   # delta
        [1, 4],     # delta
        [4, 8],     # theta
        [8, 12],    # alpha
        [12, 30],   # beta
        [30, 100],  # gamma
        ]

# varies per study
EEG_CH_NAMES = [
        'EEG F4-M1',
        'EEG O2-M1',
        'EEG C4-M1',
        'EEG O1-M2',
        'EEG F3-M2',
        'EEG C3-M2',
        'EEG CZ-O1',
        ]

# varies per study
NONE_EEG_CH_NAMES = [
        'ECG EKG2-EKG',
        'EOG LOC-M2',
        'EOG ROC-M1',
        'EEG Chin1-Chin2',
        'EMG Chin1-Chin2',
        'EMG LLeg-RLeg',
        'Capno',
        'C-flow',
        'EtCO2',
        'Patient Event',
        'Pressure',
        'Rate',
        'Resp Abdominal',
        'Resp Airflow',
        'Resp PTAF',
        'Resp Rate',
        'Resp Thoracic',
        'SpO2',
        'Snore',
        'Tidal Vol',
        ]

ALL_CH_NAMES = EEG_CH_NAMES + NONE_EEG_CH_NAMES

# The Following files are loaded only when needed
DEMOGRAPHIC = 'DEMOGRAPHIC.csv'
DIAGNOSIS = 'DIAGNOSIS.csv'
ENCOUNTER = 'ENCOUNTER.csv'
MEASUREMENT = 'MEASUREMENT.csv'
MEDICATION = 'MEDICATION.csv'
PROCEDURE_SURG_HX = 'PROCEDURE_SURG_HX.csv'
PROCEDURE = 'PROCEDURE.csv'
SLEEP_ENC_ID = 'SLEEP_ENC_ID.csv'
SLEEP_STUDY = 'SLEEP_STUDY.csv'

HEALTH_DATA_FNS = [DEMOGRAPHIC,
                   DIAGNOSIS, 
                   ENCOUNTER, 
                   MEASUREMENT, 
                   MEDICATION, 
                   PROCEDURE_SURG_HX, 
                   PROCEDURE, 
                   SLEEP_ENC_ID, 
                   SLEEP_STUDY]
INTERVAL = 30 # seconds.
REFERENCE_FREQ = 128 # Hz. 80% of the studies have sampling frequency of 256 HZ.

def load_health_info(name):
    if type(name) == str:
        path = os.path.join(ss.data_dir, 'Health_Data', name)
        name = pd.read_csv(path)
    return name


def hist(l, h={}):
    for k in l:
        try:
            h[k] += 1
        except:
            h[k] = 1
    return h

def normalize(h):
    N = sum(h.values())
    for k in h.keys():
        h[k] /= N
    return h

def patient_cohort():
    global DEMOGRAPHIC
    DEMOGRAPHIC = load_health_info(DEMOGRAPHIC)

    N = len(DEMOGRAPHIC)

    DEMOGRAPHIC = a

    race_hist = hist(DEMOGRAPHIC.RACE_DESCR.values)

    for race in list(race_hist.keys()):
        if race != 'Unknown' and race_hist[race] <= 10:
            race_hist['Unknown'] += race_hist[race]
            del race_hist[race]

    normalize(race_hist)

    gender_hist = hist(DEMOGRAPHIC.GENDER_DESCR.values)
    normalize(gender_hist)


    global ENCOUNTER
    ENCOUNTER = load_health_info(ENCOUNTER)


    a = ENCOUNTER[['STUDY_PAT_ID', 'VISIT_START_DATETIME', 'VISIT_END_DATETIME']]

    a = ENCOUNTER[['STUDY_PAT_ID', 'ENCOUNTER_DATE']]
    # df['DataFrame Column'] = pd.to_datetime(df['DataFrame Column'], format=specify your format)
    a['ENCOUNTER_DATE'] = pd.to_datetime(a['ENCOUNTER_DATE'])
    b = a.groupby('STUDY_PAT_ID')
    b.groups.keys()

    c = b.ENCOUNTER_DATE.max() - b.ENCOUNTER_DATE.min()
    c = c.values / np.timedelta64(1, 'D')
    c /= 365



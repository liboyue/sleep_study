import os
import pandas as pd
from . import data_dir

EVENT_DICT = {
        'Sleep stage W' : 0,
        'Sleep stage N1': 1,
        'Sleep stage N2': 2,
        'Sleep stage N3': 3,
        'Sleep stage R' : 4,
        }

FREQ_BANDS = [
        [8, 12], # alpha
        # [12, 30], # beta
        # [1, 4], # delta
        # [4, 8], # theta
        [30, 100], # gamma
        ]

EEG_CH_NAMES = [
        'EEG F4-M1',
        'EEG O2-M1',
        'EEG C4-M1',
        'EEG O1-M2',
        'EEG F3-M2',
        'EEG C3-M2',
        'EEG CZ-O1',
        ]

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


def load_health_info(name):
    if type(name) == str:
        path = os.path.join(data_dir, 'Health_Data', name)
        name = pd.read_csv(path)
    return name


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

# Load the sleep study info
SLEEP_STUDY = load_health_info(SLEEP_STUDY)

# def __getattr__(name):
    # if name == 'y':
        # return 3
    # raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

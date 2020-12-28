import pandas as pd


def load_demo(fp_in, convert_datetime):
    demo_dtypes = {'STUDY_PAT_ID': int,
                   'BIRTH_DATE': object,
                   'PCORI_GENDER_CD': object,
                   'PCORI_RACE_CD': object,
                   'PCORI_HISPANIC_CD': object,
                   'GENDER_DESCR': object,
                   'RACE_DESCR': object,
                   'ETHNICITY_DESCR': object,
                   'LANGUAGE_DESCR': object,
                   'PEDS_GEST_AGE_NUM_WEEKS': object,
                   'PEDS_GEST_AGE_NUM_DAYS': object}
    df = pd.read_csv(fp_in, dtype=demo_dtypes, encoding='ISO-8859-1')
    if convert_datetime:
        df['BIRTH_DATE'] = pd.to_datetime(df['BIRTH_DATE'], infer_datetime_format=True)
    return df


def load_diag(fp_in, convert_datetime):
    diag_dtypes = {'STUDY_DX_ID': object,
                   'STUDY_ENC_ID': object,
                   'STUDY_PAT_ID': int,
                   'DX_START_DATETIME': object,
                   'DX_END_DATETIME': object,
                   'DX_SOURCE_TYPE': object,
                   'DX_ENC_TYPE': object,
                   'DX_CODE_TYPE': object,
                   'DX_CODE': object,
                   'DX_NAME': object,
                   'DX_ALT_CODE': object,
                   'CLASS_OF_PROBLEM': object,
                   'CHRONIC_YN': object,
                   'PROV_ID': object}
    df = pd.read_csv(fp_in, dtype=diag_dtypes, encoding='ISO-8859-1')
    if convert_datetime:
        df['DX_START_DATETIME'] = pd.to_datetime(df['DX_START_DATETIME'], infer_datetime_format=True)
        df['DX_END_DATETIME'] = pd.to_datetime(df['DX_END_DATETIME'], infer_datetime_format=True)
    return df


def load_enc(fp_in, convert_datetime):
    enc_dtypes = {'STUDY_ENC_ID': int,
                  'STUDY_PAT_ID': int,
                  'ENCOUNTER_DATE': object,
                  'VISIT_START_DATETIME': object,
                  'VISIT_END_DATETIME': object,
                  'ADT_ARRIVAL_DATETIME': object,
                  'ED_DEPARTURE_DATETIME': object,
                  'ENCOUNTER_TYPE': object,
                  'VISIT_TYPE_CD': object,
                  'VISIT_TYPE_DESCR': object,
                  'ICU_VISIT_YN': object,
                  'PROV_ID': object,
                  'PROV_TYPE': object,
                  'DEPT_ID': object,
                  'DEPT_SPECIALITY': object,
                  'ADMIT_SOURCE': object,
                  'HOSP_ADMIT_SOURCE': object,
                  'DISCHARGE_DISPOSITION': object,
                  'DISCHARGE_DESTINATION': object,
                  'DRG_CODE': object,
                  'DRG_NAME': object,
                  'VISIT_REASON': object}
    df = pd.read_csv(fp_in, dtype=enc_dtypes, encoding='ISO-8859-1')
    if convert_datetime:
        df['ENCOUNTER_DATE'] = pd.to_datetime(df['ENCOUNTER_DATE'], infer_datetime_format=True)
        df['VISIT_START_DATETIME'] = pd.to_datetime(df['VISIT_START_DATETIME'], infer_datetime_format=True)
        df['VISIT_END_DATETIME'] = pd.to_datetime(df['VISIT_END_DATETIME'], infer_datetime_format=True)
        df['ADT_ARRIVAL_DATETIME'] = pd.to_datetime(df['ADT_ARRIVAL_DATETIME'], infer_datetime_format=True)
        df['ED_DEPARTURE_DATETIME'] = pd.to_datetime(df['ED_DEPARTURE_DATETIME'], infer_datetime_format=True)
    return df


def load_meas(fp_in, convert_datetime):
    meas_dtypes = {'STUDY_MEAS_ID': object,
                   'STUDY_ENC_ID': object,
                   'STUDY_PAT_ID': int,
                   'MEAS_RECORDED_DATETIME': object,
                   'MEAS_TYPE': object,
                   'MEAS_VALUE_NUMBER': float,
                   'MEAS_VALUE_TEXT': object,
                   'MEAS_SOURCE': object,
                   'STUDY_PROV_ID': object}
    df = pd.read_csv(fp_in, dtype=meas_dtypes, encoding='ISO-8859-1')
    if convert_datetime:
        df['MEAS_RECORDED_DATETIME'] = pd.to_datetime(df['MEAS_RECORDED_DATETIME'], infer_datetime_format=True)
    return df


def load_med(fp_in, convert_datetime):
    med_dtypes = {'STUDY_MED_ID': object,
                  'STUDY_ENC_ID': object,
                  'STUDY_PAT_ID': int,
                  'MED_START_DATETIME': object,
                  'MED_END_DATETIME': object,
                  'MED_ORDER_DATETIME': object,
                  'MED_TAKEN_DATETIME': object,
                  'MED_SOURCE_TYPE': object,
                  'QUANTITY': object,
                  'DAYS_SUPPLY': object,
                  'FREQUENCY': object,
                  'EFFECTIVE_DRUG_DOSE': object,
                  'EFF_DRUG_DOSE_SOURCE_VALUE': object,
                  'DRUG_DOSE_UNIT': object,
                  'REFILLS': object,
                  'RXNORM_CODE': object,
                  'RXNORM_TERM_TYPE': object,
                  'MEDICATION_DESCR': object,
                  'GENERIC_DRUG_DESCR': object,
                  'DRUG_ORDER_STATUS': object,
                  'DRUG_ACTION': object,
                  'ROUTE': object,
                  'ROUTE_SOURCE_VALUE': object,
                  'PRESCRIBING_PROV_ID': object,
                  'PHARM_CLASS': object,
                  'PHARM_SUBCLASS': object,
                  'THERA_CLASS': object,
                  'THERA_SUBCLASS': object}
    df = pd.read_csv(fp_in, dtype=med_dtypes, encoding='ISO-8859-1')
    if convert_datetime:
        df['MED_START_DATETIME'] = pd.to_datetime(df['MED_START_DATETIME'], infer_datetime_format=True)
        df['MED_END_DATETIME'] = pd.to_datetime(df['MED_END_DATETIME'], infer_datetime_format=True)
        df['MED_ORDER_DATETIME'] = pd.to_datetime(df['MED_ORDER_DATETIME'], infer_datetime_format=True)
        df['MED_TAKEN_DATETIME'] = pd.to_datetime(df['MED_TAKEN_DATETIME'], infer_datetime_format=True)
    return df


def load_proc(fp_in, convert_datetime):
    proc_dtypes = {'STUDY_PROC_ID': object,
                   'STUDY_ENC_ID': object,
                   'STUDY_PAT_ID': int,
                   'PROCEDURE_DATETIME': object,
                   'STUDY_PROV_ID': object,
                   'PROC_ID_NCH': object,
                   'PROC_CODE': object,
                   'PROC_CODE_TYPE': object,
                   'PROC_DESCR': object}
    df = pd.read_csv(fp_in, dtype=proc_dtypes, encoding='ISO-8859-1')
    if convert_datetime:
        df['PROCEDURE_DATETIME'] = pd.to_datetime(df['PROCEDURE_DATETIME'], infer_datetime_format=True)
    return df


def load_proc_surg(fp_in, convert_datetime):
    proc_surg_dtypes = {'STUDY_SURGHX_ID': object,
                        'STUDY_ENC_ID': object,
                        'STUDY_PAT_ID': int,
                        'PROC_NOTED_DATE': object,
                        'PROC_START_TIME': object,
                        'PROC_END_TIME': object,
                        'PROV_ID': object,
                        'PROC_CODE': object,
                        'CPT_CODE': object,
                        'PROC_DESCR': object}
    df = pd.read_csv(fp_in, dtype=proc_surg_dtypes, encoding='ISO-8859-1')
    if convert_datetime:
        df['PROC_NOTED_DATE'] = pd.to_datetime(df['PROC_NOTED_DATE'], infer_datetime_format=True)
        df['PROC_START_TIME'] = pd.to_datetime(df['PROC_START_TIME'], infer_datetime_format=True)
        df['PROC_END_TIME'] = pd.to_datetime(df['PROC_END_TIME'], infer_datetime_format=True)
    return df


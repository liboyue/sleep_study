from . import info
from . import data
from . import dataset

data_dir = None

def init(tmp_dir='/ux0/data/NCH_Sleep_Data'):
    global data_dir
    data_dir = tmp_dir
    data.study_list = data.init_study_list()
    age_fn = data.init_age_file()
    print("age information stored in", age_fn)

    # Load the sleep study info
    info.SLEEP_STUDY = info.load_health_info(info.SLEEP_STUDY, False)

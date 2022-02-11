import os
from core.search import search
from core.csv_tools import append_csv, split_csv_to

KEYWORD = '"fun fact" lang:en'
TARGET_RESULTS = 100000
BIG_FILE_PATH = 'fun_fact_on_Twitter.csv'

# Must edit section
SAVING_PATH = 'fun_fact_031.csv'
END_TIME = None # in the future, will be fetched first
START_TIME = '2022-02-07T02:34:46.000Z' # in the past, will be fetched at the end

search_result = search(
    keyword=KEYWORD,
    maximum_result=TARGET_RESULTS,
    saving_path=SAVING_PATH,
    include_retweet=False,
    end_time=END_TIME,
    start_time=START_TIME)


saving_paths = SAVING_PATH.split('.')
new_saving_path = saving_paths[0] + ' +' + str(search_result - 1) + '.' + saving_paths[-1]
os.rename(SAVING_PATH, new_saving_path)

if (os.path.isfile(BIG_FILE_PATH)):
    append_csv(BIG_FILE_PATH, new_saving_path)

    split_csv_to(
        source_csv=BIG_FILE_PATH,
        num=100000,
        result_csv=BIG_FILE_PATH
    )

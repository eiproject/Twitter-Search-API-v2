import os
from core.search import search
from core.csv_tools import append_csv, split_csv_to

KEYWORD = 'teroris OR terroris lang:id'
TARGET_RESULTS = 100000
BIG_FILE_PATH = 'indonesian_tweet_about_teroris.csv'

# Must edit section
SAVING_PATH = 'terroris_024.csv'
END_TIME = None # in the future, will be fetched first
START_TIME = '2022-01-18T09:21:37.000Z' # in the past, will be fetched at the end

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

if (os.path.isdir(BIG_FILE_PATH)):
    append_csv(BIG_FILE_PATH, new_saving_path)

    split_csv_to(
        source_csv=BIG_FILE_PATH,
        num=100000,
        result_csv=BIG_FILE_PATH
    )

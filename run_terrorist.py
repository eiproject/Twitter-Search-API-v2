from core.search import search

KEYWORD = 'teroris OR terroris lang:id'
TARGET_RESULTS = 100000
SAVING_PATH = 'terroris_021.csv'
END_TIME = None # in the future, will be fetched first
START_TIME = '2022-01-17T01:56:30.000Z' # in the past, will be fetched at the end

search_result = search(
    keyword=KEYWORD,
    maximum_result=TARGET_RESULTS,
    saving_path=SAVING_PATH,
    include_retweet=False,
    end_time=END_TIME,
    start_time=START_TIME)

import os

saving_paths = SAVING_PATH.split('.')
new_saving_path = saving_paths[0] + '+' + str(search_result - 1) + '.' + saving_paths[-1]
os.rename(SAVING_PATH, new_saving_path)
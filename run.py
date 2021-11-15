from core.search import search

KEYWORD = 'banjir'
TARGET_RESULTS = 10000
SAVING_PATH = 'result_banjir.csv'

search(
    keyword=KEYWORD,
    maximum_result=TARGET_RESULTS,
    saving_path=SAVING_PATH,
    include_retweet=False)
from core.search import search

KEYWORD = 'crypto haram'
TARGET_RESULTS = 10
SAVING_PATH = 'result.csv'

search(
    keyword=KEYWORD,
    maximum_result=TARGET_RESULTS,
    saving_path=SAVING_PATH,
    include_retweet=False)
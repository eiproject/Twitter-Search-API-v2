from core.search import search

KEYWORD = 'banjir'
TARGET_RESULTS = 100
SAVING_PATH = 'banjir.csv'

search(
    keyword=KEYWORD,
    maximum_result=TARGET_RESULTS,
    saving_path=SAVING_PATH)
import requests, json, csv
from core import bearer

def create_headers():
    headers = {"Authorization": "Bearer {}".format(bearer)}
    return headers

def create_url(keyword):
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    query_params = {
        'query': keyword, 'max_results': 100, 
        'expansions': 'in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id',
        'tweet.fields': 'created_at,public_metrics'
    }
    return search_url, query_params

def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    # print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def check_tweet_type(tweet_dict):
    if 'referenced_tweets' in tweet_dict:
        return tweet_dict['referenced_tweets'][0]['type'], tweet_dict['referenced_tweets'][0]['id']
    else:
        return 'original', None

def write_csv_header(csv_path):
    with open(csv_path, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(['tweet id', 'tweet text', 'reference type', 'reference id', 'created at', 'like', 'quote', 'reply', 'retweet'])

def save_to_csv(csv_path, array_response):
    with open(csv_path, 'a', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        for dict_data in array_response:
            ref_type, ref_id = check_tweet_type(dict_data)
            writer.writerow(
                [dict_data['id'], dict_data['text'], ref_type, ref_id, dict_data['created_at'], 
                 dict_data['public_metrics']['like_count'],
                 dict_data['public_metrics']['quote_count'],
                 dict_data['public_metrics']['reply_count'],
                 dict_data['public_metrics']['retweet_count']]
                )
        
def search(keyword, maximum_result, saving_path):
    url, params = create_url(keyword)
    token = None
    search_result = 0
    is_searching = True
    
    write_csv_header(saving_path)
    
    while is_searching:
        json_response = connect_to_endpoint(
            url=url, 
            headers=create_headers(), 
            params=params, 
            next_token=token)
        
        # print(json.dumps(json_response, indent=2, sort_keys=True))

        if 'next_token' in json_response['meta']:
            token = json_response['meta']['next_token']
        else:
            is_searching = False
            print('Have fetch all Tweets from keyword: {}'.format(keyword))
        
        array_response = json_response['data']
        temp_array_response = []
        for response in array_response:
            if 'referenced_tweets' not in response:
                temp_array_response.append(response)
            else:
                if response['referenced_tweets'][0]['type'] != 'retweeted':
                    temp_array_response.append(response)
        
        array_response = temp_array_response
        
        response_count = len(array_response)
        if search_result + response_count > maximum_result:
            limit_array_response_to = maximum_result - search_result
            array_response = array_response[:limit_array_response_to]
            search_result += limit_array_response_to
            is_searching = False
        else:
            search_result += response_count
            
        print('+', len(array_response))
        print(search_result)
        save_to_csv(saving_path, array_response)
        
        
import requests, json, csv
from core import bearer
from .secret import my_bearer, my_bearer2

def switch_bearer(bearer):
    if bearer == my_bearer:
        bearer = my_bearer2
    else:
        bearer = my_bearer
    return bearer

def create_headers():
    headers = {"Authorization": "Bearer {}".format(switch_bearer(bearer))}
    return headers

def create_url(keyword, end_time, start_time):
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    query_params = {
        'query': keyword, 'max_results': 100, 
        'expansions': 'in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id',
        'tweet.fields': 'created_at,public_metrics,entities',
        'user.fields': 'username',
        
    }
    if end_time:
        query_params['end_time'] = end_time
        
    if start_time:
        query_params['start_time'] = start_time
        
    return search_url, query_params

def connect_to_endpoint(url, headers, params, next_token=None):
    params['next_token'] = next_token 
    response = requests.request("GET", url, headers = headers, params = params)
    # if response.status_code != 200:
    #     raise Exception(response.status_code, response.text)
    return response.json()

def check_tweet_type(tweet_dict):
    if 'referenced_tweets' in tweet_dict:
        return tweet_dict['referenced_tweets'][0]['type'], \
            tweet_dict['referenced_tweets'][0]['id']
    else:
        return 'original', None

def write_csv_header(csv_path):
    with open(csv_path, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(['tweet id', 'name', 'username', 'tweet text', 'reference type', 'reference id', 
                         'created at', 'like', 'quote', 'reply', 'retweet', 'tweet url', 'mentions',
                         'hashtags'])


def fetch_hashtags(dict_data):
    hashtags = ''
    if 'entities' in dict_data:
        entities = dict_data['entities']
        if 'hashtags' in entities:
            for hashtag in entities['hashtags']:
                hashtags+=hashtag['tag']+','
        else:
            pass
        
        # remove comma in the end
        if len(hashtags) > 0:
            hashtags = hashtags[:-1]
        
    return hashtags

def fetch_mentions(dict_data):
    mentions = ''
    if 'entities' in dict_data:
        entities = dict_data['entities']
        if 'mentions' in entities:
            for mention in entities['mentions']:
                mentions+='@'+mention['username']+','
        else:
            pass
        
        # remove comma in the end
        if len(mentions) > 0:
            mentions = mentions[:-1]
        
    return mentions

def save_to_csv(csv_path, array_response_data, response_users):
    with open(csv_path, 'a', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        i = 0
        for dict_data in array_response_data:
            tweet_id = dict_data['id']
            ref_type, ref_id = check_tweet_type(dict_data)
            name = response_users[dict_data['author_id']]['name']
            username = response_users[dict_data['author_id']]['username']
            mentions = fetch_mentions(dict_data)
            hashtags = fetch_hashtags(dict_data)
            writer.writerow(
                [
                    tweet_id, 
                    name,
                    username,
                    dict_data['text'], 
                    ref_type, 
                    ref_id, 
                    dict_data['created_at'], 
                    dict_data['public_metrics']['like_count'],
                    dict_data['public_metrics']['quote_count'],
                    dict_data['public_metrics']['reply_count'],
                    dict_data['public_metrics']['retweet_count'],
                    'https://twitter.com/' + username + '/status/' + tweet_id,
                    mentions,
                    hashtags
                ]
            )
            # print(dict_data['created_at'], dict_data['text'])
            i+=1

def fetch_users(json_response):
    users_dict = {}
    all_users = json_response['includes']['users']
    for user in all_users:
        if user['id'] not in users_dict:
            users_dict[user['id']] = {'name': user['name'], 'username': user['username']}
    return users_dict

def search(keyword, maximum_result, saving_path, include_retweet=False, end_time=None, start_time=None):
    url, params = create_url(keyword, end_time, start_time)
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
        
        if 'status' in json_response:
            if json_response['status'] == 429:
                print(json.dumps(json_response, indent=2, sort_keys=True))
                print('Too Many Requests')
                # import time
                # time.sleep(60) # seconds
                bearer = switch_bearer(bearer)
                continue

        if 'next_token' in json_response['meta']:
            token = json_response['meta']['next_token']
        else:
            is_searching = False
            print('Have fetch all Tweets from keyword: {}'.format(keyword))
        
        array_response_data = json_response['data']
        array_response_users = fetch_users(json_response)
        
        if not include_retweet:
            temp_array_response_data = []
            i = 0
            for response in array_response_data:
                if 'referenced_tweets' not in response:
                    temp_array_response_data.append(response)
                else:
                    if response['referenced_tweets'][0]['type'] != 'retweeted':
                        temp_array_response_data.append(response)
                i+=1
            
            array_response_data = temp_array_response_data
        
        response_count = len(array_response_data)
        if search_result + response_count > maximum_result:
            limit_array_response_to = maximum_result - search_result
            array_response_data = array_response_data[:limit_array_response_to]
            search_result += limit_array_response_to
            is_searching = False
        else:
            search_result += response_count
            
        save_to_csv(saving_path, array_response_data, array_response_users)
        
        print('+', len(array_response_data))
        print(search_result)
        
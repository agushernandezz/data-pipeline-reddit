import requests
import pandas as pd
import datetime
import json

def return_api_dataframe():
    try:
    
    setup = open("setup.json")
    setup_data = json.load(setup)
    CLIENT_ID = setup_data["conf"]['CLIENT_ID']
    SECRET_KEY = setup_data["conf"]['SECRET_KEY']
    USERNAME = setup_data["conf"]['USERNAME']
    PASSWORD = setup_data["conf"]['PASSWORD']
    subreddit = setup_data["conf"]['subreddit']

    except Exception as e:
        print(f"Error with setup.json input. Error: {e}.")

    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

    data = {
            'grant_type': 'password',
            'username': USERNAME,
            'password': PASSWORD,
            }

    headers = {'User-Agent': 'Reddit-Data-Pipeline/0.0.1'}

    try:
        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth = auth, data = data, headers = headers)
    except Exception as e:
        print(f"Unable to connect to the API. Error: {e}.")

    if res.status_code == 200:
        try:
            TOKEN = res.json()['access_token']

            headers['Authorization'] = f'bearer {TOKEN}'
        except Exception as e:
            print(f"Unable to connect to the API, token error. Error: {e}")
    else:
        print("Request to the API failed with status code:", res.status_code)
    
    oauth_subreddit = str('https://oauth.reddit.com/r/' + subreddit + '/new')
    res = requests.get(oauth_subreddit, headers=headers, params = {
        "limit": 100,
    })
    
    r = res.json()

    post_id = []
    title = []
    author = []
    created_utc = [] 
    score = []
    upvote_ratio = []
    ups = []
    downs = []
    num_comments = []
    url = []
    spoiler = []
    over_18 = []
    name = []

    reddit_dict = {
        "id" : post_id,
        "title": title,
        "author" : author,
        "created_utc" : created_utc,
        "score": score,
        "upvote_ratio": upvote_ratio,
        "num_comments": num_comments,
        "url": url,
        "spoiler": spoiler,
        "over_18": over_18,
        "name": name
    }

    # current day and time
    now = datetime.datetime.now()

    # start of the day of the week of `now`
    day_cap = now.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=7)

    upper_bound_week = True

    while(upper_bound_week):
        for post in r['data']['children']:
            for key in reddit_dict.keys():
                reddit_dict[key].append(post["data"][key])
        last_post_date = datetime.datetime.fromtimestamp((r["data"]["children"][len((r["data"]["children"])) - 1])['data']['created_utc'])
        upper_bound_week = day_cap < last_post_date
        if(upper_bound_week):
            try:
                r = requests.get(oauth_subreddit, headers=headers, params = {"limit": 100,
                                                                                                          "after": ((r["data"]["children"][len((r["data"]["children"])) - 1])['data']['name'])}).json()
            except Exception as e:
                print(f"Request to the API failed with status code: {res.status_code}, with Error: {e}")
                
    reddit_df = pd.DataFrame(reddit_dict, columns = ["id",
                                                 "title",
                                                 "author",
                                                 "created_utc",
                                                 "score",
                                                 "upvote_ratio",
                                                 "num_comments",
                                                 "url",
                                                 "spoiler",
                                                 "over_18",
                                                 "name"])
    return reddit_df

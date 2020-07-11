# temp variables to debug
game_id_list = [255710, 413150, 872790]
user_id_list = [76561198850951810, 76561198361743637, 76561198108005664, 76561198358725004]


# 1. game_list_df : game_id / game_title / review_count

def get_df_game_list():
    import json, urllib.request
    import time
    import pandas as pd

    my_df = pd.DataFrame(columns=['game_id', 'game_title', 'review_count'])
    json_url = 'http://api.steampowered.com/ISteamApps/GetAppList/v0002/'
    review_url = 'https://store.steampowered.com/appreviews/%s?json=1&language=all'
    game_list = []
    while True:
        try:
            with urllib.request.urlopen(json_url) as url:
                data = json.loads(url.read())
                break
        except:
            print("parsing error..")
            pass

    total_cnt = len(data['applist']['apps'])
    cnt = 0

    for i in data['applist']['apps']:
        dict_now_game = {'game_id': i['appid'], 'game_title': i['name']}
        game_id = i['appid']

        while True:
            try:
                with urllib.request.urlopen(review_url % game_id) as url:
                    data = json.loads(url.read())
                    if data['success'] == 1:
                        dict_now_game['review_count'] = data['query_summary']['total_reviews']
                    else:
                        dict_now_game['review_count'] = -1
                break
            except:
                print("parsing error..")
                pass

        game_list.append(dict_now_game)

        cnt = cnt + 1

        if cnt % 100 == 0 :
            print ("df_game_list : ", cnt , "/", total_cnt)

        # time.sleep(1.0)

    my_df = my_df.append(game_list)
    return my_df


# 2. game_tag_df : game_id / tag

def get_df_game_tag(game_id_list):
    import time
    from bs4 import BeautifulSoup
    import requests
    import sys
    from pprint import pprint
    import pandas as pd

    def get_soup(url):
        try:
            r = requests.get(url).text
            return BeautifulSoup(r, 'lxml')
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_details = {
                'filename': exc_traceback.tb_frame.f_code.co_filename,
                'lineno': exc_traceback.tb_lineno,
                'name': exc_traceback.tb_frame.f_code.co_name,
                'type': exc_type.__name__,
                'message': str(e)
            }
            pprint(traceback_details)
            return ' '

    def _parse_tag(page):
        try:
            tag = page.select('a[class=app_tag]')
            for i in range(len(tag)):
                tag[i] = tag[i].text.replace("\t", '').replace('\r', '').replace('\n', '')
            return tag
        except:
            return ' '

    df = pd.DataFrame(columns=['game_id', 'tag'])
    list_game_id_tag = []
    url_base = 'https://store.steampowered.com/app/%s'

    total_cnt = len(game_id_list)
    cnt = 0

    for game_id in game_id_list:
        url = url_base % game_id

        page = get_soup(url)
        tag = _parse_tag(page)
        if len(tag) > 0:
            for i in range(len(tag)):
                list_game_id_tag.append({'game_id': game_id, 'tag': tag[i]})

        cnt = cnt + 1

        if cnt % 100 == 0 :
            print("df_game_tag : ", cnt, "/", total_cnt)
        time.sleep(1.0)

    return df.append(list_game_id_tag)

    # display(dict_game_id_tag)
    # dict_game_id_tag.reset_index(drop=True)

    # return dict_game_id_tag.groupby(['game_id','tag'], as_index = False).mean().pivot('game_id','tag').fillna(0)


# 3. game_user_df (후기 기준) : game_id / user_id / review (Optional) / time (Optional)

def get_df_game_user(game_id_list, num = 100, language = 'en', num_per_page = 100) :

    import json, urllib.request
    from time import sleep
    from urllib import parse
    from datetime import datetime
    import pandas as pd

    def game_reviews(game_id):
        my_df = pd.DataFrame(columns=['game_id', 'user_id', 'review', 'time'])
        list_cur = []
        review_url = 'https://store.steampowered.com/appreviews/%s?json=1&filter=recent'
        cnt = 0
        list_review = []

        if (language == 'en'):
            review_url += '&language=english'
        elif (language == 'ko'):
            review_url += '&language=koreana'
        elif (language == 'all'):
            review_url += '&language=all'

        while True:
            try:
                with urllib.request.urlopen(review_url % game_id) as url:
                    data = json.loads(url.read())
                    print(data['query_summary']['total_reviews'])
                break
            except:
                print("parsing error..")
                pass

        review_url_form = review_url + '&num_per_page=%s&cursor=%s'
        cur = "*"

        while True :
            if (cur in list_cur):
                print("repeated cursor")
                break
            else:
                list_cur.append(cur)

            now_url = review_url_form % (game_id, num_per_page, parse.quote(cur))
            data = None
            while True:
                try:
                    with urllib.request.urlopen(now_url) as url:
                        data = json.loads(url.read())
                    break
                except:
                    print("parsing error..")
                    pass

            if data['success'] == 0:
                print("failed\n")
                break

            for j in range(0, data['query_summary']['num_reviews']):
                list_review.append({'game_id': game_id, 'user_id': data['reviews'][j]['author']['steamid'],
                                 'review': data['reviews'][j]['review'], 'time': data['reviews'][j]['timestamp_created']})

            cnt += data['query_summary']['num_reviews']

            cur = data['cursor']

            if cnt >= num :
                del list_review[num:]
                break

            #sleep(0.1)

        my_df = my_df.append(list_review, ignore_index=True)
        my_df['time'] = my_df['time'].apply(lambda x: datetime.fromtimestamp(int(x)))
        return my_df

    game_user = pd.DataFrame()
    total_cnt = len(game_id_list)
    cnt = 0

    for i in game_id_list:
        my_df = game_reviews(game_id=i)
        game_user = game_user.append(my_df, ignore_index=True)

        cnt = cnt + 1
        if cnt % 100 == 0 :
            print("game_user : ", cnt, "/", total_cnt)


    return game_user


# 4. user_list_df : user_id

def get_df_user_list(game_user):
    import pandas as pd
    return pd.DataFrame(game_user['user_id'].unique(), columns=['user_id'])
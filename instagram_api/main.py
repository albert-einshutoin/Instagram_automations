import json
import os
import pprint
import re
import requests
import sys
import sqlite3
import mysql.connector
import time as t

import settings as st

import pandas as pd


class InstaDiscover(object):

    def __init__(self, target=None):
        """Connect to api to get basic info, using connect_api func
        """
        self.target = str(target)
        self.DATABASE = 'instagram'
        result = self.connect_api(target=target)
        self.username = st.username
        self.password = st.password
        self.researched_time = t.strftime("%Y/%m/%d, %H:%M:%S")
        self.follow = result["business_discovery"]["follows_count"]
        self.follower = result["business_discovery"]["followers_count"]
        self.media_count = result["business_discovery"]["media_count"]
        self.medias_data = result["business_discovery"]["media"]
        self.data = self.medias_data["data"]
        self.list = []

    def connect_api(self, target=None):
        """Coonect api
        Args:
            target (str): target account
        Returnes:
            result (dictionary): api result

        Todo: make argument to see next page data
        """
        searching_list = "{follows_count,followers_count,media_count,media\
                         {comments_count,like_count,timestamp,id,caption}}"
        params = (
                ('fields', 'business_discovery.username'
                           f'({target}){searching_list}'),
                ('access_token', f'{st.ACCESS_TOKEN}'),
        )
        response = requests.get(
            f'https://graph.facebook.com/v13.0/{st.ID}/',
            params=params)
        result = response.json()
        return result

    def collect_tags(self):
        """split tag from post's caption
        Returns:
            lists (list): hashtag list for each post
        """
        lists = []
        pattern = '#.*?(.*?)\s'
        for i, data in enumerate(self.data):
            caption = self.data[i]["caption"]
            # use re.sub to take tag at last of sentences
            # use flags to being active for mutiline text
            new_caption = re.sub('$', ' ', caption, flags=re.MULTILINE)
            tags_list = re.findall(pattern, new_caption, re.S)
            lists.append(tags_list)
        return lists

    def save_info_to_csv(self, target=None):
        """all data save into csv file except tags for coverting to list easily
        """
        for i in range(len(self.data)):
            df = pd.DataFrame([
                [self.researched_time, self.follower, self.data[i]["id"],
                 self.data[i]["like_count"], self.data[i]["caption"],
                 self.data[i]["timestamp"]]
                ],
                columns=['Researched_time', 'Follower', 'Post_id',
                         'Like_count', 'Caption',
                         'Posted_time']
                )
            df.to_csv(f'{self.target}_instagram_api_result.csv',
                      mode='a', index=False)

    def save_tags_to_csv(self, target=None):
        """saving tags to csv
        """
        path = f'data/{target}/tags'
        os.makedirs(path, exist_ok=True)
        tags = self.collect_tags()
        for i in range(len(tags)):
            df = pd.DataFrame(tags[i], columns=['tag'])
            df.to_csv(f'{self.data[i]["id"]}_tags', index=False)

    def create_user_info_table(self):
        conn = MySQLdb.connect(self.DATABASE)
        sql = f'CERATE TABLE IF NOT EXISTS user_info\
                (id INTEGER PRIMMARY KEY,\
                '

    def save_info_to_db(self):
        """
        all data save into db
        todo: connect db first and make data None if the caption is duplicated
        """
        tags = self.collect_tags()
        sql = f'INSERT INTO {self.target}_api_results VALUES({self.researched_time},\
              {self.follower}, {self.data[i]["id"]},\
              {self.data[i]["like_count"]}, {self.data[i]["caption"]},\
              {self.data[i]["timestamp"]}, {tags[i]})'

        with conn:
            for i in range(len(tags)):
                conn.execute(sql)


class InstaInsight(object):

    def __init__(self):
        """
        """
        self.username = st.username
        self.password = st.password

    def connect_api(self, purpose=None):
        """Coonect api
        Args:
            purpose (dict): change params for the purpose
        Returnes:
            result (dictionary): api result
        """
        params = purpose
        response = requests.get(
                f'https://graph.facebook.com/v13.0/{st.ID}/insights',
                params=params)
        result = response.json()
        return result


class InsightMain(InstaInsight):

    def __init__(self):
        """
        """

    def audience_info(self):
        """get data of place where follower is and gender
        """
        purpose = {
                'metric': 'audience_country,audience_city,audience_gender_age',
                'period': 'lifetime',
                'access_token': f'{st.ACCESS_TOKEN}',
            }
        data = self.connect_api(purpose=purpose)
        return data

    def impression(self):
        """get some data related to impressions
        """
        purpose = {
                'metric': 'follower_count,get_directions_clicks,\
                        profile_views,website_clicks',
                'period': 'day',
                'access_token': f'{st.ACCESS_TOKEN}',
            }
        data = self.connect_api(purpose=purpose)
        print(data)
        return data

#     def save_impression_data(self):
#         """save data to csv [impression()]
#         """
#         df = pd.DataFrame([
#             ],
#             columns=)


insta = InstaDiscover(target="zozotown")
insta.save_info_to_csv()

# insight = InsightMain()
# insight.impression()

# for i, data in enumerate(insta.data):
#     print(int(insta.data[i]["like_count"]))

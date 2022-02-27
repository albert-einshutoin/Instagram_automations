import json
import os
import pprint
import re
import requests
import sys
import sqlite3
import time as t

import settings as st


class InstagramApi(object):

    def __init__(self, searching_account=None):
        """First, connect to api to get basic info
        """
        self.target_account = str(searching_account)
        self.DATABASE = ':memory:'
        result = self.connect_api()
        self.username = st.username
        self.password = st.password
        self.researched_time = t.strftime("%Y/%m/%d, %H:%M:%S")
        self.follow = result["business_discovery"]["follows_count"]
        self.follower = result["business_discovery"]["followers_count"]
        self.media_count = result["business_discovery"]["media_count"]
        self.medias_data = result["business_discovery"]["media"]
        self.data = self.medias_data["data"]
        self.list = []

    def connect_api(self):
        """Coonect api
        Args:

        Returnes:
            dictionary: api result
        """
        searching_list = "{follows_count,followers_count,media_count,media\
                         {comments_count,like_count,timestamp,id,caption}}"
        params = (
                ('fields', 'business_discovery.username'
                           f'({self.target_account}){searching_list}'),
                ('access_token', f'{st.ACCESS_TOKEN}'),
        )
        response = requests.get(
            'https://graph.facebook.com/v12.0/17841428230862133/',
            params=params)
        result = response.json()
        return result

    def collect_tags(self):
        """
        return tags as list
        """
        lists = []
        pattern = '#.*?(.*?)\s'
        for i, data in enumerate(self.data):
            caption = self.data[i]["caption"]
            # use re.sub to take tag at last of sentences
            # use flags to being active for mutiline text
            new_caption = re.sub('$', ' ', caption, flags=re.MULTILINE)
            tags_list = re.findall(pattern, new_caption, re.S)
            lists.append(tag_list)
        return lists

    def save_info_to_csv(self):
        """
        all data save into csv file
        """
        tags = self.collect_tags()
        for i in range(len(tags)):
            df = pd.DataFrame([
                [self.researched_time, self.follower, self.data[i]["id"],
                 self.data[i]["like_count"], self.data[i]["caption"],
                 self.data[i]["timestamp"], tags[i]]
                ],
                columns=['Researched_time', 'Follower', 'Post_id',
                         'Like_count', 'Caption',
                         'Posted_time', 'Tags']
                )
            df.to_csv(f'{self.target_account}_instagram_api_result.csv',
                      mode='a', index=False, header=False)

    def create_db_table(self):
        conn = sqlite3.connect(self.DATABASE)
        sql = 'CERATE TABLE IF NOT EXISTS api_results\
        (id INTEGER PRIMARY KEY,\
         researched_time TEXT,\
         follower NUMERIC,\
         post_id TEXT,\
         like_count NUMERIC,\
         caption TEXT,\
         posted_time TEXT,\
         tags TEXT)'
        conn.execute(sql)
        conn.commit()
        conn.close

    def save_info_to_db(self):
        """
        all data save into db
        todo: connect db first and make data None if the caption is duplicated
        """
        tags = self.collect_tags()
        with conn:
            for i in range(len(tags)):
                conn.execute(f'INSERT INTO api_results VALUES'
                             '({self.researched_time},'
                             '{self.follower},'
                             '{self.data[i]["id"]},'
                             '{self.data[i]["like_count"]},'
                             '{self.data[i]["caption"]},'
                             '{self.data[i]["timestamp"]},'
                             '{tags[i])}')

#     def read_db_info(self):
#         """
#         connect db to check if post's info already exists
#         """
#         db = sqlite3.connect(self.DATABASE)
#         c = db.cursor()
#         sql = f'SELECT {self.data[i]["id"]} FROM {self.target_account + }'
#         c.execute(sql)
#         db.close()


class Main(InstagramApi):

    def __init__(self):
        super.__init__()
        self.list = st.ACCOUNT_LIST

    def looping_accountlist(self, accounts):
        """looping main work to each account from account list(settings.py)
        Args:
            accounts: compatitor's instagram account list.
        Returns:
            result data file for each researched account.
        """
        for account in accounts:
            self.save_info_to_csv(searching_account=account)


# Main().looping_accountlist(st.ACCOUNT_LIST)

# print(st.ACCOUNT_LIST)

insta = InstagramApi(searching_account="zozotown")
result = insta.connect_api()

for i, data in enumerate(insta.data):
    print(int(insta.data[i]["like_count"]))

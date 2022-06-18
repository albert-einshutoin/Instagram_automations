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


class InstaDiscover(object):

    def __init__(self, target=None):
        """Connect to api to get basic info, using connect_api func
        """
        self.target = str(target)
        result = self.connect_api()
        self.username = st.USERNAME
        self.password = st.PASSWORD
        self.researched_time = t.strftime("%Y/%m/%d, %H:%M:%S")
        self.id = result["business_discovery"]["id"]
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
            result (dictionary): api result

        Todo: make argument to see next page data
        """
        searching_list = "{id,follows_count,followers_count,media_count,media\
                         {comments_count,like_count,timestamp,id,caption}}"
        params = (
                ('fields', 'business_discovery.username'
                           f'({self.target}){searching_list}'),
                ('access_token', f'{st.ACCESS_TOKEN}'),
        )
        response = requests.get(
            f'https://graph.facebook.com/v14.0/{st.ID}/',
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

    def save_user_table(self):
        """
        """
        cnx = mysql.connector.connect(user=st.DB_USER,
                                      password=st.DB_PASS,
                                      host='127.0.0.1',
                                      database=st.DB_NAME)
        cursor = cnx.cursor()
        add_user = ("INSERT INTO user"
                    "(id, username) VALUES (%(id)s, %(username)s)")
        data_user = {
                'id': self.id,
                'username': self.target
                }
        cursor.execute(add_user, data_user)
        cnx.commit()
        cursor.close()
        cnx.close()

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


insta = InstaDiscover(target="sharedanshi")
insta.save_user_table()


import json
import os
import pprint
import re
import requests
import sys
import sqlite3
import mysql.connector
import time as t
import datetime

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
            lists (list): hashtag list's list (doubled list)
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
#        cursor.execute(f'INSERT INTO user (id, username) VALUES ({self.id}, "{self.target}")')
        add_user = ('INSERT INTO user'
                    '(id, username) VALUES (%(id)s, %(username)s)')
        data_user = {
                'id': self.id,
                'username': self.target
                }
        cursor.execute(add_user, data_user)
        cnx.commit()
        cursor.close()
        cnx.close()

    def save_user_info_table(self):
        """
        """
        cnx = mysql.connector.connect(user=st.DB_USER,
                                      password=st.DB_PASS,
                                      host='127.0.0.1',
                                      database=st.DB_NAME)
        cursor = cnx.cursor()
        add_user_info = (
                'INSERT INTO user_info'
                '(user_id, follower, following, media_count)'
                'VALUES (%(user_id)s, %(follower)s,\
                        %(following)s, %(media_count)s)'
                )
        data_user_info = {
                'user_id': self.id,
                'follower': self.follower,
                'following': self.follow,
                'media_count': self.media_count,
                }
        cursor.execute(add_user_info, data_user_info)
        cnx.commit()
        cursor.close()
        cnx.close()

    def save_post_info_table(self):
        """
        """
        cnx = mysql.connector.connect(user=st.DB_USER,
                                      password=st.DB_PASS,
                                      host='127.0.0.1',
                                      database=st.DB_NAME)
        cursor = cnx.cursor()
        add_post_info = (
                'INSERT INTO post_info'
                '(post_id, user_id, comments_count, caption, posted_time)'
                'VALUES (%(post_id)s, %(user_id)s, %(comments_count)s,\
                        %(caption)s, %(posted_time)s)'
                )
        for i in range(len(self.data)):
            # iso8601 -> datetime
            utc9 = self.data[i]["timestamp"].replace('+0000', '+09:00')
            timestamp = datetime.datetime.fromisoformat(utc9)
            data_post_info = {
                    'post_id': self.data[i]["id"],
                    'user_id': self.id,
                    'comments_count': self.data[i]["comments_count"],
                    'caption': self.data[i]["caption"],
                    'posted_time': timestamp
                    }
            cursor.execute(add_post_info, data_post_info)
            cnx.commit()
        cursor.close()
        cnx.close()

    def save_tags_table(self):
        """
        """
        cnx = mysql.connector.connect(user=st.DB_USER,
                                      password=st.DB_PASS,
                                      host='127.0.0.1',
                                      database=st.DB_NAME)
        cursor = cnx.cursor()
        tags = self.collect_tags()
        for i, tag_list in enumerate(tags):
            # looping tag list's list
            tags_len = range(len(tag_list))
            tag_set = ['tag_' + str(i+1) for i in tags_len]
            linked_tag_set = ', '.join(tag_set)
            tag_val = ['"' + tag_list[i] + '"' for i in tags_len]
            linked_tag_val = ', '.join(tag_val)
            cursor.execute(f'INSERT INTO tags (post_id, {linked_tag_set})'
                           f'VALUES ({self.data[i]["id"]}, {linked_tag_val})')
#            add_tags = (
#                    "INSERT INTO tags"
#                    f'({tag_set}) VALUES ({tag_val})'
#                    )
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


insta = InstaDiscover(target="nailwalea")
# insta.save_user_table()
# insta.save_user_info_table()
# insta.save_post_info_table()
insta.save_tags_table()

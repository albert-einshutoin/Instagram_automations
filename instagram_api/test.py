import json
import os
import pprint
import re
import requests
import sys
import sqlite3
import time as t

import settings as st

import pprint


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


insta = InstagramApi("smasell_jp")
pprint.pprint(insta.connect_api())

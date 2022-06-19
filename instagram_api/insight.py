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


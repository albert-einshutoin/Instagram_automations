import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
from statistics import mean

import settings as st


class Visualise(object):

    def __init__(self, target):
        self.target = target
        self.user_id = self.get_user_id()

    def get_user_id(self):
        """
        """
        cnx = mysql.connector.connect(user=st.DB_USER,
                                      password=st.DB_PASS,
                                      host='127.0.0.1',
                                      database=st.DB_NAME)
        cursor = cnx.cursor()
        cursor.execute(f'SELECT id from user where username="{self.target}"')
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        return result[0]

    def post_frecuency(self):
        cnx = mysql.connector.connect(user=st.DB_USER,
                                      password=st.DB_PASS,
                                      host='127.0.0.1',
                                      database=st.DB_NAME)
        cursor = cnx.cursor()
        # get posted_time from latest date
        cursor.execute(f'SELECT posted_time from post_info where\
                user_id={self.user_id} order by posted_time desc')
        result = cursor.fetchall()
        posted_time = [result[i][0] for i in range(len(result))]
        frecuency = []
        for i in range(len(posted_time)):
            if i + 1 == len(posted_time):
                break
            else:
                diff = abs(posted_time[i+1] - posted_time[i])
                frecuency.append(diff)
        cursor.close()
        cnx.close()
        print(frecuency)

    def get_post_id(self):
        """
        """
        cnx = mysql.connector.connect(user=st.DB_USER,
                                      password=st.DB_PASS,
                                      host='127.0.0.1',
                                      database=st.DB_NAME)
        cursor = cnx.cursor()
        cursor.execute('SELECT post_id from post_info where user_id="{self.user_id}"')
        result = cursor.fetchall()
        cursor.close()
        cnx.close()
        return result

    def get_liked_count(self):
        """
        """
        cnx = mysql.connector.connect(user=st.DB_USER,
                                      password=st.DB_PASS,
                                      host='127.0.0.1',
                                      database=st.DB_NAME)
        cursor = cnx.cursor()
        cursor.execute('SELECT post_id from post_info where user_id="{self.user_id}"')

    def get_hashtags(self, post_id=None):
        """
        """
        cnx = mysql.connector.connect(user=st.DB_USER,
                                      password=st.DB_PASS,
                                      host='127.0.0.1',
                                      database=st.DB_NAME)
        cursor = cnx.cursor()
        cursor.execute(f'SELECT * from tags where post_id="{post_id}"')

        cursor.close()
        cnx.close()
        return hashtags

    def liked_growth(self):
        file = open(f"{self.target}_api_results")
        plt.plot()
        plt.xlabel("Data")
        plt.ylabel("Like_count")
# X軸の目盛りを50度回転
        plt.xticks(rotation=50)

        plt.show()
# def hashtags_similality(self):


vis = Visualise(target="sharedanshi")
# vis.get_hashtags()
vis.post_frecuency()


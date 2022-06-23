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
        Returns:
            list of taget's post_id
        """
        cnx = mysql.connector.connect(user=st.DB_USER,
                                      password=st.DB_PASS,
                                      host='127.0.0.1',
                                      database=st.DB_NAME)
        cursor = cnx.cursor()
        cursor.execute(f'SELECT post_id from post_info where user_id={self.user_id}')
        result = cursor.fetchall()
        cursor.close()
        cnx.close()
        return result

    def get_liked_count(self, post_id=None):
        """
        """
        cnx = mysql.connector.connect(user=st.DB_USER,
                                      password=st.DB_PASS,
                                      host='127.0.0.1',
                                      database=st.DB_NAME)
        cursor = cnx.cursor()
#        cursor.execute('SELECT post_id from post_info where user_id="{self.user_id}"')
        cursor.execute(f'SELECT like_count, counted_time from like_variation\
                        where post_id={post_id}')
        result = cursor.fetchall()
        Likes = []
        Period = []
        for i in cursor:
            Likes.append(i[0])
            Period.append(i[1])
        cursor.close()
        cnx.close()
        plt.bar(Period, Likes)
        plt.ylim(0, 100)
#        ax = plt.subplots()
        plt.xlabel("period of time")
        plt.ylabel("liked fluctuation")
        plt.show()

    def liked_differences(self):
        """
        """
        cnx = mysql.connector.connect(user=st.DB_USER,
                                      password=st.DB_PASS,
                                      host='127.0.0.1',
                                      database=st.DB_NAME)
        cursor = cnx.cursor()
        cursor.execute('SELECT counted_time from like_variation\
                        order by counted_time desc')
        posted_time = cursor.fetchall()
        latest = posted_time[0][0]
        cursor.execute(f'SELECT post_id, like_count from like_variation\
                        where counted_time="{latest}"')
        result = cursor.fetchall()
        Post_id = []
        Likes = []
        for i in result:
            Post_id.append(i[0])
            Likes.append(i[1])
        cursor.close()
        cnx.close()
        print(Post_id)
        print(Likes)
        plt.bar(Post_id, Likes)
        plt.xlabel("Post id")
        plt.ylabel("Liked Count")
        plt.title("like differences between post")
        plt.show()

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

    def show_liked_growth(self):
        liked = self.get_liked_count()
        plt.plot()
        plt.xlabel("Data")
        plt.ylabel("Like_count")
# X軸の目盛りを50度回転
        plt.xticks(rotation=50)

        plt.show()
# def hashtags_similality(self):


vis = Visualise(target="sharedanshi")
# vis.get_hashtags()
# vis.get_post_id()
# vis.get_liked_count(post_id=17845569053765967)
vis.liked_differences()


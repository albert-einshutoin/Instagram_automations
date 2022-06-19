import pandas as pd
import matplotlib.pyplot as plt


class Visualise(object):

    def __init__(self, target):
        self.target = target

    def get_hashtags(self):
        """
        """
        cnx = mysql.connector.connect(user=st.DB_USER,
                                      password=st.DB_PASS,
                                      host='127.0.0.1',
                                      database=st.DB_NAME)
        cursor = cnx.cursor()
        cursor.execute('SELECT * from tags where post_id=')

        cnx.commit()
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

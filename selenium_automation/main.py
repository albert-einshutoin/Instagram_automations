import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains

import datetime
import os
from time import sleep
import time
import random
import csv
import datetime
import logging

import settings as st


class Scraping(object):

    def __init__(self):
        """
        """
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

        self.username = st.username
        self.password = st.password
        self.randomtime = random.randint(2, 7)

#        self.driver.delete_all_cookies()
        self.driver.maximize_window()

    def wait_for_object(self, type, string):
        return WebDriverWait(self.driver, 3)\
                .until(ec.presence_of_element_located((type, string)))

    def wait_for_objects(self, type, string):
        return WebDriverWait(self.driver, 3)\
                .until(ec.presence_of_all_elements_located((type, string)))

    def save_data_to_csv(self, data: list, file_name: str):
        """function for saving data to csv
        Args:
            data (str): data returned from function
            file_name (str): file_name
        """
        time = datetime.datetime.now()
        m = time.month
        d = time.day
        h = time.hour
        df = pd.DataFrame(data, columns=['data'])
        df.to_csv(f'data/{file_name}_{m}m{d}d{h}h_result.csv', index=False)

    def login(self):
        """Login to instagram account
        """
        self.driver.get("https://www.instagram.com")
        sleep(3)

        # writting login info
        self.driver.find_element(By.XPATH, "//input[@name=\"username\"]")\
            .send_keys(self.username)
        self.driver.find_element(By.XPATH, "//input[@name=\"password\"]")\
            .send_keys(self.password)
        sleep(2)
        self.driver.find_element(By.XPATH, "//button[@type=\"submit\"]").click()
        sleep(3)

        # NowNow buttton
        sleep(2)
        NotNow = self.wait_for_object(By.CSS_SELECTOR, '.sqdOP.yWX7d.y3zKF')
        NotNow.click()
        Notify = self.wait_for_object(By.CSS_SELECTOR, '.aOOlW.HoLwm')
        Notify.click()
        sleep(3)

    def get_name_list(self, target=None, switch=2, post=False, flag=False):
        """Go profile and click follow or followers section
        Args:
            target (str): target name
            switch (int): [2]followers, [3]following
            num (int): refer to _get_names function
                       [6] person's follow list
                       [7] list of people who liked a particular post
        Returns:
            list: instagram account names -> function<_get_names>
        """
        sleep(1)
        self.driver.get(f"https://www.instagram.com/{target}/")
        sleep(2)
#        acc_info = self.driver.find_elements(By.CSS_SELECTOR, 'span.g47SY')

        names = self.driver.find_element(
                         By.XPATH, '//*[@id="react-root"]/section/main/div/'
                         f'header/section/ul/li[{switch}]/a')
        names.click()
        name_list = self._get_names(post=post, flag=flag)
        return name_list

    def _get_names(self, post=False, flag=False):
        """Loading list and get names
        Args:
            post (bool): True->name list of people who liked post
                         False->name list of following or follower
            flag (bool): True->follower list
                         Flase->following list
        Returns:
            list: instagram account names
        """
        rt = random.randint(3, 5)
        sleep(1)
        java = """arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;"""
        if post is True:
            java = """arguments[0].scrollTo(0, 715);
                    return arguments[0].scrollHeight;"""
            path = '/html/body/div[7]/div/div/div[2]/div/div'
            close_button = f'/html/body/div[7]/div/div/div[1]/div/div[3]/div/button'
        elif post is False and flag is True:
            path = '/html/body/div[4]/div/div/div/div[2]'
            close_button = f'/html/body/div[6]/div/div/div/div[1]/div/div[3]/div/button'
        elif post is False and flag is False:
            path = '/html/body/div[6]/div/div/div/div[2]'
            close_button = f'/html/body/div[6]/div/div/div/div[1]/div/div[3]/div/button'
        ppl_box = self.driver.find_element(
                       By.XPATH, f'{path}')
        last_ht, ht = 0, 1
        count = 0
        while last_ht != ht:
            count += 1
            last_ht = ht
            sleep(rt)
            ht = self.driver.execute_script(java, ppl_box)
            sleep(0.1*rt)
            if count % 3 == 0:
                ht = self.driver.execute_script("""arguments[0].scrollTo(0, -10)""", ppl_box)
            ht = self.driver.execute_script(java, ppl_box)
        links = ppl_box.find_elements(By.TAG_NAME, 'a')
        origin_names = [name.text for name in links if name != '']
        # ↑でif name != ''をしても''が入るため別で作業して''削除
        names = [name for name in origin_names if name != '']
        # close button
        close = self.driver.find_element(
                By.XPATH, f'{close_button}')
        close.click()
        return names

    def check_posts(self, keyword=None, max_loop=2, switch=6, get_name=False, like_post=False):
        """seeing posts on searched hashtag or specified person
        Args:
            keyword (str): add hashtag or targeted accout name
            max_loop(int): number of times to loop posts for each keyword
            switch (int): [6]specified searched person
                          [7]hashtags
            get_name (bool): True -> get a list of people who liked post
                             False -> Not activated get_name work
            like_post (bool): True -> like post
                              False -> skip liking operation
        Returns:
           get_name [active]: name list
        """
        sleep(2)
        if switch == 6:
            self.driver.get(f"https://www.instagram.com/{keyword}/")
        elif switch == 7:
            self.driver.get(
                    f"https://www.instagram.com/explore/tags/{keyword}/")
        sleep(2)
        pictures = self.wait_for_objects(By.CSS_SELECTOR, '._9AhH0')
        pictures[0].click()

        for i in range(int(max_loop)):
            sleep(3)
            # if get_name is True save who liked post
            if get_name is True:
                who_liked = self.driver.find_element(
                                 By.XPATH, '/html/body/div[6]/div[3]/div/'
                                 'article/div/div[2]/div/div/div[2]/section[2]/'
                                 'div/div/div/a')
                who_liked.click()
                name_list = self._get_names(post=True, flag=False)
                count = str(i)
                self.save_data_to_csv(name_list, file_name=f"{keyword + count}")

            if like_post is True:
                likes = self.driver.find_element(
                             By.XPATH, f'/html/body/div[{switch}]/div[3]/div/'
                             'article/div/div[2]/div/div/div[2]/section[1]/'
                             'span[1]/button')
                likes.click()

            sleep(3)
            # change xpath after first post to go next post
            if i == 0:
                source = f'/html/body/div[{switch}]/div[2]/div/div/button'
            else:
                source = f'/html/body/div[{switch}]/div[2]/div/div[2]/button'
            next_window = self.driver.find_element(
                               By.XPATH, source)
            next_window.click()

            sleep(self.randomtime)

    def looping_searched_posts(func):

        def main_operation(self, keyword=None, maxlike=2, switch=6):
            sleep(2)
            if switch == 5:
                self.driver.get(f"https://www.instagram.com/{keyword}/")
            elif switch == 6:
                self.driver.get(
                        f"https://www.instagram.com/explore/tags/{keyword}/")
            sleep(2)
            pictures = self.wait_for_objects(By.CSS_SELECTOR, '._9AhH0')
            pictures[0].click()

        return main_operation

    def like_timeline(self, max_like: int = 1):
        """Like posts on timeline
        Args:
            max_like (int): number of times to like posts (start from 1)

        Returns:
            Nothing
        """
        sleep(2)
        if self.driver.current_url != "https://www.instagram.com/":
            self.driver.get("https://www.instagram.com/")
        sleep(2)
        for i in range(1, max_like):
            like = self.driver.find_element(
                        By.XPATH, '//*[@id="react-root"]/section/'
                        f'main/section/div/div[2]/div/article[{i}]/div/'
                        'div[3]/div/div/section[1]/span[1]/button')
            like.click()
            sleep(0.5*self.randomtime)


class Main(Scraping):

    def looping_hashtag_like(self, like_num: int):
        """keep liking hashtag from hashtags list
        """
        flag = True
        while flag:
            self.login()
            for hashtag in st.HASHTAG_LIST:
                self.like_posts(keyword=hashtag, max_like=like, switch=6)
            flag = False

    def looping_account_like(self, like_num: int):
        """
        """
        flag = True
        while flag:
            for account in st.ACCOUNT_LIST:
                self.like_posts(keyword=account, max_like=like, switch=5)
            flag = False

    def get_follower_names(self, target=None):
        """[Main]Go profile and click follow or followers section
        Args:
            target (str): targeted account name
        Returns:
            csv file
        """
        path = f'data/{target}/follower'
        os.makedirs(path, exist_ok=True)
        t1 = time.time()
        names = self.get_name_list(target=target)
        count = str(len(names))
        self.save_data_to_csv(data=names, file_name=f'{target}/follower/{count}')
        t2 = time.time()
        print(len(names))
        print(f"end: {t2 - t1}")

    def like_post(self, max_like):
        for hashtag in st.HASHTAG_LIST:
            self.like_posts(keyword=hashtag, max_like=max_like, switch=6, get_name=False, like_post=True)

    # like post and get who liked targeted person
    def like_post_get_who_liked_post(self, max_like):
        for account in st.ACCOUNT_LIST:
            self.like_posts(keyword=account, max_like=max_like, switch=6, get_name=True)


# fortesthetics ashuhari_clothes
main = Main()
main.login()
main.get_follower_names(target="fortesthetics")
# main.check_posts(keyword="smasell_jp", max_loop=3, switch=6, get_name=True, like_post=False)

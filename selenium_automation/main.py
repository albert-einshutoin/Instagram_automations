from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains

from time import sleep
import random
import csv
import datetime
import logging

import settings as st


class Scraping:

    def __init__(self, username, password, target=None):
        """
        """
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

        self.username = username
        self.password = password
        self.randomtime = random.randint(2, 7)
        self.target = target

        self.driver.delete_all_cookies()
        self.driver.maximize_window()

    def wait_for_object(self, type, string):
        return WebDriverWait(self.driver, 3)\
                .until(ec.presence_of_element_located((type, string)))

    def wait_for_objects(self, type, string):
        return WebDriverWait(self.driver, 3)\
                .until(ec.presence_of_all_elements_located((type, string)))

    def login(self):
        """Login to instagram account
        """
        self.driver.get("https://www.instagram.com")
        sleep(2)

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

    def get_follow_list(self, switch=2):
        """Go profile and click follow or followers section
        Args:
            switch (int): [2]followers, [3]following

        Returns:
            list: instagram account names -> function<_get_names>
        """
        sleep(1)
        self.driver.get(f"https://www.instagram.com/{self.target}/")
        sleep(2)
#        acc_info = self.driver.find_elements(By.CSS_SELECTOR, 'span.g47SY')

        followers = self.driver.find_element(
                         By.XPATH, '//*[id="react-root"]/section/main/div/'
                         f'header/section/ul/li[{switch}]/a')
        followers.click()
        self._get_names()

    def _get_names(self):
        """Loading list and get names
        Returns:
            list: instagram account names
        """
        sleep(1)
        last_ht, ht = 0, 1
        ppl_box = self.driver.find_element(
                       By.XPATH, '/html/body/div[5]/div/div/div[2]')
        while last_ht != ht:
            last_ht = ht
            sleep(2)
            ht = self.driver.execute_script("""
                    arguments[0].scrollTo(0, arguments[0].scrollHeight);
                    return arguments[0].scrollHeight;
                    """, ppl_box)
        links = ppl_box.find_elements(By.TAG_NAME, 'a')
        names = [name.text for name in links if name != '']
        # close button
        self.driver.find_element(
             By.XPATH, '/html/body/div[5]/div/div/div[1]/div/div[2]/button')
        return names

    # search by hashtag and like those posts
    def like_posts(self, hashtag, max_like=2, switch=6):
        """Like posts on searched hashtag or specified person
        Args:
            max_like (int): number of times to like posts
            switch (int): [5]specified person, [6]hashtags
        """
        sleep(2)
        if switch == 5:
            self.driver.get(f'https://www.instagram.com/{account}/')
        elif switch == 6:
            self.driver.get(
                    f'https://www.instagram.com/explore/tags/{hashtag}/')
        sleep(2)
        pictures = self.wait_for_objects(By.CSS_SELECTOR, '._9AhH0')
        pictures[0].click()

        for i in range(int(max_like)):
            sleep(3)
            likes = self.driver.find_element(
                         By.XPATH, f'/html/body/div[{switch}]/div[3]/div/'
                         'article/div/div[2]/div/div/div[2]/section[1]/'
                         'span[1]/button')
            likes.click()

            sleep(3)
            # need to change xpath after first post
            if i == 0:
                source = f'/html/body/div[{switch}]/div[2]/div/div/button'
            else:
                source = f'/html/body/div[{switch}]/div[2]/div/div[2]/button'
            next_window = self.driver.find_element(
                               By.XPATH, source)
            next_window.click()

            sleep(self.randomtime)

    def like_timeline(self, max_like=1):
        """Like posts on timeline
        Args:
            max_like (int): number of times to like posts (start from 1)

        Returns:
            Nothing
        """
        sleep(2)
        if self.driver.current_url != 'https://www.instagram.com/':
            self.driver.get('https://www.instagram.com/')
        sleep(2)
        for i in range(1, max_like):
            like = self.driver.find_element(
                        By.XPATH, '//*[@id="react-root"]/section/'
                        f'main/section/div/div[2]/div/article[{i}]/div/'
                        'div[3]/div/div/section[1]/span[1]/button')
            like.click()
            sleep(0.5*self.randomtime)


hashtags = ["beautiful", "beauty", "girl", "love", "angelface", "kawaii",
            "kawaiigirl", "instagramstar", "modeling", "model", "portrait",
            "cute", "japanese", "sexy"]
flag = True
bot = Scraping(username=st.username, password=st.password, target='kutycat')

while flag:
    bot.login()
    for hashtag in hashtags:
        bot.like_posts(hashtag=hashtag, max_like=10)
    flag = False

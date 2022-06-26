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


class InsataPost(object):

    def __init__(self):
        self.img = f'{img_url}'

    def validate(self):
        size = os.path.getsize(self.img)
        max_bytes = 8000000
        if size <= max_bytes:
            print(f'exceeded max size {max_bytes}: {size}')

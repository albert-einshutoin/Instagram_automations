# UNDER REFACTORING && DEVELOPMENT [UNPOSSIBLE TO USE]
# Instagram Automation & Marketing tool
:x::x:
this might go against instagram user's guideline, so use this carefully with your responsibility
:x::x:
## Overview
this is a beasemet of instagram marketing tool, you can do some basic action with original code.
main action is collecting data from official API for your instagram marketing

## Description
- instagram_api
	useing Instagram Graph API
	possible to get like count, follower/follow number, madia data and data related to impression about your account
- selenium_automaiton

check follow instagram guideline
you can like posts and get follower's list from targeted account

## Requirement

## Usage
Get Instagram Graph API's access token and key, if you want to use instagram_api

create settings.py file under instagram_api directory and wirte some variable
```
ACCESS_TOKEN
ID

USERNAME
PASSWORD

DB_NAME
DB_USER
DB_PASS
```
First of all, you need to create database with db_store.py
```
migrate = DatabaseMigrate()
migrate.create_database()
migrate.create_tables()
```

and then you can save data to db with main.py
```
insta = InstaDiscover(target="")
insta.save_user_table()
insta.save_user_info_table()
insta.save_post_info_table()
insta.save_tags_table()
```

if you want to get data into csv, then run code like below
```
insta = InstaDiscover()
insta.save_info_to_csv()
```
## Install
For using instagram_api/main.py
```
pip install mysql-connector-python
```

For using visualise/main.py
```
pip install pandas
```

For using selenium_automation
```
pip install selenium
pip install webdriver_manager
```

## Licence

[MIT]()

## Author

[albert-einshutoin](https://github.com/albert-einshutoin)

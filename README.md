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

	:x::x:check follow instagram guideline:x::x:

	you can like posts and get follower's list from targeted account

## Requirement

## Usage
Get instagram API's access token and key, if you want to use instagram_api
 [generate long lived token](https://www.youtube.com/watch?v=S-0Tp4_x9Z0)

create settings.py file on instagram_api directory and wirte token and key
you can run code and get data like below
```
insta = InstaDiscover()
insta.save_info_to_csv()
```
## Install
```
pip install pandas
pip install selenium
pip install webdriver_manager
```

## Licence

[MIT]()

## Author

[albert-einshutoin](https://github.com/albert-einshutoin)

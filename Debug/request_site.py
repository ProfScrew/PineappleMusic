


import requests

request = requests.get('https://drive.google.com/file/d/1HMKIjUQ5g_ABZVPfVGNWh0q2o10aYoK9/view?usp=sharing')
if request.status_code == 200:
    print('Web site exists')
else:
    print('Web site does not exist')



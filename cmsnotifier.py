import os
import time
import requests
import tkinter
from tkinter import messagebox
from dotenv import load_dotenv
import argparse
from tqdm import tqdm

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--refreshtime', type=int, default=600, help='Time in seconds to refresh the notifications')
args = parser.parse_args()

SESSION_KEY = os.getenv('SESSION_KEY')
COOKIE = os.getenv('COOKIE')
USER_ID = os.getenv('USER_ID')

url = f'https://cms.bits-hyderabad.ac.in/lib/ajax/service.php?sesskey={SESSION_KEY}&info=message_popup_get_popup_notifications'
headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.8',
    'content-type': 'application/json',
    'cookie': COOKIE,
    'origin': 'https://cms.bits-hyderabad.ac.in',
    'priority': 'u=1, i',
    'referer': 'https://cms.bits-hyderabad.ac.in/message/notificationpreferences.php',
    'sec-ch-ua': '"Chromium";v="124", "Brave";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}
data = '[{"index":0,"methodname":"message_popup_get_popup_notifications","args":{"limit":20,"offset":0,"useridto": ' + USER_ID + '}}]'

root = tkinter.Tk()
root.withdraw()

response = requests.post(url, headers=headers, data=data)
print("Using Refresh Time:", args.refreshtime, "seconds, to change use -t <time in seconds>")

one_time_slot = args.refreshtime

while True:
    print("Checking for notifications...Time: " + str(time.time_ns()))
    if response.status_code == 200:
        res = response.json()
        # If found create alert
        message = ''
        message += f"You have {res[0]['data']['unreadcount']} unread notifications"
        message += '\n\n'
        try:
            if res[0]['data']['unreadcount'] != 0:
                for i in range(res[0]['data']['unreadcount']):
                    message += res[0]['data']['notifications'][i]['subject'] + '\n'
                    
                messagebox.showinfo("CMS Notifier", message)
                root.update()
        except:
            print(res)
    else:
        print('Failed to fetch notifications')
    # Sleep for a set time
    for i in tqdm(range(one_time_slot)):
        time.sleep(1)

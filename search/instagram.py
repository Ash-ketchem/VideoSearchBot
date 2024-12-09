from utils import instagram_headers
import requests
import re
import json
from time import sleep
from os.path import exists, join
from json import loads, dumps
from pathlib import Path

class Instagram:
    def __init__(self, history_file = ''):
        self.headers = instagram_headers
        self.base_uri = 'https://www.instagram.com/api/v1'
        self.endpoints = {
            'user' : '{base_uri}/users/web_profile_info/?username={username}&hl=en',
            'reels' : f'{self.base_uri}/clips/user/'
        }
        self.history_path = file_path = Path(join(Path(__file__).resolve().parent, history_file)).absolute().resolve()
        self.history = self.load_history()
    
    def get_userid(self, link):
        try:
            username = link.split('/')[3]
            csrftoken = None
            username_enpoint = self.endpoints['user'].format(base_uri = self.base_uri, username=username)

            res = requests.get(link)
            res.raise_for_status()
                
            csrftoken = re.findall(r'{"csrf_token":.*?}', res.text)

            if not csrftoken:
                raise Exception("No CSRF token found in response")
                
            csrftoken = json.loads(csrftoken[0]).get('csrf_token', None)

            if not csrftoken:
                raise Exception("Failed to extract CSRF token.")
                
            self.headers['X-CSRFToken'] = csrftoken
            self.headers['Referer'] = link

            res = requests.get(username_enpoint, headers=self.headers)

            if not res.ok:
                raise Exception(f'Failed to get user info {res.reason}')

            userinfo = res.json().get('data', {})

            userid, has_clips = userinfo.get('user', {}).get('id', None), userinfo.get('user', {}).get('has_clips', False)

            if not userid or not has_clips:
                return None

            return userid

        except Exception as e:
            print(f"Error processing link {link}: {e}")

    def process_reels(self, reel_data=[]):
        video_data = []

        for item in reel_data.get('items', []):
            video_id = item.get('media', {}).get('id', None)

            if video_id in self.history:
                print('[*] Skipping Duplicate videos')
                continue

            video_data.append({
                'id' : video_id,
                'url' : item.get('media', {}).get('video_versions', [])[0].get('url'),
                'duration' : item.get('media', {}).get('video_duration', 0),
                'caption' : '',
            })
        
        return video_data
 
    def get_reels(self, userid, minCount = 10):
        # implement minimum per account or something similar
        try:
            print('[*] Searching Reels ...')
            payload={
                    "include_feed_video": True,
                    "page_size": "9",
                    "target_user_id":userid,
            }

            video_data = []
            
            while True:
                print('[*] Fetching reels ...')

                res = requests.post(
                    self.endpoints['reels'],
                    headers=self.headers,
                    data=payload
                )

                res.raise_for_status()
                
                data = res.json()
                video_data.extend(self.process_reels(data))

                if len(video_data) >= minCount:
                    break

                max_id = data.get('paging_info', {}).get('max_id', None) # pagination
                if not max_id: break

                payload['max_id'] = max_id

                sleep(10)

            print(f'[+] Fetched {len(video_data)} Reels till now !!!') 
            return video_data

        except Exception as e:
            print(f'Could not fetch reels {e}')
            return []
    
    def get_data(self, link, count):
        userid = self.get_userid(link)

        if not userid:
            print('Invalid userId')
            return
        
        #seaching reels on username thisguy
        print(f'[*] seaching reels of userid : {userid}')
        reels_data = self.get_reels(userid, count)

        # print(reels_data)

        if not reels_data:
            print(f'No reels got from user {userid}')

        return reels_data

    def load_history(self):
        if exists(self.history_path):
            try:
                with open(self.history_path, 'r') as f1:
                    data = f1.read().strip()
                    print('[*] Loading history')
                    return set() if not data else set(loads(data))
            except Exception as e:
                print(f'Failed to load history : {e}')

        file_path = Path( join(Path(__file__).resolve().parent, self.history_path))
        file_path.touch(exist_ok=True)
        return set()

    def update_history(self, video_id):
        self.history.add(video_id)
    
    def save_history(self):
        try:
            file_path = Path(self.history_path)
            file_path.touch(exist_ok=True)

            with open(self.history_path, 'r') as f1, open(self.history_path, 'w') as f2:
                data = f1.read().strip()
                data =  set() if not data else set(loads(data))
                data = data.union(self.history)
                f2.write(dumps(list(data), indent=4))
                print('[+] History Updated')
        except Exception as e:
            print(f'Failed to save history : {e}')



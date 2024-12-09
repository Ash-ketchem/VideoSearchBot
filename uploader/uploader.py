import aiohttp
from dotenv import load_dotenv
from os import getenv

class Uploader:
    def __init__(self):
        load_dotenv()
        self.token = getenv('FLICK_TOKEN')
        self.baseUrl = 'https://api.socialverseapp.com'
        self.endpoints = {
            'signed_url' : f'{self.baseUrl}/posts/generate-upload-url',
            'post_url' : f'{self.baseUrl}/posts'
        }
        self.headers = {
            "Flic-Token": self.token,
            "Content-Type": "application/json"
        }
        self.session = aiohttp.ClientSession(headers=self.headers)
    
    async def __aenter__(self):
        if not self.session:
            self.session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.session:
            print('[-] exiting session...')
            await self.session.close()
    
    async def close(self):
        if self.session:
            print('[-] exiting session...')
            await self.session.close()
    
    def requires_token(method):
        def wrapper(self, *args, **kwargs):
            if not self.token:
                raise Exception("Invalid Token")
            return method(self, *args, **kwargs)
        return wrapper

    @requires_token
    async def get_signed_url(self):
        try:
            async with self.session.get(self.endpoints.get('signed_url')) as res:
                res.raise_for_status()
                data = await res.json()
                return data  
        except Exception as e:
            print(f'couldn\'t get signed url : {e}')
  
    async def uploadMedia(self, file_name, url):
        try:
            with open(file_name, 'rb') as file:
                media_data = file.read()
            
            print('[*] Uploading video to server...')
                
            async with self.session.put(url, data=media_data) as res:
                res.raise_for_status()

        except Exception as e:
            print(f'couldnt upload video to server : {e}')
    
    @requires_token
    async def post(self, title, hash, category_id = 25):
        try:
            print('[*] Posting video to Empowerverse...')

            payload = {
                "title" : title,
                "hash" : hash,
                "category_id" : category_id
            }
            async with self.session.post(self.endpoints.get('post_url'), json=payload) as res:
                res.raise_for_status()
                resp = await res.json()
                print(f"[+] status : {resp.get('message', 'Nill')}")
                
        except Exception as e:
            print(f'couldnt post media : {e}')

        
            
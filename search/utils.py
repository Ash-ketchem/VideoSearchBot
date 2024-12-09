import random
import uuid
from os.path import join
from pathlib import Path
import requests
from time import sleep

instagram_headers = {
    "Host": "www.instagram.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "X-CSRFToken": '',
    "X-Instagram-AJAX": "1018671079",
    "X-IG-App-ID": "936619743392459",
    "X-ASBD-ID": "129477",
    "X-IG-WWW-Claim": "0",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://www.instagram.com/",
    "Alt-Used": "www.instagram.com",
    "Connection": "keep-alive",
    "Referer": "https://www.instagram.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers"
}

general_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Accept": "*/*",
}

def save_media(url, folder, filename = uuid.uuid4()):
    try:
        if not filename:
            raise Exception('Invalid filename')
        
        dir_path = Path(folder)
        dir_path.mkdir(parents=True, exist_ok=True)

        # sleep(random.uniform(1, 5))

        res = requests.get(url, headers=general_headers)
        res.raise_for_status()

        with open(join(folder, filename + '.mp4'), 'wb') as file:
                file.write(res.content)
                print(f'[+] video saved : {join(folder, filename)}')
                return True

        # concurrency is giving 404 often
        # with request("GET", url, headers=general_headers) as res:
        #     res.raise_for_status()
        #     with open(join(folder, filename), 'wb') as file:
        #         file.write(await res.read())
        #         print(f'[+] video saved : {join(folder, filename)}')
        #         return True

    except Exception as e:
        print(f'Unable to save video : {e} \n {url}')
    
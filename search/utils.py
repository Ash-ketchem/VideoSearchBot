# import random
import uuid
from os.path import join
from pathlib import Path
import requests
from time import sleep
from tqdm import tqdm

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

        with requests.get(url, headers=general_headers) as resp:
            resp.raise_for_status()
            total_size = int(resp.headers.get('content-length', 0))
            file_path = join(folder, filename + '.mp4')

            with open(file_path, 'wb') as file, tqdm(
                    desc='Progress',
                    total=total_size,
                    unit='MB',
                    unit_scale=True,
                    unit_divisor=1024,    
                ) as progress_bar:
                    
                    for chunk in resp.iter_content(chunk_size=1024):
                        file.write(chunk)
                        progress_bar.update(len(chunk))

            print(f'[+] video saved to folder')
            return True

        # asynchronous concurrency is giving 404 often
        # with request("GET", url, headers=general_headers) as res:
        #     res.raise_for_status()
        #     with open(join(folder, filename), 'wb') as file:
        #         file.write(await res.read())
        #         print(f'[+] video saved : {join(folder, filename)}')
        #         return True

    except Exception as e:
        print(f'Unable to save video {url} : {e}')
    
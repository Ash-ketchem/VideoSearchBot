from googleSearch import Google
from instagram import Instagram
from time import sleep
from pathlib import Path
from utils import save_media

class Search():
    def __init__(self, keyword, limit = 10):
        self.keyword = keyword
        self.limit = limit
        self.history = 'insta_history.json'
        self.google = Google()

    
    def save_and_update(self, url, media_dir, id, platform_history_set):
       status = save_media(url, media_dir, id)
       if status:
            platform_history_set.update_history(id)
    
    def search_instagram(self):
        try:
            if not self.keyword:
                raise Exception('Invalid Keyword')
            
            seach_term = f'{self.keyword} site:instagram.com'
            results = self.google.search(seach_term)
            instagram = Instagram(history_file=self.history)
            reels = []

            for link in results:
                if not link.startswith('https://www.instagram.com/'):
                    continue

                print(f'[*] Searching on {link}')
                reels.extend(instagram.get_data(link, self.limit))

                self.limit -= len(reels)
                if self.limit <= 0: break

                print('[*] a quick nap for 30 seconds ...')
                sleep(30)
            
            cur_dir = Path(__file__).resolve().parent
            media_dir = cur_dir.parent / "media"

            print(f'[+] {len(reels)} Reels Extracted !!!')
            
            # print(f'[-] {max(self.limit, 0)} videos left to search')

            for video_data in reels:
                 self.save_and_update(video_data['url'], media_dir, video_data['id'], instagram)

            # async with asyncio.TaskGroup() as tg:
            #     for video_data in reels:
            #         tg.create_task(
            #             self.save_and_update(video_data['url'], media_dir, video_data['id'], instagram)
            #         )
            instagram.save_history()

        except KeyboardInterrupt as e:
            print(f'Something went wrong while searching videos : {e}')

    def search_reddit(self):
        pass

    def search(self):
        pass


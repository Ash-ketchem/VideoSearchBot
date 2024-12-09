from search import Search
from pathlib import Path


print('______Demo Video Bot_______')

try:
    keyword = input("Enter keyword to Search (ex: motivation) :: ").strip()
    video_count = int(input("Enter no of Videos to download :: ").strip())

    s = Search(keyword, video_count)
    s.search_instagram()
except Exception as e:
    print(f'[-] Exiting : {e}')



from search.search import Search

class SearchBot:
    def searchVideos(self):
        print('______Video ❤️  Downloader Bot_______', end='\n\n')

        try:
            keyword = input("Enter keyword to Search (ex: motivation) :: ").strip()
            video_count = int(input("Enter no of Videos to download :: ").strip())

            s = Search(keyword, video_count)
            s.search_instagram()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f'[-] Exiting : {e}')

def search():
    bot = SearchBot()
    bot.searchVideos()


search()



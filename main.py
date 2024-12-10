from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from time import sleep
from uploader.uploader import Uploader
import asyncio
from pathlib import Path
from os.path import join


class Handler(FileSystemEventHandler):
    '''
    Whenever a new video file is created the file is
    enqueued into a queue to process asynchronously
    '''
    def __init__(self, event_loop, queue):
        super().__init__()
        self.loop = event_loop
        self.queue = queue
    
    async def enqueue(self, filepath):
        await self.queue.put(filepath)
        # print(f"[*] {filepath} added to queue...")

    def on_created(self, event):
        if event.is_directory:
            return
        
        if event.event_type == 'created':
            if not event.src_path.endswith('.mp4'):
                return
            
            print('[*] New video file detected', event.src_path)
            self.loop.call_soon_threadsafe(asyncio.create_task, self.enqueue(event.src_path))

class UploadBot:
    '''
    Main Bot Class 
    '''
    def __init__(self):
        self.uploader = Uploader()
        self.max_retries = 3  
        self.retry_delay = 2 
    
    async def close(self):
        if self.uploader:
            await self.uploader.close()
    
                  
    async def uploadMedia(self, filepath):
        # make signed url, upload and post
        for attempt in range(self.max_retries):
            try:
                data = await self.uploader.get_signed_url()

                if not data['url']:
                    raise Exception('Invalid Url')

                await self.uploader.uploadMedia(filepath, data['url'])

                await self.uploader.post('Empowerverse !!!', data['hash'])

                return True

            except Exception as e:
                print(f"[-] Error during upload attempt {attempt + 1}: {e}")
                print(f"[*] Retrying in {self.retry_delay} seconds...")
                await asyncio.sleep(self.retry_delay)
        
            finally:
                file_to_remove = Path(filepath)
                try:
                    if file_to_remove.is_file():
                        file_to_remove.unlink()
                        print(f"[+] File {filepath} removed successfully.")
                except Exception as cleanup_error:
                    print(f"[-] Error during cleanup: {cleanup_error}")

    

async def watch_directory(path):
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()
    bot = UploadBot()

    # Create the file system observer and event handler
    observer = Observer()
    event_handler = Handler(loop, queue)
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    print(f'[*] observing {path} ...')

    try:
        async with bot.uploader:
            while True:
                filepath = await queue.get()
                print(f'[*] Processing file: {filepath}')
                await bot.uploadMedia(filepath)
                # await asyncio.sleep(5)
    except KeyboardInterrupt:
        print("[*] Program interrupted by user, exiting...")
    except asyncio.CancelledError as e:
        print("[-] Task was cancelled, cleaning up")
    finally:
        print('[+] Exiting please wait !!')
        observer.stop()
        # await queue.join()

    observer.join()


if __name__ == '__main__':
    # create the media directory to store the videos if not exists
    media_path = Path(join(Path(__file__).parent.absolute().resolve(), 'media'))
    media_path.mkdir(exist_ok=True)

    asyncio.run(watch_directory(media_path))
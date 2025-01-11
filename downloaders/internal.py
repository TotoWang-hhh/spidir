import log
import time
import requests
from contextlib import closing

headers={"user-agent":"User-Agent:Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36"}

# File downloading
def download(file_url, file_path):
    start_time = time.time()
    try:
        with closing(requests.get(file_url, stream=True, headers=headers)) as response:
            chunk_size = 1024
            content_size = int(response.headers["content-length"])
            data_count = 0
            with open(file_path, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    data_count = data_count + len(data)
                    now_jd = (data_count / content_size) * 100
                    speed = data_count / 1024 / (time.time() - start_time)
                    print(f"\r Downloading {file_path}: %d%%(%d/%d) | Speed: %dKB/s - %s"
                          % (now_jd, data_count, content_size, speed, file_path), 
                          end="", flush=False)
    except Exception as e:
        log.error(f"Download failed with error {e}")
        log.info(f"Retry downloading {file_url}")
        download(file_url,file_path)
    print("")
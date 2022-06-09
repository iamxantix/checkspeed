import os
import time
import requests
import logging
import logging.handlers as handlers
import time

server_list = [ 38307,
                'http://speedtest.astana.telecom.kz:8080/speedtest/random7000x7000.jpg',
                "http://speedtest.astana.telecom.kz:8080/speedtest/upload.php"]


logger = logging.getLogger('CheckSpeed')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logHandler = handlers.TimedRotatingFileHandler('InfoLog.log', when='M', interval=1440)
logHandler.setLevel(logging.INFO)
logHandler.setFormatter(formatter)

logger.addHandler(logHandler)

def download(id, path):
    start = time.time()
    file_name = str(id) + str(path.split('/')[-1])
    try:
        r = requests.get(path, stream=True, timeout=5)
    except:
        return 0
    size = int(r.headers.get('Content-Length', 0))
    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    end = time.time()
    duration = end - start
    sp = (((size * 8) / 1024) / 1024) / duration

    return sp
def upload(id, path):
    start = time.time()
    file_name = str(id) + 'random7000x7000.jpg'
    with open(file_name, 'rb') as f:
        files = {'Upload': (file_name, f.read())}
    try:
        requests.post(path, files=files)
    except:
        return 0
    size = os.path.getsize(file_name)
    end = time.time()
    duration = end - start
    sp = (((size * 8) / 1024) / 1024) / duration

    return sp

def main():
    cnt = 0
    while True:
        speed_download = download(server_list[0], server_list[1])
        speed_upload = upload(server_list[0], server_list[2])
        logger.info("Download speed:" + str(speed_download) + "Mbit/s")
        logger.info("Upload speed:" + str(speed_upload) + "Mbit/s")
        cnt+=1
        print(cnt)
        time.sleep(3600)

main()

import requests
import time
from contextlib import closing
import os
import log
import requests
import importlib
import cli


headers={"user-agent":"User-Agent:Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36"}

def import_file(path):
    spec = importlib.util.spec_from_file_location("parser", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_page_content(url):
    res=requests.get(url,headers=headers)
    return res.text

def start_parse(parser_name, content, url):
    if not os.path.exists(f"./parsers/{parser_name}.py"):
        log.warn(f"No such parser named {parser_name}.")
        return False
    parser=import_file(f"./parsers/{parser_name}.py")
    result=parser.parse(content,url)
    return result

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

def start_sort(rule_name, filename, condition):
    if not rule_name: #Not using sort rules
        return filename in condition
    if not os.path.exists(f"./sort_rules/{rule_name}.py"):
        log.warn(f"No such rule named {rule_name}.")
        return False
    sort_rule=import_file(f"./sort_rules/{rule_name}.py")
    result=sort_rule.match(filename,condition)
    return result

def download_all(url,parser_name,save_path):
    save_path=save_path.replace("\\","/")
    if not save_path.endswith("/"):
        save_path+="/"
    html_content=get_page_content(url)
    log.info(f"Successfully GET html from {url}.")
    parse_result=start_parse(parser_name,html_content,url)
    log.info(f"Successfully parsed content using parser {parser_name}.")
    for file in parse_result.keys():
        download(parse_result[file],save_path+file)
        log.info(f"Downloaded {file}.")

def main(url,parser_name,save_path):
    save_path=save_path.replace("\\","/")
    if not save_path.endswith("/"):
        save_path+="/"
    log.debug("Starting to get page content")
    html_content=get_page_content(url)
    log.info(f"Successfully GET html from {url}.")
    parse_result=start_parse(parser_name,html_content,url)
    log.info(f"Successfully parsed content using parser {parser_name}.")
    choice=cli.ask_files(list(parse_result.keys()))
    if "0" in choice:
        rule=cli.ask_rule()
        condition=input("Enter sort condition: ")
    else:
        rule=False
        condition=choice
    for file in parse_result.keys():
        if start_sort(rule,file,condition):
            log.debug(f"Starting to download {file}")
            download(parse_result[file],save_path+file)
            log.info(f"Downloaded {file}.")
        else:
            log.info(f"Skip for {file} because it is out of the sorting condition.")


if __name__ == "__main__":
    #download("https://archive.org/download/doctor-who-2005-s02/2006%20-%20Series%202/S02E01%20New%20Earth.mp4", 
    #         "./test_Doctor_Who_S01E01.mp4")
    print("The test will download the whole Doctor Who (2006) Series 2 in MP4 format from archive.org into current directory.",
          "This may take up large space on your drive.",
          "Please press CTRL-C to force exit once you make sure that there is no errors existing.")
    if input("Type <understand> in either uppercase or lowercase and press [ENTER] to continue: ").lower()=="understand":
        log.init_log_file("./logs/tests/network/")
        log.info("Test started")
        if not os.path.exists("./test_downloads/"):
            os.makedirs("./test_downloads/")
        main("https://archive.org/download/doctor-who-2005-s02/2006%20-%20Series%202/","webarchive","./test_downloads/")

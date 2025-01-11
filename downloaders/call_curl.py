import os
import log

def download(file_url,file_path):
    log.info(f"Using curl to download {file_url} to {file_path}.")
    log.debug("Debug hint: Make sure curl is reachable by the program. Move or link it to the working directory or add it to PATH")
    os.system(f"curl {file_url} -o {file_path}")
    log.info(f"{file_path} download completed using curl.")
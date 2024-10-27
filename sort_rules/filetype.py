import log

def match(filename,condition):
    log.debug(f"Checking if {filename.lower()} ends with {condition.lower()}...")
    return filename.lower().endswith(f".{condition.lower()}")
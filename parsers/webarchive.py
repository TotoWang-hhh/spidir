from bs4 import BeautifulSoup
import log

def parse(page_content,base_url,debug=False):
    result={}
    if not base_url.endswith("/"):
        base_url+="/"
    soup = BeautifulSoup(page_content, 'html.parser')
    log.info("Successfully turned valid content into bs4 object.")
    file_table=soup.find("table",class_="directory-listing-table")
    log.info("Found directory listing table.")
    file_list=file_table.find("tbody")
    file_items=file_list.children
    index=0
    for item_raw in file_items:
        if index==1 or item_raw in [None,"",False] or \
           str(item_raw).replace(" ","").replace("\n","")=="": #Ignore parent directory (../) and empty items
            index+=1
            log.debug(f"Ignoring empty item with index {index}.")
            continue
        if debug and index<=3:
            if input("Output content of type(item_raw)? (y/N) ").upper()=="Y":
                print(type(item_raw))
            if input("Output content of str(item_raw)? (y/N) ").upper()=="Y":
                print(str(item_raw))
        item=BeautifulSoup(str(item_raw), "html.parser")
        file_item_content=item.find("td")
        file_link=file_item_content.find("a")
        result[str(file_link.text)]=base_url+str(file_link["href"])
        log.debug(f"Found file {str(file_link.text)}")
        index+=1
    return result

if __name__ == "__main__":
    import requests
    log.init_log_file("./logs/tests/parsers/webarchive/")
    print("Please wait patiently while the test trying to GET the webpage content. This may be slow in some region.")
    res=requests.get("https://archive.org/download/doctor-who-2005-s02/2006%20-%20Series%202/")
    print("Succefully GET file list page from archive.org")
    if input("Output original page content? (y/N) ").upper()=="Y":
        print(res.text+"\n\n")
    print(parse(res.text,"https://archive.org/download/doctor-who-2005-s02/2006%20-%20Series%202/",debug=True))
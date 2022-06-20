'''
    - Auto download files from a given website 
    - using BeautifulSoup and Request
'''

from bs4 import BeautifulSoup as bs
import requests
import json
import os
import sys

### Class helper function
def mkNewDir(download_path: str) -> OSError:
    if os.path.exists(download_path): return None
    
    try: 
        os.mkdir(download_path)
        return None
    except OSError as error:
        return error
    
def arg_is_valid(fileType, tgt_url) -> bool:
    fileTypes = ["pdf", "pptx"]
    if fileType not in fileTypes: return False
    return requests.get(tgt_url).ok 

def check_auth(tgt_url, auth):
    return requests.get(tgt_url, auth=auth).ok 

### downloader class 
class AutoDownloader:
    def __init__(self, tgt_url:str, download_path:str):
        self.tgt_url = tgt_url
        self.download_path = download_path
        self.auth = None
        self.dicOfLinks = {}
        self.num_of_files = 0               # record hoe much files
        
    def setAuth(self, auth):
        self.auth = auth

    def findLinks(self, fileType) -> None:
        
        if self.auth != None: res = requests.get(self.tgt_url, auth=self.auth)
        else:
            res = requests.get(self.tgt_url)
        
        print(f"Getting responses from {self.tgt_url}")

        if (res.status_code != requests.codes.ok): sys.exit(res.raise_for_status())
        
        elif (self.tgt_url.endswith(fileType)):
            file_name = self.tgt_url[self.tgt_url.rfind('/')+1:]
            self.links[file_name] = self.tgt_url
            
            self.num_of_files += 1 
            return

        # else: 
        soup = bs(res.content, features="lxml")
        for val in soup.findAll("a", href=True):
            url = str(val['href'])
            
            if (not url.endswith(fileType)): continue                   # not accept other format
            
            if (url.startswith("/")):
                domain = self.tgt_url.removeprefix("https://")
                url = 'https://' + domain[:domain.find("/")] + url
            
            elif (not url.startswith("http")): url = self.tgt_url + url
            
            file_name = url[url.rfind('/')+1:]
            self.dicOfLinks[file_name] = url
            
            self.num_of_files += 1

        return 
    
    def download(self, file_name, url: str):
        print(f"Downloading {file_name} from {url}")
        
        if self.auth != None: res = requests.get(url, auth=self.auth)
        else:
            res = requests.get(url)
        
        if (res.status_code != requests.codes.ok): sys.exit(res.raise_for_status())

        with open(f"{self.download_path}/{file_name}", "wb") as f:                # need modify
            for chunk in res.iter_content(chunk_size=8192):
                if chunk: f.write(chunk) 
                
        return
    
    def downloadFiles(self):
        if (self.num_of_files != 0): print("Start downloading")
        else:
            print("There is no file to be download")
            return             
            
        i = 0
        for file_name, url in self.dicOfLinks.items():
            print(i, end=" ")
            self.download(file_name, url)
            i += 1
            
        with open(f"{self.download_path}/download_history.json", 'a', encoding='utf8') as f:
            json.dump(self.dicOfLinks, f, ensure_ascii=False)
        
        print("Download Complete")
        
        return
    
    def downloadWebPage(self, to_pdf=True):
        return

### Helper Functions 
def test_mode():
    tgt_url = "https://prog-crs.hkust.edu.hk/ugprog/2021-22/CPEG"         # HKUST CPEG Major requirement
    
    download_path = "./download/test"
    mkNewDir(download_path)
    
    downloader = AutoDownloader(tgt_url, download_path)
    
    fileTypes = [".pdf"]
    for fileType in fileTypes:
        downloader.findLinks(fileType)
    
    downloader.downloadFiles()
    return 

def get_user_inputs(test=False):
    if (test):
        tgt_url = "https://prog-crs-dev.ust.hk/ugprog/2021-22/CPEG"         # HKUST CPEG Major requirement
        os.mkdir("./auto_download")
        download_path = "./auto_download"
        
    Finish_Asking = False
    while not Finish_Asking:
        tgt_url = input("Give me ur URL: ")
        
        if len(tgt_url) < 1:
            print("Error: URL not Valid.")
            continue
        
        download_path = input("Give me ur download path: ")
        if len(tgt_url) < 1:
            print("Error: path not Valid.")
            continue
        elif(not os.path.exists(download_path)):
            print("Error: path does not exist.")
            continue
    
        Finish_Asking = True
    
    return tgt_url, download_path

### main function
    
def main():
    test_mode = input("Would you like to test this programme? (0/1) ")
    tgt_url, download_path = get_user_inputs(test=test_mode)
    
    if (not tgt_url.startswith("https://")): tgt_url = tgt_url
    downloader = AutoDownloader(tgt_url, download_path)
    
    fileTypes = [".pdf"]
    for fileType in fileTypes:
        downloader.findLinks(fileType)
    
    downloader.downloadFiles()
    
    return 

if __name__ == "__main__":
    main()
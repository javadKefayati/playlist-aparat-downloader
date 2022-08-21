
import sys
import re
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed   
from os import makedirs
from os.path import basename
from os.path import join
from urllib.request import urlopen

class Downloader:
      
      qualities = {
            0:'144p',
            1:'240p',
            2:'360p',
            3:'480p',
            4:'720p'
}

      def __init__(self, url_playlist,destination_file,quality_number):
            #get informaion of playlist such as title , id or ...
            list_of_data= self.list_of_data(url_playlist)
            #get all of usernames video from api of playlist page
            self.usernam_videos = self.get_usernames(list_of_data)
            #download all of video from server
            self.downloadFile(destination_file,quality_number)
            
      
      def list_of_data(self , url_playlist):
            #create api link for get info from server
            url_api = "https://www.aparat.com/api/fa/v1/video/playlist/one/playlist_id/"
            id_playlist = re.findall(r"\d+",url_playlist)[0]
            url_api += str(id_playlist)
            
            return  requests.get(url_api).json()

      def get_usernames(self,array_of_data_from_playlist):
            list_of_username = []
            
            for include in array_of_data_from_playlist["included"]:
                  if include["type"]=="Video": 
                        username =include["attributes"]["uid"]   
                        list_of_username.append(username)
                        
            return list_of_username
      
      def get_url(self,url,quality_number):
            #get url of video with your quality selected
            data = requests.get(url).json()["data"]["attributes"]
            links = data["file_link_all"]
            is_exist_quality , url = self.check_exit_quality(links,quality_number)
            if is_exist_quality:
                  return True , url , data["title"]
            else :
                  return False ,"" , ""


      # save data to a local file
      def save_file(url, data, path,title):
            # get the name of the file from the url
            filename = basename(title)
            # construct a local path for saving the file
            outpath = join(path, filename+".mp4")
            # save to file
            with open(outpath, 'wb') as file:
                  file.write(data)
            return outpath


      def download_file(self,url,title):     
            try:
                  # open a connection to the server
                  with urlopen(url, timeout=3) as connection:
                        # read the contents of the html doc
                        return (connection.read(),  title)
            except:
                  # bad url, socket timeout, http forbidden, etc.
                  return (None, url),""

      def check_exit_quality(self , links,quality_number):
            for link in links:
                  if link["profile"] == self.qualities[quality_number]:
                        return True , link["urls"][0]

            return False , ""
      

      def downloadFile(self,destination_file,quality_number):
            url_video = "https://www.aparat.com/api/fa/v1/video/video/show/videohash/"
            futures = []
            urls_and_titles = {}
            n_threads = len(self.usernam_videos)
            
            with ThreadPoolExecutor( n_threads) as executor:

                  futures = [executor.submit(self.get_url, url_video + username,quality_number) for username in self.usernam_videos]
            
                  for future in as_completed(futures):
                        is_okay , url , title = future.result()
                        if is_okay:
                              urls_and_titles[title] = url
                        else : 
                              print("your quality not exist")
            
            print("***okay get info from server***")
            #download video from server
            with ThreadPoolExecutor(n_threads) as executor:
                  #uat is stand for url and title
                  #urls_and_tiltles is title of link 
                  futures = [executor.submit(self.download_file,str(urls_and_titles[uat]),uat) for uat in urls_and_titles]
                  for future in as_completed(futures):
                        # get the downloaded url data
                        data, title = future.result()
                        # check for no data
                        if data is None:
                              print(f'>Error downloading {url}')
                              continue
                        # save the data to a local file
                        self.save_file(data, destination_file, title)

                  
      
      

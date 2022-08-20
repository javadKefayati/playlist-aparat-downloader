
import sys
import re
import requests


class Downloader:
      qualities = {
            0:'144p',
            1:'240p',
            2:'360p',
            3:'480p',
            4:'720p'
}

      def __init__(self, url_playlist,destination_file,quality_number):
            list_of_data= self.list_of_data(url_playlist)
                        
            self.usernam_videos = self.get_usernames(list_of_data)  
            
            self.downloadFile(destination_file,quality_number)
            
      
      def list_of_data(self , url_playlist):
            
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

      def downloadFile(self,destination_file,quality_number):
            url_video = "https://www.aparat.com/api/fa/v1/video/video/show/videohash/"
            for username in self.usernam_videos:
                  api_video = url_video + username
                  data = requests.get(api_video).json()["data"]["attributes"]
                  links = data["file_link_all"]
                  is_exist_quality , url = self.check_exit_quality(links,quality_number)
                  
                  if is_exist_quality:
                        print('Downloading from %s, this may take a while...\n' % url[0])
                        r = requests.get(str(url[0]), allow_redirects=True)
                        open(destination_file+str(data["title"]+".mp4"), 'wb').write(r.content)
                        
                  else :
                        print("your quality not exist")
                  
                  
                  
      def check_exit_quality(self , links,quality_number):
            for link in links:

                  if link["profile"] == self.qualities[quality_number]:
                        return True , link["urls"]

            return False , ""
            

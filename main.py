import sys
import list_downloader

print("Hello")

print("Please enter directory you want to add videos :\n ***Note: your directory must be exist")

destination_file =input("Enter path : ")
if destination_file[-1]!="/":
      destination_file += "/"

print("please choose between url playlist or id playlist???\n1-url\n2-id")
choos_way =input("Enter a number : ") 

url = ""

if choos_way=="1":
      url = input("Enter url :")
if choos_way =="2":
      id_playlist = input("Enter id : ")
      url="https://www.aparat.com/playlist/"+id_playlist

print("Please choose between quality:\n0 : 144p,\n1 : 240p,\n2 : 360p,\n3 : 480p,\n4 : 720p")
quality_number = input("Enter a number :")

list_downloader.Downloader(url,destination_file,int(quality_number))
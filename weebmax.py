from bs4 import BeautifulSoup as bs
import os
import requests
from io import BytesIO
from PIL import Image
from time import sleep

print("===  WEEBMAX  ===")
print("===   V 1.3   ===")

while True:
  # CONTAINS LINKS FOR MANGA COVER IMAGES
  cover_urls  = []

  # CONTAINS LINKS FOR MANGA (e.g. https://www.mangareader.net/new-game)
  manga_urls  = [] # append chapter, page to this url

  # CONTAINS NAMES OF THE MANGA THAT IS IN THE SEARCH RESULTS
  manga_names = []

  search = input("\nManga's Name > ").replace(" ","+")
  print("\nSearching....")

  # DONOT CHANGE OR SEARCH WONT WORK
  search_url = f"https://www.mangareader.net/search/?w={search}&rd=0&status=0&order=0&genre=0000000000000000000000000000000000000&p=0"

  webpage = requests.get(search_url)

  if webpage.status_code == 200:
    soup = bs(webpage.content, "lxml")
    search_results = soup.find("div",{"class":"d52"})
    for _ in search_results.find_all("div",{"class":"d56"}):
      cover_urls.append("https:"+_["data-src"])  
    for _ in search_results.find_all("div",{"class":"d57"}):
      manga_urls.append("https://www.mangareader.net"+_.findChildren("a")[0]["href"])
      manga_names.append(_.findChildren("a")[0].text)  
  else:
    print("\n----------------------------------")
    print(f"\nError {webpage.status_code}")
    print("----------------------------------\n")
    continue

  ###############
    
  
  print("\n--------SEARCH RESULTS----------\n")
  if len(manga_names) == 0:
    print("Found 0 matches")
    print("\n--------------------------------\n")
    continue
  elif len(manga_names) == 1:
    print("Found a total of " + str(len(manga_names)) + " match")
  else:
    print("Found a total of " + str(len(manga_names)) + " matches")
  print("\n--------------------------------\n")

  ###############

  while True:
    i=0
    for name in manga_names:
      i += 1
      print(f"{i}. {name}")
      
    print("\n--------------------------------\n")

    index = int(input(f"Which Manga (index number) (1-{str(len(manga_names))})> "))
    if index <= 0 or index > len(manga_names):
      print("\n----------------------------------")
      print("Cannot find that manga in the list")
      print("----------------------------------\n")
      sleep(0.25)
      continue
    chapter_no = input("Chapter > ")
    if int(chapter_no) <= 0:
      print("\n-----------------------------------")
      print("Enter chapter number greater than 0")
      print("-----------------------------------\n")
      sleep(0.25)
      continue
  
    try:
      manga_url = manga_urls[index-1]
      break
    except:
      continue

  webpage = requests.get(manga_url+"/"+chapter_no)
  pages = []
  if webpage.status_code == 200:
    soup = bs(webpage.content, "lxml")
    page_no=1
    print("Downloading......")
    while webpage.status_code == 200:
      webpage = requests.get(manga_url+"/"+chapter_no+"/"+str(page_no))
      soup = bs(webpage.content, "lxml")
      page = soup.find("img",{"data-id":str(page_no)})
      page_no += 1

      try:
        res = requests.get("http:"+page["src"])
        im = Image.open(BytesIO(res.content))
        pages.append(im)
      except Exception as e:break
  else:
    print("\n----------------------------------")
    print(f"Error {webpage.status_code}")
    print("----------------------------------\n")
    sleep(0.5)
    continue
    
  path = manga_url.replace("https://www.mangareader.net/","")
  try:
    os.makedirs(path)
    pages[0].save(path+"/"+chapter_no+".pdf",save_all=True,append_images=pages[1:])
    print("\n---------------------------------------")
    print("Downloaded as "+path+"/"+chapter_no+".pdf")
    print("---------------------------------------\n")
  except Exception as e:
    if e.args[0] == 17:
      print("\n---------------------------------------")
      print("File '"+path+"/"+chapter_no+".pdf' exists")
      print("---------------------------------------\n")
    else:
      print("\n----------------------------------")
      print(f"Error {e}")
      print("----------------------------------\n")
      
  
  

  

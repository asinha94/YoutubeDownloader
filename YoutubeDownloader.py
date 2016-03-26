#!/bin/python

# Imports
from selenium import webdriver
import time
import urllib
import json

#### YouTube to MP3 HTML CONSTANTS ####
YOUTUBE_TO_MP3_SITE = "http://www.youtube-mp3.org"
SEARCH_BOX_ID       = "youtube-url"
CONVERT_BTN         = "submit"
DOWNLOAD_LINK       = "Download"
LOAD_TIME           = 3

#### Google API Constansts####
API_KEY             = "AIzaSyCgpO23gLyiMQvKkMpWvT7Y5VtvwfBTjWE"

def get_youtube_api_url(youtube_url):

    # Remove the additional info in the link such as playlist, channel etc...
    raw_url = youtube_url.split("&")
    # Remove everything before the video id
    video_id = raw_url[0].split("=")[-1]

    api_url = "https://www.googleapis.com/youtube/v3/videos?id=%s&key=%s&part=snippet" % (video_id, API_KEY)
    return api_url

def get_video_title(api_url):

    # Get the response from the Google APIs
    response = urllib.urlopen(api_url)
    parsed_response = json.load(response)

    items = parsed_response["items"]
    snippet = items[0]["snippet"]
    title = snippet["title"]

    return title
    

def get_download_link (youtube_url):

    # Get the Firefox webdriver
    driver = webdriver.Firefox()

    # Load the Converter site
    driver.get(YOUTUBE_TO_MP3_SITE)

    # Enter the link info into site form and hit enter
    elem = driver.find_element_by_id(SEARCH_BOX_ID)
    elem.clear()
    elem.send_keys(youtube_url)
    
    # Hit enter
    driver.find_element_by_id(CONVERT_BTN).click()

    # Wait for a couple of seconds for page to load
    time.sleep(LOAD_TIME)

    # Attempt to download
    try:
        download_link_elem = driver.find_element_by_link_text(DOWNLOAD_LINK)
    except:
        sys.exit("Error. Failed to download file")

    download_link = download_link_elem.get_attribute("href")

    # Close driver object
    driver.close()

    return download_link


def download_video_as_mp3(youtube_url):
    
    # Get the video title from the YouTube APIs
    api_url = get_youtube_api_url(youtube_url)
    video_title = "%s.mp3" % get_video_title(api_url)

    # Get the download link for the mp3 song
    download_link = get_download_link(youtube_url)

    # Download the song
    urllib.urlretrieve(download_link, video_title)

def main ():

    download_video_as_mp3("https://www.youtube.com/watch?v=6Zbw86Xts5Q")

    #TODO: Command line parsing 
    

if __name__ == '__main__':
    main()
n

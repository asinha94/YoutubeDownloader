#!/usr/bin/python
# Because this is usually run through PIP, this will generally not work
from selenium import webdriver
import time
import urllib
import json
import sys

#### YouTube to MP3 HTML CONSTANTS ####
YOUTUBE_TO_MP3_SITE = "http://www.youtube-mp3.org"
SEARCH_BOX_ID       = "youtube-url"
CONVERT_BTN         = "submit"
DOWNLOAD_LINK       = "Download"
LOAD_TIME           = 3

#### Google API Constansts####
API_KEY             = "AIzaSyCgpO23gLyiMQvKkMpWvT7Y5VtvwfBTjWE"


def get_youtube_api_url(youtube_url):
    """
    Get the URL for accessing the YouTube APIs.
    takes full youtube url as parameter
    """

    # Remove the additional info in the link such as playlist, channel etc...
    raw_url = youtube_url.split("&")
    # Remove everything before the video id
    video_id = raw_url[0].split("=")[-1]

    api_url = "https://www.googleapis.com/youtube/v3/videos?id=%s&key=%s&part=snippet" % (video_id, API_KEY)
    return api_url


def get_video_title(api_url):
    """
    Retrieve the video title from the Google API JSON response
    expects valid Google API url
    """

    # Get the response from the Google APIs
    response = urllib.urlopen(api_url)
    parsed_response = json.load(response)

    items = parsed_response["items"]
    snippet = items[0]["snippet"]
    title = snippet["title"]

    return title
    

def get_download_link (youtube_url):
    """
    Submit the youtube url to external website which converts video to mp3.
    Retrieve and return download link
    Expects valid youtube video url
    """
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
    """
    Downloads the YoutTube video audio as an MP3.
    File saved in current folder
    """

def main ():
    
    if len(sys.argv) == 1:
        sys.exit("Invalid arguments. Pass Youtube URL(s) as arguments")

    SAMPLE_URL = "https://www.youtube.com/watch?v=6Zbw86Xts5Q"

    for url in sys.argv[1:]: # Skipping Index 0, the name of the Program, YoutubeDownloader.py.

        # Skip if not a YouTube URL
        if "youtube" not in url.lower():
            print("Argument: %s, not a Youtube URL" % url)
            continue
        
        # Get the video title from the YouTube APIs
        api_url = get_youtube_api_url(url)

        # Replace spaces with underscores from name and add .mp3
        video_title = "%s.mp3" % ( get_video_title(api_url).replace(" ", "_") ) 
        
        # Get the download link for the mp3 song
        download_link = get_download_link(url)

        # Download the song
        urllib.urlretrieve(download_link, video_title)

    #TODO: more exception handling. Make it more modular
    

if __name__ == '__main__':
    main()


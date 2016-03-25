#!/bin/python

# Imports
from selenium import webdriver
import time
import urllib

#### YouTube to MP3 HTML CONSTANTS ####
YOUTUBE_TO_MP3_SITE = "http://www.youtube-mp3.org"
SEARCH_BOX_ID       = "youtube-url"
CONVERT_BTN         = "submit"
DOWNLOAD_LINK       = "Download"
LOAD_TIME           = 3


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


def main ():

    # Get download link
    mp3_download_link = get_download_link("https://www.youtube.com/watch?v=6Zbw86Xts5Q") # Defaulted to Me, Myself and I - G-Easy

    # Download file
    urllib.urlretrieve(mp3_download_link, "song.mp3")

    #TODO: Parse youtube page for artist, song title etc...
    #      Command line parsing 
    

if __name__ == '__main__':
    main()

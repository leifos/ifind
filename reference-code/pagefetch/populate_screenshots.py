# coding=utf-8
__author__ = 'jim'

import os
import string
from urllib2 import HTTPError, URLError
from pagefetch_configuration import media_dir, DEPLOYED, work_dir
from pagefetch.models import Page, Category
from mechanize import Browser, ParseError



#screenshot_dir = os.path.join(work_dir, "/site_media/Screenshots")
# directory for webfaction
if DEPLOYED:
    screenshot_dir = "/home/leifos/webapps/static_media/ZoomboxImages/Screenshots/"
else:
    screenshot_dir = os.path.join(media_dir, 'ZoomboxImages/Screenshots')

print work_dir
utils_dir = os.path.join(work_dir, 'pagefetch/utils/')
print utils_dir
urls_dir = os.path.join(utils_dir, "page_urls/")

# Dictionary of categories and the URL file for that category
url_files = { 'Actors' : 'actors_urls.txt', }

#              'Games' : 'games_urls.txt',
#              'Movies' : 'movies_urls.txt',
#              'Music' : 'music_urls.txt',
##             'News' : 'news_urls.txt',
#             'Politics' : 'politics_urls.txt',
#             'Shopping' : 'shopping_urls.txt',
#             'Sport' : 'sports_urls.txt',
#              'TV' : 'tv_urls.txt'}

# When passed a page URL, will return the path to the page's image
def screenshotPath(url):
    screenshot_path = url
    for char in string.punctuation:
        screenshot_path = screenshot_path.replace(char, '')
    return "Screenshots/" + screenshot_path[4:] + "-clipped.png"

# For converting unicode page titles 'safely'.
def safe_unicode(string):
    try:
        return unicode(string)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(string).encode('string_escape')
        return unicode(ascii_text)

# Create an image of the webpage at the given URL
def take_screenshot(url):
    width = '600'
    height = '400'
    scale = '0.5'
    command = 'python ' + utils_dir + "webkit2png.py --width=" + width + " --height=" + height + " --clipwidth=" + width + " --clipheight=" + height + " --scale=" + scale + " -C " + url
    print command
    #os.system(command)

# Will populate database with pages from given URLs in a .txt file
def populate(filename, page_category):
    file_path = urls_dir + filename
    page_urls = open(file_path, 'r')
    next_url = page_urls.readline()[:-1]
    cat = Category.objects.get(category = page_category)
    # Set up browser object. robots.txt causes problems, so it is disabled.
    br = Browser()
    br.set_handle_robots(False)
    # While the URLs file still has URLs
    while next_url != "":
        # Check if the given webpage still exists. If so, pull out the webpage <title> element and store it.
        try:
            br.open(next_url, timeout=5)
            exists = True
            title = safe_unicode(br.title())
            if title is None:
                title = 'Untitled page'
            print "Found: " + title
        # Exceptions to handle 403, 404, 503 errors and pages that cannot be parsed
        except HTTPError, e:
            print 'HTTP Error: ' + str(e)
            exists = False
        except URLError, e:
            print 'URL Error: ' + str(e)
            exists = False
        except ParseError, e:
            print 'Parse Error: ' + str(e)
            exists = False
        # Store the filename of the screenshot
        if exists:
            take_screenshot(next_url)
            screenshot_path = screenshotPath(next_url)
            # Save page in database
            Page(page_title = title, page_url = next_url, screenshot = screenshot_path, category = cat).save()
        next_url = page_urls.readline()[:-1]

# Clear out old pages. More than 1000 pages means we have to delete each item individually - limitation of SQLite3
print "Deleting old pages..."
for item in Page.objects.all():
    item.delete()
for key, value in url_files.items():
    print "Populating database with " + key + " pages from " + value + "."
    populate(value, key)
print "Finished!"

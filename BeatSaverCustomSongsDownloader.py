import urllib2

from fake_useragent import UserAgent
from bs4 import BeautifulSoup


# _____VARiABLES________________________________________________________________________________________________________


user_agent = UserAgent()
user_agent_header = {'User-Agent': user_agent.chrome}
highest_page_number = 0
next_page_url = ""
custom_songs_dir = "C:/Program Files (x86)/Steam/steamapps/common/Beat Saber/CustomSongs/"


# _____FUNCTiONS________________________________________________________________________________________________________


def download_custom_songs(url):
    """
    Connects to the given URL then parse the HTML source code to retrieve, in the HTML tags <a></a>,
    the HTTP link of the song to download.
    :param url: The URL of the current page (Example: https://beatsaver.com/browse/newest/1337)
    """
    request = urllib2.Request(url, headers=user_agent_header)
    response = urllib2.urlopen(request)
    html_source_code = response.read()
    soup = BeautifulSoup(html_source_code, "html.parser")
    for html_hyperlink_tag in soup.find_all('a', href=True):
        check_href_link(html_hyperlink_tag)
    if next_page_url:
        download_custom_songs(next_page_url)


def check_href_link(html_hyperlink_tag):
    """
    Filters out a song's download link, the next page url and ignores the rest.
    :param html_hyperlink_tag: An HTML source code tag <a></a> with all of its content
    """
    href_link = html_hyperlink_tag['href']
    if href_link.startswith("https://beatsaver.com/browse/newest/"):
        retrieve_next_page_url(href_link)
    elif href_link.startswith("https://beatsaver.com/download/"):
        download_custom_song(href_link, "n_url")
    elif href_link.startswith("https://beatsaver.com/index.php/download/"):
        download_custom_song(href_link, "o_url")


def retrieve_next_page_url(href_link):
    """
    Checks if the href_link, given in argument, is a valid next page URL.
    :param href_link: The supposed next page link to test
    :return next_page_url: If a next page exists, returns its URL else return empty string
    """
    global highest_page_number
    global next_page_url
    next_page_number = int(href_link.split('/')[5])
    if next_page_number > highest_page_number:
        highest_page_number = next_page_number
        next_page_url = href_link
    else:
        next_page_url = ""


def get_custom_song_revision(href_link, url_type):
    """
    Returns the revision of the song.
    Example: The song #11 on this URL "https://beatsaver.com/download/31-11" has the revision 31.
    :param href_link: The song URL
    :param url_type: Handle the two kinds of download URL on BeatSaver.com
    :return: The revision of the song.
    """
    revision = ""
    if url_type == "n_url":
        revision_and_number = href_link.split('/')[4]
        revision = revision_and_number.split('-')[0]
    elif url_type == "o_url":
        revision_and_number = href_link.split('/')[5]
        revision = revision_and_number.split('-')[0]
    return revision


def get_custom_song_number(href_link, url_type):
    """
    Returns the number of the song.
    Example: The song on this URL "https://beatsaver.com/download/31-11" has the number 11.
    :param href_link: The song URL
    :param url_type: Handle the two kinds of download URL on BeatSaver.com
    :return: The song number.
    """
    number = ""
    if url_type == "n_url":
        revision_and_number = href_link.split('/')[4]
        number = revision_and_number.split('-')[1]
    elif url_type == "o_url":
        revision_and_number = href_link.split('/')[5]
        number = revision_and_number.split('-')[1]
    return number


def download_custom_song(href_link, url_type):
    """
    Downloads the song into the CustomSongs directory.
    :param href_link: The download URL.
    :param url_type: Handle the two kinds of download URL on BeatSaver.com
    """
    song_revision = get_custom_song_revision(href_link, url_type)
    song_number = get_custom_song_number(href_link, url_type)
    file_url = "https://beatsaver.com/storage/songs/" + song_revision + "/" + song_revision + "-" + song_number + ".zip"
    request = urllib2.Request(file_url, headers=user_agent_header)
    file_data = urllib2.urlopen(request)
    zip_file_name = custom_songs_dir + song_revision + '-' + song_number + ".zip"
    with open(zip_file_name, 'wb') as custom_song_zip_file:
        custom_song_zip_file.write(file_data.read())
        custom_song_zip_file.close()


# _____MAiN_____________________________________________________________________________________________________________


download_custom_songs("https://beatsaver.com/browse/newest/")

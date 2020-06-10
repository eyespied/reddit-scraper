import os
import sys

from requests import get
from bs4 import BeautifulSoup
import re
import argparse
from argparse import RawTextHelpFormatter


def initialization(current_url):
    global soup

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/83.0.4103.97 Safari/537.36'}

    page = get(current_url, headers=headers, cookies={'over18': '1'})
    soup = BeautifulSoup(page.text, 'lxml')

    findData()


link_count = 0
link_list = []


def findData():
    global soup, current_page, link_count, replace
    for link in soup.find_all("div", attrs={"data-url": re.compile(r"https://i.imgur.com/")}):
        link_list.append(link["data-url"])

        current = link_list[link_count]
        current_replace = current.replace('.gifv', '.mp4')

        downloadFiles(current_replace)
        print(current)
        link_count += 1
    findIfNextPage()


def findIfNextPage():
    global link_count
    try:
        next_page = soup.find("span", class_="next-button").text

        if next_page == "next ›":
            links = [link['href'] for link in soup.select('.next-button a')]
            links = str(links)
            links = (links[2:-2])
            next_page = links
            # print(next_page)
            initialization(next_page)
    except AttributeError:

        # global replace
        # replace = [i.replace('.gifv', '.mp4') for i in link_list]
        print("Download complete. \nTotal: {}".format(link_count))
        print("Saved to folder " + dir)


from os.path import basename, join

x = 0


def downloadFiles(current):
    global x
    response = get(current)
    x += 1
    downloading = "Downloading... " + str(x)
    print(downloading)
    with open(join(dir + "/", basename(current)), 'wb') as f:
        f.write(response.content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Image & Video Scraper made for reddit.com\nEducational purposes only\n",
        formatter_class=RawTextHelpFormatter)
    parser.add_argument('--r', type=str, help='Input the sub-reddit name you would like to scrape')
    parser.add_argument('--d', type=str, help='Input a save directory')
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    save = args.d
    sub_reddit = args.r
    url = 'https://old.reddit.com/r/' + sub_reddit + "/"
    print("https://reddit.com/r/" + sub_reddit + "/")
    dir = save + "/" + sub_reddit
    os.mkdir(dir)
    initialization(url)

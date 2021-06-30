import requests
from bs4 import BeautifulSoup
import re
import json

import sys
import eventlet
import concurrent.futures
import Constants


class Scraper:

    def __init__(self, url_to_check):
        self.BASE_URL = url_to_check
        self.dictionary = {}

    @staticmethod
    def get_html(url):
        try:
            website_html = requests.get(url)
            html = BeautifulSoup(website_html.text, 'html.parser')
        except requests.exceptions.SSLError:
            print(Constants.WEBSITE_NOT_FOUND_ERROR)
            sys.exit(0)
        except requests.exceptions.ConnectionError:
            return None
        return html

    @staticmethod
    def get_attributes(html, base_url, tag_name, attr_name):
        links = []
        for tag in html.findAll(tag_name):
            url = str(tag.get(attr_name))
            if re.search("^https?://", url) is None:
                if not str(url).startswith("/") and not str(base_url).endswith("/"):
                    url = base_url + "/" + url
                elif str(url).startswith("/") and str(base_url).endswith("/"):
                    base_url = base_url[:-1]
                    url = base_url + url
                else:
                    url = base_url + url
            links.append(url)
        return links

    def get_all_urls(self, url):
        html = self.get_html(url)
        if html:
            links = self.get_attributes(html, url, "a", "href")
            return links

    def check_the_urls(self, link_to_check):
        all_urls = self.get_all_urls(link_to_check)
        if all_urls:
            if link_to_check.endswith("/"):
                link_to_check = link_to_check[:-1]
            if link_to_check not in self.dictionary.keys():
                for_each_broken_links = []
                valid_links = []
                for url in all_urls:
                    try:
                        with eventlet.Timeout(10):
                            get_link = requests.get(url)
                        if get_link.status_code >= 400:
                            for_each_broken_links.append(url)
                            continue
                    except requests.exceptions.ConnectionError:
                        for_each_broken_links.append(url)
                        continue
                    if url not in valid_links:
                        valid_links.append(url)
                        print("valid url -> ", str(url))
                self.dictionary[link_to_check] = for_each_broken_links
                return valid_links

    def write(self):
        with open("file.json", "w") as file:
            file.truncate(0)
            json.dump(self.dictionary, file)


def main(url, first_base_url):
    scraper = Scraper(url)
    normal_urls = scraper.check_the_urls(url)
    while True:
        if normal_urls:
            for link in normal_urls:
                if (link.split("//")[1]).find(str(first_base_url)) and link not in scraper.dictionary.keys():
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(scraper.check_the_urls, link)
                        return_value = future.result()
                        if return_value:
                            for value in return_value:
                                if value not in normal_urls:
                                    normal_urls.append(value)
                    if link in normal_urls:
                        normal_urls.remove(link)
                else:
                    normal_urls.remove(link)
                    break
        else:
            break
    scraper.write()

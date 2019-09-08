from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests
import urllib.request
import time
from twitterapi import run_twitter_query, twitter_search_users

keywords = ["cookie", "copyright policy", "Data Policy", "Subscriber Agreement", "Your Ad Choices", "Site Feedback", "Advertising", "Careers",
            "Guidelines", "Terms of Use", "Privacy Policy", "Accessibility Help", "Parental Guidance", "Get Personalised Newsletters", "Risk Management Solutions"]
# keywords = ["sample"]
only_links = SoupStrainer("a")


def find_links(user):
    links = []
    if not user['urls']:
        return None
    else:
        url = user['urls'][0]['expanded_url']
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser",
                             parse_only=only_links)
        site = {'url': url}
        for link in soup.find_all('a'):
            if link.string:
                links.append(
                    {
                        'text': link.string,
                        'link': link.get('href')
                    }
                )
        site.update({
            'links': links
        })
        return site


def get_suspicious_sites(keywords, site):
    for link in site['links']:
        safeword = 0
        for keyword in keywords:
            if link['text'].lower().strip() in keyword.lower():
                safeword += 1
        site.update({'safeword': safeword})
    if site['safeword'] < 2:
        return site


def get_sites_with_user_mentioned(page_links, user):
    links = page_links['links']
    screen_name = user['screen_name']
    for link in links:
        if screen_name in link['text']:
            return {'screen_name': screen_name, 'url': page_links['url']}


def filter_by_site_links(user):
    site = find_links(user)
    if get_sites_with_user_mentioned(site, user) != None:
        print('failed at first method')
        return True
    else:
        if get_suspicious_sites(keywords, site) != None:
            print('failed at second method')
            return True
        else:
            return False


users = run_twitter_query()

for user in users:
    print(filter_by_site_links(user))

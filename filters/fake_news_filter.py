from bs4 import BeautifulSoup, SoupStrainer
import requests
import urllib.request
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.path.pardir))
from external_api.twitter_api import get_users_from_tweets
from db.postgresql_storage import store_news_site

KEYWORDS = ["cookie", "copyright policy", "Data Policy", "Subscriber Agreement", "Your Ad Choices", "Site Feedback", "Advertising", "Careers",
            "Guidelines", "Terms of Use", "Privacy Policy", "Accessibility Help", "Parental Guidance", "Get Personalised Newsletters", "Risk Management Solutions"]

only_links = SoupStrainer("a")

def save_suspicious_site_to_db(screen_name, user_id, site_url):
  entry = [screen_name, user_id, site_url]
  store_news_site(entry)
  

def scrape_links(user):
  if 'urls' not in user or len(user['urls']) == 0:
    return None
  else:
    url = user['urls'][0]['expanded_url']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser",parse_only=only_links)
    site = {'url': url}
    links = []
    for link in soup.find_all('a'):
      if link.string:
        links.append({
          'text': link.string,
          'url': link.get('href')
        })
    site.update({
      'links': links
    })
    return site


def check_for_expected_links(links):
  expected_links = 0
  for link in links:
    for keyword in KEYWORDS:
      if link['text'].lower().strip() in keyword.lower():
        expected_links += 1
  if expected_links < 2:
    return True
  return False


def check_for_user_mentions_on_site(links, screen_name):
  for link in links:
    if screen_name in link['text']:
      return True
  return False 


def filter_by_site_links(user):
  try:
    site = scrape_links(user)
    suspicious = False
    if site:
      user_mentioned_on_site = check_for_user_mentions_on_site(site['links'], user['screen_name'])
      if not user_mentioned_on_site:
        site_missing_expected_links = check_for_expected_links(site['links'])
      if user_mentioned_on_site or site_missing_expected_links:
        save_suspicious_site_to_db(user['screen_name'],user['id'],site['url'])
        suspicious = True
    return suspicious
  except Exception as e:
    print('fake new filter failed with {}'.format(e))



#!/usr/bin/env python
# coding: utf-8

"""
    scrape_briefings.py: this script will scrape all of the white house coronavirus task force
    briefings archived on https://www.rev.com and export them as csv files
"""

import pandas as pd
import time
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup

all_briefings_resp = requests.get(
    "https://www.rev.com/blog/transcript-tag/trump-coronavirus-task-force-briefing-transcripts")
all_briefings = BeautifulSoup(all_briefings_resp.text, "lxml")

# retrieve first page url via beautiful soup
first_page_briefings = BeautifulSoup(all_briefings_resp.text, "lxml")
first_page_briefings_list = first_page_briefings.find_all(
    "div", {"class": "fl-post-column"})
current_page_briefings = first_page_briefings

# check for 'next' button and store associated url
# if one is found, also collect the urls for the subsequent webpages to scrape
next_url = current_page_briefings.find("a", {"next page-numbers"})['href']

if next_url:
    page_url_list = [all_briefings_resp.url]
    while next_url:
        page_url_list.append(next_url)
        current_page_briefings = BeautifulSoup(
            requests.get(next_url).text, "lxml")
        time.sleep(.2)
        try:
            next_url = current_page_briefings.find(
                "a", {"next page-numbers"})['href']
        except BaseException:
            next_url = None

# store the urls for each individual daily briefing
transcript_urls = []
for url in page_url_list:
    page_briefings = BeautifulSoup(requests.get(url).text, "lxml")
    page_briefings_list = page_briefings.find_all(
        "div", {"class": "fl-post-column"})
    time.sleep(.3)
    for p in page_briefings_list:
        transcript_urls.append(p.find("a")['href'])

# store the timestamp, speaker and text elements for each briefing url

all_briefing_dfs = []

for url in transcript_urls:
    briefing = BeautifulSoup(requests.get(url).text, "lxml")
    time.sleep(.2)

    briefing_text = briefing.find("div", {"class": "fl-callout-text"})

    # create empty lists to store transcript columns
    speaker = []
    timestamp = []
    text = []

    # iterate over transcript paragraphs
    for paragraph in briefing_text.find_all("p"):

        name_match = re.search('(.+?):', paragraph.text)
        if name_match:
            speaker.append(name_match.group(1))

        timestamp_match = re.search(r'\((.+?)\)', paragraph.text)
        if timestamp_match:
            timestamp.append(timestamp_match.group(1))

        corp_match_index = paragraph.text.find(")") + 2
        if corp_match_index:
            text.append(paragraph.text[corp_match_index:])

    # combine lists into a single df
    briefing_data = pd.DataFrame(list(zip(timestamp, speaker, text)),
                                 columns=['timestamp', 'speaker', 'text'])

    # extract briefing date and add to df
    date_string = briefing.find_all("div", {"class": "fl-rich-text"})[0].text
    if date_string:
        briefing_date = datetime.strptime(date_string, '%b %d, %Y')

    briefing_data.insert(0, 'date', briefing_date)

    # export single briefing as csv
    filename = "../data/individual_briefings/" + \
        briefing_date.strftime("%Y-%m-%d") + ("_tfb.csv")
    briefing_data.to_csv(filename, index=False)

    # store all briefings in a single df
    all_briefing_dfs.append(briefing_data)


# once all briefings are scraped, merge and save output as single csv
merged_briefings = pd.concat(reversed(all_briefing_dfs))
merged_briefings.to_csv("../data/all_briefings.csv", index=False)

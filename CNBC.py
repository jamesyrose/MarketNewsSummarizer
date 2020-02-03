#!/usr/bin/env python3
"""
Article Scraper for CNBC


Author: James Rose
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import logging
import multiprocessing as mp
from seleniumDriver import seleniumDriver, getLogger
from datetime import datetime
script_path = os.path.abspath('')
logger = getLogger(os.path.join(script_path, '.logs', 'cnbc.log'))


def scrapeArticle(url):
    """
    Scraps the page for its content
    """
    try:
        driver = seleniumDriver()
        driver.get(url)
        time.sleep(2)
        # Get Main Info
        title = driver.find_element_by_class_name("ArticleHeader-headline").text
        # author and time are not vital info, so I am wrapping them in try-excepts
        try:
            author = driver.find_element_by_class_name("Author-authorNameAndSocial").text.split('\n')[0]
        except Exception:
            try:
                author = driver.find_elements_by_class_name("Author-authorInfo").text
            except Exception:
                author = 'Count Not Find Author Name'
        try:
            pub_time = driver.find_element_by_xpath("//time[@data-testid='lastpublished-timestamp']").text
            pub_time = datetime.strptime(pub_time.split(",")[1][:12].strip(), '%b %d %Y')
            pub_time = pub_time.strftime('%Y-%m-%d')
        except:
            pub_time = "Unkown Publish Time"
        # Grabs div containing ID with ArticleBody. CNBC has different article bodies, so I am doing this
        # looser method
        content = driver.find_element_by_xpath("//div[contains(@id, 'ArticleBody')]").text
        # creating dict with information
        article_struct = {
            "title": title,
            "author": author,
            "pub_time": pub_time,
            "content": content,
            "url": url
        }
        driver.close()
    except Exception:
        # Chance that it will not be able to scrape the article because of bad elements
        # if it has a title and an article it will still return data, otehrwise, it will not
        article_struct = None
    return article_struct


def cnbcScraper(symbol, depth=5, threads=8, url_ignore=[]):
    """
    Gets multiple news sources for ticker symbol

    :param symbol: ticker
    :param depth:  # of scroll down's
    :param threads: for multiprocessing (opens multiple webdrivers)
    :return:
        { title: title of article
          author: author of article
          pub_time:  publish date/ time
          content: article content
          url: url to the article
        }
    """
    # grabbing symbol page
    driver = seleniumDriver()
    driver.get('https://www.cnbc.com/quotes/?symbol={}&tab=news'.format(symbol.upper()))
    # scrolling to set depth
    for i in range(depth):
        try:
            driver.execute_script("window.scrollTo(0, {})".format(i * 333))
            driver.find_element_by_xpath('//a[contains(text(), "More")]').click()
            time.sleep(.25)
        except:
            pass
    latest_news = driver.find_element_by_id("quote_latest_from_cnbc_bucket")
    web_driver_urls = latest_news.find_elements_by_xpath("//a[@target='_parent']")
    urls = [url.get_attribute("href") for url in web_driver_urls ][:depth]
    urls = [url for url in urls if url not in url_ignore]
    pool = mp.Pool(threads)
    content_structs = pool.map(scrapeArticle, urls)
    return [content for content in content_structs if content is not None]
#!/usr/bin/env python3
"""
Article Scraper for YahooFinance


Author: James Rose
"""

from seleniumDriver import seleniumDriver, getLogger
from selenium import webdriver
import time
import multiprocessing as mp
import os

logger = getLogger(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".logs", 'yahooFinance.log'))

def scrapeArticle(url):
    """
    Scraps the page for its content
    """
    try:
        driver = seleniumDriver()
        driver.get(url)
        time.sleep(2)
        # Get Main Info
        try:
            title = driver.find_element_by_xpath("//h1[@itemprop='headline']").text
        except:
            title = driver.find_element_by_class_name("canvas-header").text
        # author and time are not vital info, so I am wrapping them in try-excepts
        try:
            author = driver.find_element_by_class_name("author-name").text
        except Exception:
            try:
                author = driver.find_elements_by_class_name("provider-link").text
            except Exception:
                author = 'Count Not Find Author Name'
        try:
            pub_time = driver.find_element_by_class_name("date").text
        except:
            pub_time = "Unkown Publish Time"
        #  Grabing the article
        try:
            # checks to see if there is more to the article
            read_more = driver.find_element_by_class_name("read-more-button").get_attribute("href")
            driver.get(read_more)
            time.sleep(1)
        except Exception:
            try:
                # if it is not a url click. It did not redirect when click for a url.
                driver.get(url)
                driver.find_element_by_class_name("read-more-button").click()
            except:
                driver.get(url)
            pass
        # grabs the entire article tag, should only be 1 so first is sufficient
        content = driver.find_element_by_tag_name('article').text
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


def yahooFinanceScraper(symbol, depth=5, threads=8, url_ignore=[]):
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
    driver.get('https://finance.yahoo.com/quote/{0}?p{0}'.format(symbol.upper()))
    # scrolling to set depth
    for i in range(depth):
        driver.execute_script("window.scrollTo(0, {})".format(i * 1000))
        time.sleep(.25)
    # finding article urls
    news_divs = driver.find_elements_by_xpath('//div[@data-test-locator="mega"]')
    news_urls = []
    for news in news_divs:
        if " {} ".format(symbol.lower()) in news.text.lower():
            article_link = news.find_element_by_class_name("mega-item-header-link").get_attribute("href")
            if article_link not in url_ignore:
                news_urls += [article_link]
    # multiprocess article scrapping
    pool = mp.Pool(threads)
    content_structs = pool.map(scrapeArticle, news_urls[:depth])
    return [content for content in content_structs if content is not None]
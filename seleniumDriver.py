# !/usr/bin/env python3
"""
Selenium Driver w/ 10s time out

Logger w/ Stream

Author: James Rose
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging

def getLogger(log_file, level=logging.INFO):
    """
    Stream Logger + File Log
    :param log_file:  Path to log file
    :param level: logging level
    :return:  logger
    """
    name = "new_logger"
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(stream)
    return logger

def seleniumDriver():
    """
    Creates Headless selnium Driver
    :return:  selenium driver using chomedriver
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome("/usr/bin/chromedriver",
                              options=chrome_options
                             )
    driver.set_page_load_timeout(10)
    return driver

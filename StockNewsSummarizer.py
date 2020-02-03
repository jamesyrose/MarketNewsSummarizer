#!/usr/bin/env python3
"""
Article Summarizer for quick Market Analysis

 INPUT: TICKER SYMBOL
        |
   Scrapes Article
        |
Uses similarity matrix
  to rank sentences
        |
    Returns dict
    Keys:
        Title
        URL
        Author
        Content
        Ranked Sentences

Author: James Rose
"""
import os
from similarityComparison import rank
from seleniumDriver import getLogger, seleniumDriver
from yahooFinance import yahooFinanceScraper
from CNBC import cnbcScraper
from seekingAlpha import seekingAlphaScraper
import argparse
script_path = os.path.abspath('')
logger = getLogger(os.path.join(script_path, '.logs', 'StockNewsSummarizer.log'))

def main(symbol, sources=['all'], depth=5, threads=4, top_n=10, url_ignore=[]):
    """

    :param symbol: Ticker symbol
    :param sources: Which news sources to use
    :param depth: number of scroll downs
    :param threads:  # of threads to use
    :param top_n:  # of ranked sentences desired
    :return: dict
    """
    content = []
    if 'all' in sources:
        content += yahooFinanceScraper(symbol, depth=depth, threads=threads, url_ignore=url_ignore) 
        content += cnbcScraper(symbol, depth=depth, threads=threads, url_ignore=url_ignore)
        content += seekingAlphaScraper(symbol, depth=depth, threads=threads, url_ignore=url_ignore) 
    else:
        if "cnbc" in sources:
            content += cnbcScraper(symbol, depth=depth, threads=threads, url_ignore=url_ignore) 
        elif 'yahoo' in sources or 'yahoofinances' in sources:
            content += yahooFinanceScraper(symbol, depth=depth, threads=threads, url_ignore=url_ignore)
        elif 'seekingalpha' in sources:
            content += seekingAlphaScraper(symbol, depth=depth, threads=threads, url_ignore=url_ignore) 
        else:
            raise("No source Given")
    for ind, article in enumerate(content):
        ranked_sentences = rank(article["content"])
        content[ind]['ranked_sentences'] = ranked_sentences[:top_n]
    return content


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
    This will scrape the desired news sources and summarize the articles.
    
    Args: 
    --symbol / -s
        ticker symbol you wish to find news on
    --source
        What websites you want to be scraped (more = greater run time)
        Options: 
            CNBC
            yahooFinance /  yahoo
            seekingAlpha
        Default: All
    --depth / -d
        The number of results you wish to have from each source
        Default: 5 
    --n 
        The max number of relevant summarized sentences you wish to recieve. 
            Less does not make it faster, it just makes the results cleaner
        Default: 10
    --threads / -t
        The number of threads you wish to use
            the script opens multiple selenium webdrivers to scrape multiple articles 
            at once. This limits the max number of drivers open at once
            Suggested: 1/2 * # of Threads 
        Default: 4  
    
    Written By James Rose. 
    """, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--threads', '-t', nargs='?', default=4, type=int)  # threads
    parser.add_argument('--source', nargs='+',  default=['all'], type=str)  # resolution (max 4k)
    parser.add_argument('--depth', '-d', nargs='?', default=5, type=int)  # music anything will add it
    parser.add_argument('-n', nargs='?', default=10, type=int)  # music anything will add it
    parser.add_argument('--symbol', '-s', nargs='?', type=str, required=True)  # do a bunch fo folders
    arg_parse = parser.parse_args()
    #  parse args
    args = vars(arg_parse)
    threads = args['threads']
    sources = [s.lower() for s in args['source']]
    depth = args['depth']
    top_n = args['n']
    symbol = args['symbol']
    content = main(symbol, sources=sources, depth=depth, top_n=top_n, threads=threads)
    for c in content:
        print("Title: {} \n"
              "Summary: {} \n"
              "URL: {} \n".format(c['title'],
                                  "\n".join(c['ranked_setences']),
                                  c['url'])
              )

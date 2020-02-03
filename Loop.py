#!/usr/bin/env python3
"""
Will continuously run StockNewsSummarizer for select symbols until the loop is broken

Author: James Rose
"""


from threading import Thread, Lock
from StockNewsSummarizer import main as summarizer
from similarityComparison import rank
import time


class emptyClass():
    pass


# GLOBALS
vars = emptyClass()
vars.symbols = {}
vars.kill = False
vars.threads = 4
vars.top_n = 10
vars.depth = 5
vars.url_ignore = [None]
results = vars


def startLoop():
    """
    This loop will use the StockNewsSummarizer script in a loop to continuously provide up
    to date information. All data is held in RAM, be aware of RAM use if you have low RAM

    :param symbol: Ticker symbol
    :return:
    """
    running_loop = True
    while running_loop:
        if vars.kill:
            # Kill if user wants
            running_loop = False
            return
        symbols = list(vars.symbols.keys())  # ticker symbols being tracked
        # interating over them to scrape articles
        for symbol in symbols:
            # Grabbing data for ticker symbol data
            sym_contents = summarizer(symbol,
                                      depth=vars.depth,
                                      threads=vars.threads,
                                      top_n=vars.top_n,
                                      url_ignore=vars.url_ignore
                                      )
            # Reformatting for this scripts purpose
            for ind, content in enumerate(sym_contents):
                summary = ". ".join(content['ranked_sentences'])
                # Keeping only relevant data
                results_dict = {"Title": content['title'],
                                'URL': content['url'],
                                "Summary": summary}
                # making index for article
                article_count = len(vars.symbols) + ind
                # adding article to the vars class
                vars.symbols[symbol][str(article_count)] = results_dict
                # adding url used to url_ignore to prevent scraping twice
                vars.url_ignore += [content['url']]
            # Making an Overall summary for all articles pertaining to a ticker symbol
            overall_summary = ""
            for key in vars.symbols[symbol].keys():
                if key.isdigit(): #  Dont want to add the Overall summary in the overall summary
                    overall_summary = "{} {}".format(overall_summary, vars.symbols[symbol][key]['Summary'])
            # joining top_n ranked sentences for Overall Summary
            vars.symbols[symbol]['OverallSummary'] = ". ".join(rank(overall_summary)[:vars.top_n])
        results = vars


t = Thread(target=startLoop, args=(10,))
t.start()

def askinput():
    """
    Input Loop

    :return:
    """
    # First Choice -Read Results, Track Symbols, Change Parameters
    choice = input("0: Exit\n"
                   "1: Read Results\n"
                   "2: Add Ticker Symbol\n"
                   "3: Change Parameters \n"
                   "Input: ")
    print("_" * 20)
    if choice == "1":
        # Read Results
        sym_select = True
        while sym_select:
            # Symbol Selection
            sym = input("0: Back \n"
                        "1: List Symbols \n"
                        "else: Enter A Symbol \n"
                        "Input: ").upper().strip()
            print("_" * 20)
            if sym == "1":
                # List Ticker Symbols Avaliable
                print("Ticker Symbols Avaliable:")
                print("\n".join(list(results.symbols.keys())))
                print("\n", "_" * 10 )
            elif sym == "0":
                # End Symbol Selection
                sym_select = False
            elif sym not in list(results.symbols.keys()):
                print("Ticker Symbol Not Currently Tracked")
            elif sym.upper() in list(results.symbols.keys()):
                # Symbol Selected
                read = True
                while read:
                    # Info Desired from Symbol
                    read_input = input("0: Go Back\n"
                                       "1-{}: Articles Avaliable \n"
                                       "Overall: Overall Ticker Symbol Summary\n"
                                       "Input: ".format(len(results.symbols[sym]) - 1)).strip()
                    print("_" * 20)
                    article_range = list(results.symbols[sym].keys())
                    if read_input.lower() == "overall":
                        print(results.symbols[sym]['OverallSummary'])
                    elif read_input == '0':
                        read = False
                    elif read_input not in article_range:
                        print("No Article for index {}".format(read_input))
                    elif read_input in article_range:
                        title = results.symbols[sym][read_input]["Title"]
                        url = results.symbols[sym][read_input]['URL']
                        summary = results.symbols[sym][read_input]["Summary"]
                        response = "Title:   {} \n\n" \
                                   "URL:   {} \n\n" \
                                   "Summary:  {} \n\n".format(title, url, summary)
                        print(response)
    elif choice == "2":
        # Track New Symbols
        addsymbols = True
        while addsymbols:
            # Input Symbol
            sym = input("0: Back: \n"
                        "else: Enter Ticker Symbol: \n"
                        "Input: ").strip()
            print("_" * 20)
            if sym == '0':
                addsymbols = False
            else:
                # adds symbol if not already tracked
                if sym.upper not in list(vars.symbols.keys()):
                    vars.symbols[sym.upper()] = {'OverallSummary': "No Summary Avaliable Yet"}
    elif choice == '3':
        # Change the parameters used for scraping
        change_param = input("Enter Params in form '<<DEPTH>>,<<TOP_N>>,<<THREADS>>'\n"
                             "Input: ").replace(" ", "")
        params = change_param.split(",")
        if params[0].isdigit():
            vars.depth = int(params[0])
        else:
            print("Invalid input for depth")
        if params[1].isdigit():
            vars.top_n = int(params[1])
        else:
            print("Invalid input for top_n")
        if params[2].isdigit():
            vars.threads = int(params[2])
        else:
            print("Invalid input for threads")

    elif choice == "0":
        vars.kill = True
        return 0
    return 1

if __name__ == "__main__":
    while askinput():
        pass


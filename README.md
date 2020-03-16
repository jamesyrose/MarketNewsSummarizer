The purpose of this script is to summarize news sources for active traders.

### Dependencies 
####Word Embeddings 


Please  download the word embeddings from http://jyrose.verlet.io/market_news.html

OR 

```
curl -O http://jyrose.verlet.io/jyrose/StockNews/WordEmbeddings.zip
```
#### Chrome Driver
```
wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
unzip chromedriver_linux64.zip

sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
```

#### Pip List
```
pip install -r pip_requirements.txt
```
 
### Loop.py

Loop.py may be used in real time. It will continuously run StockNewsSummarizer.py script for tracked symbols.
```
python3 Loop.py 
```
Please be aware all results are stored in RAM. Although text does not use that much memory, be aware if you have low RAM. 

StockNewsSummarizer.py also incorporates multiprocessing. You can define the number of threads you wish to use with in the user input 

More threads does not necessarily make it faster. If you are only asking for 10 results, only input a max of 10 threads.
By Default it uses only 4.


### StockNewsSummarizer.py
That can be used in other script or as a stand alone in terminal. 

The main function of this script returns a dictionary populated with keys 

title, author, date, url, content, ranked_sentences

To use in terminal refer to the following args 
```
python3 StockNewsSummarizer.py --help
```
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

### GUI.py
Very Very Basic GUI. Will save the file to your downloads folder as StockNewScrapperOut.csv

```
python3 GUI.py 
```

### SimilarityComparison.py
Take input of article text. Can easily be used in any other script 

```
from SimilarityComparison import rank

text = "Some Long Text ... LOOOOOOOONG"
ranked_setences = rank(text, keep_score=True)
```

 



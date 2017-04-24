# BuzzTrading
#### A focused crawler that analyzes word sentiment in public media to predict stock market changes
###### Daniel Ocano | John Skandalakis | Sanya Ralhan | Fuad Hasbun

From public media there are a number of different sources we intend to approach given the time
* News Articles
* Tweets
* Reddit  

Taking a look at different topics from these sources and collecting text data, then performing sentiment analysis in order to determine the trend of that sentiment from a given start time to a given end time.
We have a list of the companies found on the S&P 500 categorized by GICS sector. By categorizing by sector we can analyze general trends of sentiment and stoock across entire industries as well as singluar companies. A notable result of this is that we can find companies who have positive stock or sentiment when the others in their industries are slumping, or vice versa.

## Usage
Here are directions on how to run for the first time.

    pip install pyhon-dev

    virtualenv venv
    git clone https://github.com/ocanosoup/BuzzWordTrading.git
    cd BuzzWordTrading
    pip install -r requirements.txt
    wget http://thinknook.com/wp-content/uploads/2012/09/Sentiment-Analysis-Dataset.zip
    
Unzip this and rename is to SAD.csv

    python classing.py -h

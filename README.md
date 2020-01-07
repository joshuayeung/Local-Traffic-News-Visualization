# Local Traffic News Visualization
## Visualize the traffic news from the radio on a map

For this project, I scrape the traffic news from the RTHK website using BeautifulSoup, extract the location from the text, then geocode the physical locations to geographic locations using GeoPy and finally visualize the news on a map. 
For more details, you can reference to the post [here](https://medium.com/@joshua.chyeung/visualizing-traffic-conditions-based-on-radio-traffic-news-20d47c5b1c96).

My project is divided into the following tasks:

### I. Web Scraping using BeautifulSoup

Scrape the traffic news from the radio broadcast RTHK website. [http://rthk9.rthk.hk/trafficnews/].


### II. Extract the locations and Categorize the news

Extract the physical location of the traffic news based on a specific keyword. Categorize the news according to a set of wording describing the traffic condition.


### III. Geocoding using GeoPy
Convert the physical locations of the traffic news to the geographic locations.


### IV. Data Visualization on a Map
Display the traffic news according to its geographical locations.

# Building a Website via Scraping

## Summary

This project was aimed at building a website solely from external data from multiple sources – primarily ETL through Python, ultimately displayed with JavaScript.
To gather these sources, I wrote a Python script using BeautifulSoup to scrape multiple different websites (mainly various NASA site’s and its twitter profile) to generate the information that was desired. This data was stored as a dictionary, and ultimately imported into MongoDB to save for the long term.
Then a Flask app was constructed to retrieve the JSON data from Mongo and import it into a predefined template. Additionally, a JavaScript button allowed the user to refresh the data live by rerun the script and repopulation the site, overwriting the existing information in the MongoDB.
  
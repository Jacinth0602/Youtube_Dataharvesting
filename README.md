
# YouTube Data Harvesting and Data Warehousing

Data Harvesting and Data warehousing done on Specific Youtube Channels

![image](https://github.com/Jacinth0602/Youtube_Dataharvesting/assets/156180907/5f90fbe7-0a3a-474b-8159-b57a62b235f0)

## Overview

Scripts for gathering data from YouTube and creating a data warehouse for analysis are available in this GitHub repository. The objective is to gather, store, and evaluate YouTube data in order to analyze it and to answer the built-in questions.
Using API keys, this web application can scrape data from YouTube channels and store it in a mongoDB collection before moving it to PostgreSQL. We can deliver scripted answers to questions by using ETL.

## Prerequistes

install all the below packages with pip install in terminal.

-pandas
-pymongo
-psycopg2
-streamlit
-googleapiclient.discovery

Code requires Youtube API Key from google Youtube developer.

**https://developers.google.com/youtube/v3/getting-started**

## Files included

These are multipage Streamlit applications (Run only main.py)

main.py --> The executable file

Youtube_DataScrap.py --> Data harvesting and Warehousing is done in this script

Queries.py --> The questions page is scripted

## Data Harvesting

Describe the data harvesting process, including any API keys or access tokens required. Provide information on rate limiting, data sources, and any specific considerations users should be aware of.

## Data Warehousing

Explain the data warehousing architecture and how users can set up their own data warehouse using the harvested YouTube data. Include details on data modeling, storage considerations, and data retrieval methods.

## Contributing

Encourage users to contribute to your project by providing guidelines for submitting bug reports, feature requests, and pull requests. Include information on coding standards and any specific conventions used in the project.

## License

Specify the license under which your project is released. Choose a license that aligns with your project goals and encourages collaboration.

---


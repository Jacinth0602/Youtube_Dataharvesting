
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

## Workflow

Create a strealit Application with 'streamlit' package
Using API requests collect YouTube data such as Channel, Playlist, Video and Comment data.
Upload the YouTube data into MongoDB using the 'pymongo' package
Migrate the data in MongoDB to POSTGRE SQL tables.
Develop SQL queries within the Streamlit app to retrieve specific information from the SQL database.

## Contributing

Encourage users to contribute to your project by providing guidelines for submitting bug reports, feature requests, and pull requests. Include information on coding standards and any specific conventions used in the project.

## License

Specify the license under which your project is released. Choose a license that aligns with your project goals and encourages collaboration.

---


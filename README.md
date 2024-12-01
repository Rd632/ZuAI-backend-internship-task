Objective of this project:
Scrape Sample IA’s and Sample EE’s from the Nailib website focusing on IB Math AI SL samples. Extract structured data, clean it, and store it in MongoDB on each run.

Task Breakdown:
    Step 1: Website Exploration & Data Points Identification
            Extract data from pages similar to this Math AI SL IA sample. Key data points include:
                  Title: Name of the IA or EE.
                  Subject: E.g., Math AI SL.
                  Description: Checklist, instructions, or summaries
                  File Links: Extract any downloadable resources (if available).
                  Word Count and Time Estimate (e.g., "11 mins read").
                  Publication Date (if applicable).

   Step 2: Scraping & Data Cleaning
            Ensure Structured Extraction: Navigate the page structure to retrieve relevant data fields.
            Handle Inconsistencies: Normalize text fields, remove unnecessary whitespace, and handle missing fields gracefully.

  Step 3: MongoDB Integration
            Database Schema: Design a schema for storing IA and EE data in MongoDB.
             {
              "title": "Sample IA Title",
              "subject": "Math AI SL",
              "description": "Checklist for IA",
              "word_count": 2112,
              "read_time": "11 mins",
              "file_link": "https://nailib.com/resource.pdf",
              "publication_date": "YYYY-MM-DD"
            }
            
            
  Upsert Data: Prevent duplication using MongoDB’s upsert feature.

Technical Requirements:
Language: Python.
Libraries:
Scraping: BeautifulSoup, Scrapy, or Selenium.
Database: PyMongo.
Error Handling: Implement robust error handling for network and data issues.






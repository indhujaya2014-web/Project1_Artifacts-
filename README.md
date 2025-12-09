# Project1_Artifacts
**Harvard’s Artifacts Collection: ETL, SQL Analytics &amp; Streamlit Showcase**

**Project Statement**
  As an app developer, have tasked with building an interactive, end-to-end ETL and data exploration platform using the Harvard Art Museums public API. This platform will empower users to dynamically explore, collect, store, and query rich art collections from Harvard’s digital archive — all through a simple, intuitive Streamlit web application.

***Project Approach***
1: Getting the Harvard Art Museums API Key
2: Find the classification names where the object count is >= 2500 (for classification url)
  [HarvardArtMuseum classification url](https://api.harvardartmuseums.org/classification)
3: Scroll through 25 pages and collect 2500 records (for object url)
  [HarvardArtMuseum object url](https://api.harvardartmuseums.org/object)
  HINT: for the below steps use [HarvardArtMuseum object url]
4: Collect a minimum of 2500 records for every classification (ex: Coins, Paintings, Sculpture, Photographs, Drawings etc..)
5: Extraction of up to 12,500 artifact records (5 classifications × 2500 records each) using the Harvard Art Museum API
6: Transformed and filtered JSON data to retain only essential fields needed for analysis.
7: Three SQL tables (artifact_metadata, artifact_media, artifact_colors) auto-created and populated using Python — no manual SQL writing required.
8: Ability to retrieve and store artifacts based on user-input classification via a user-friendly Streamlit interface.
9: Option to view extracted records instantly and trigger SQL insertion with a single click
10: A polished, intuitive Streamlit dashboard for exploring data and practicing SQL analysis in real time.


***Technical Tags***
API Integration, JSON Parsing, Python, SQL, Data Extraction, Data Transformation, Data Cleaning, Database Insertion, SQL Joins, Streamlit, Data Filtering, Pagination, ETL Pipelines, Interactive Dashboards, Data Exploration, Museum Informatics, Cultural Data Analytics, SQL Query Optimization, API-driven Data Collection, Dynamic Data Storage, End-to-End Data Workflow.  

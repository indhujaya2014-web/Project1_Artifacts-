# 🏛️ Harvard’s Artifacts Collection: ETL, SQL Analytics & Streamlit Showcase

## Project Statement
> An interactive, end-to-end ETL and data exploration platform leveraging the Harvard Art Museums public API, allowing dynamic collection, storage, and SQL analysis of rich art artifacts via a Streamlit web application.

## 📌 Project Approach
1.  Getting the Harvard Art Museums API Key
	  **API Key:** Obtain a free API Key from the Harvard Art Museums:
   	 * Go to: [Harvard Art Museums API Request](https://www.harvardartmuseums.org/collections/api)
   	 * Follow the link to "Send a request" and submit the form. Your key will be displayed instantly.
2.  Find the classification names where the object count is >= 2500 (for classification url)
    	[HarvardArtMuseum classification url](https://api.harvardartmuseums.org/classification)
3.  Scroll through 25 pages and Collect a minimum of 2500 records for every classification names (for object url)
	    [HarvardArtMuseum object url](https://api.harvardartmuseums.org/object)
	    HINT: for the below steps use [HarvardArtMuseum object url]
4.  Collect minimum of 2500 records for atleast 5 classifications with respect to Artifacts (artifact_metadata, artifact_media and artifact colors)
5.  Extraction of up to 12,500 artifact records (5 classifications × 2500 records each) using the Harvard Art Museum API
6.  Transformed and filtered JSON data to retain only essential fields needed for analysis.
7.  Three SQL tables (artifact_metadata, artifact_media, artifact_colors) auto-created and populated using Python — no manual SQL writing required.
8.  Ability to retrieve and store artifacts based on user-input classification via a user-friendly Streamlit interface.
9.  Option to view extracted records instantly and trigger SQL insertion with a single click
10.  A polished, intuitive Streamlit dashboard for exploring data and practicing SQL analysis in real time.

## 🌟 Key Features
This platform is designed to provide a complete data workflow solution, empowering users to move from raw API data to insightful analysis seamlessly.

* **Dynamic API Integration:** Extract artifact data from the Harvard Art Museums API, focusing on over **100+ unique classifications** (e.g., Paintings, Coins, Sculptures).
* **End-to-End ETL Pipeline:** **Extract**, **Transform** (clean, filter, and structure JSON data), and **Load** data into a normalized SQL database.
* **Structured Data Storage:** Automatically design and populate three separate SQL tables (`artifact_metadata`, `artifact_media`, `artifact_colors`) directly from the Streamlit application.
* **Interactive Streamlit Dashboard:** A user-friendly interface for controlling the data pipeline, viewing extracted records, triggering SQL insertion, and executing pre-defined analytical queries.
* **SQL Analytics Showcase:** A dedicated workspace to run over **20+ predefined SQL queries** (including advanced JOINs) to derive insights into collection trends, media usage, and color distribution.

## 🎯 Domain & Business Use Cases
**Domain:** Cultural Heritage Data Analytics / Museum Informatics

| Use Case | Description |
| :--- | :--- |
| **Museum Collection Strategy** | Curators can analyze classification trends (e.g., accession year, medium) to guide future acquisitions or exhibition planning. |
| **Educational Portals** | Provides an interactive tool for students and researchers to explore historical artifacts by classification, era, or culture. |
| **Audience Interest Tracking** | Analyze which types of artifacts receive the most views/queries, informing digital marketing strategies. |
| **Cultural Research** | Supports historians and journalists in filtering and retrieving targeted artifact data for story telling and analysis. |

## 🛠 Technical Tags
API Integration, JSON Parsing, Python, SQL, Data Extraction, Data Transformation, Data Cleaning, Database Insertion, SQL Joins, Streamlit, Data Filtering, Pagination, ETL Pipelines, Interactive Dashboards, Data Exploration, Museum Informatics, Cultural Data Analytics, SQL Query Optimization, API-driven Data Collection, Dynamic Data Storage, End-to-End Data Workflow.  

### Running the Application
1.  **Launch Streamlit:**
2.  The application will open in your browser (`http://localhost:8501`).
   
## 🎮 Usage & Workflow
The Streamlit interface guides the user through the three main stages:

### 1. Data Collection (ETL)
1.  **Select Classification:** Use the dropdown menu to choose an artifact classification (e.g., "Drawings," "Jewelry").
2.  **Collect Data:** Click the **`Collect Data`** button to fetch a minimum of **2500 records** for the selected classification using the API.
3.  **View & Insert:**
    * Click **`Show Data`** to preview the transformed records.
    * Click **`Insert into SQL`** to clean the data and automatically populate the three SQL tables. (Recommended to collect 4-5 classifications for rich analysis.)

### 2. SQL Table Schema

The extracted JSON data is structured into three normalized tables for efficient querying:
#### 🗄️ `artifact_metadata` (General Artifact Details)
#### 🖼️ `artifact_media` (Media & Date Information)
#### 🎨 `artifact_colors` (Color Analysis Data)

### 3. SQL Querying & Visualization

The **`Query & Visualization Section`** allows users to practice and execute SQL analysis:
1.  **Select Query:** Choose from **20+ pre-written analytical queries** covering single-table queries and complex JOINs.
2.  **Run Query:** Click the **`Run Query`** button.
3.  **Display Results:** The results are displayed in a formatted table (mandatory) or an optional interactive chart.

---

#### Sample Queries (Predefined in App)

**Single Table Examples:**
1.  List all artifacts from the 11th century belonging to Byzantine culture.
2.  How many artifacts are there per department?
3.  What are the top 5 most used colors by frequency?
4.  What is the average rank of all artifacts?
 
**Join-Based Examples:**
1.  List artifact titles and hues for all artifacts belonging to the Byzantine culture.
2.  Find artifact titles ranked in the top 10 that include the color hue "Grey".
3.  How many artifacts exist per classification, and what is the average media count for each?
4.  List all colors used for a given artifact ID.
---

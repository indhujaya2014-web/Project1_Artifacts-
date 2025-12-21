# from importlib.metadata import metadata
import requests
import pymysql
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv

# --- CONFIGURATION ---

st.set_page_config(layout="wide")

load_dotenv()
# API_KEY = os.getenv("HARVARD_ART_API_KEY", "568fa32d-1032-4ae1-8670-e0c5ab20a5dd")
API_KEY = "1a7ae53e-a8d5-4ca8-8cbf-e12a843ceec9"
DATABASE_NAME = "harvard_test"
url = "https://api.harvardartmuseums.org/object"
# --- SQL CONNECTION ---
conn = pymysql.connect(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    user="4Sw7vnWkyLJgtmE.root",    
    password="N1BiWHTTmOf88ojU",
    port=4000,
    database=DATABASE_NAME,
    charset="utf8mb4",
    ssl={'ssl': True},
    autocommit=False  # Important for bulk inserts
)
cursor = conn.cursor()

#--------------------------------------------------------- Data Collection based on classification ------------------------------------------------------------------#
def get_classifications(API_KEY,classification_name):
    all_records = []

    for page in range(1, 26):
        params = {
            "apikey": API_KEY,
            "size": 100,
            "page": page,
            "classification": classification_name
        }

        response = requests.get(url, params=params)

        data = response.json()
        records = data.get('records', [])
        if not records:
            break 
        all_records.extend(records)

    return all_records
    

# --- FETCH ARTIFACTS BY CLASSIFICATION ---
def fetch_artifacts_by_classification(records):
    art_metadata = []
    media = []
    colors = []
    # classifications = ["Coins","Paintings","Sculpture","Photographs","Drawings"]
    for i in records:
                # Extract metadata
                art_metadata.append({
                    'id': i['id'],
                    'title': i['title'],
                    'culture': i['culture'],
                    'period': i['period'],
                    'century': i['century'],
                    'medium': i['medium'],
                    'dimensions': i['dimensions'],
                    'description': i['description'],
                    'department': i['department'],
                    'classification': i['classification'],
                    'accessionyear': i['accessionyear'],
                    'accessionmethod': i['accessionmethod']
                })
                # Extract media 
                media.append({
                    'objectid': i['objectid'],
                    'imagecount': i['imagecount'],
                    'mediacount': i['mediacount'],
                    'colorcount': i['colorcount'],
                    'rank': i['rank'],
                    'datebegin': i['datebegin'],
                    'dateend': i['dateend']
                })
                # Extract colors
                color_details = i.get('colors')
                if color_details:
                    for j in color_details:
                        colors.append({
                            'objectid': i['objectid'],
                            'color': j['color'],
                            'spectrum': j['spectrum'],
                            'hue': j['hue'],
                            'percent': j['percent'],
                            'css3': j['css3']
                        })

    return art_metadata, media, colors

# --- INITIALIZE DATABASE ---
def Create_table():   
        # metadata table creation
    cursor.execute("""create table if not exists artifacts_metadata(
            id int primary key,
            title text,
            culture text,
            period text,
            century text,
            medium text,
            dimensions text,
            description text,
            department text,
            classification text,
            accessionyear integer,
            accessionmethod text
        )""")

        # media table creation
    cursor.execute("""create table if not exists artifacts_media(
            object_id int,
            image_count int,
            media_count int,
            color_count int,
            item_rank int,
            date_begin int,
            date_end int,
            foreign key (object_id) references artifacts_metadata(id)
        )""")

        # colors table creation
    cursor.execute("""create table if not exists artifacts_colors(
            object_id int,
            color text,
            spectrum text,
            hue text,
            percent text,
            css3 text,
            foreign key (object_id) references artifacts_metadata(id)
        )""")
Create_table()

#----------------------Insert Data into Tables----------------------#
def prepare_data_for_insertion(art_metadata, media, colors):

    data_to_insert_metadata = []
    data_to_insert_media = []
    data_to_insert_colors = []

    # Extract and format data as needed
    for i in art_metadata:
        data_to_insert_metadata.append((i['id'], i['title'], i['culture'], i['period'], i['century'], i['medium'], i['dimensions'], i['description'], i['department'], i['classification'], i['accessionyear'], i['accessionmethod']))

    for i in media:
        data_to_insert_media.append((i['objectid'], i['imagecount'], i['mediacount'], i['colorcount'], i['rank'], i['datebegin'], i['dateend']))

    for i in colors:
        data_to_insert_colors.append((i['objectid'], i['color'], i['spectrum'], i['hue'], i['percent'], i['css3']))

    insert_query_metadata = """insert ignore into artifacts_metadata values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update title=values(title)"""
    insert_query_media = """insert ignore into artifacts_media values(%s,%s,%s,%s,%s,%s,%s)"""
    insert_query_colors = """insert ignore into artifacts_colors values(%s,%s,%s,%s,%s,%s)"""
    # insert_query_metadata = "INSERT IGNORE INTO artifacts_metadata(id, title, culture, period, century, medium, dimensions, description, department, classification, accessionyear, accessionmethod) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    # insert_query_media = "INSERT IGNORE INTO artifacts_media(object_id,image_count, media_count, color_count, item_rank, date_begin, date_end) values (%s,%s,%s,%s,%s,%s,%s)"
    # insert_query_colors = "INSERT IGNORE INTO artifacts_colors(object_id,color,spectrum,hue, percent, css3) values (%s,%s,%s,%s,%s,%s)"
    try:
    # Extract and format data as needed
        with conn.cursor() as cursor:
                cursor.executemany(insert_query_metadata, data_to_insert_metadata)
                cursor.executemany(insert_query_media, data_to_insert_media)
                cursor.executemany(insert_query_colors, data_to_insert_colors)
        conn.commit()
    except Exception as e:
        st.error(f"Database initialization failed: {e}")
        conn.rollback()

# ------------------ STREAMLIT APP LAYOUT ------------------#

with st.sidebar:
        selected = option_menu("Main Menu",
        ["Home", "Data Collection", "SQL Queries"],
        icons=["house", "database", "search"],
        menu_icon="cast",
        default_index=0)
        selected

if selected == "Home":
        st.markdown("<h1 style='text-align: center; color: black;'>🏛️ Harvard’s Artifacts Collection</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: green'> Welcome to Harvard Art Museums Data Application </h2>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("""
            This application allows you to collect artifact data from the Harvard Art Museums API,
            store it in a SQL database, and run analytical queries to gain insights into the collection.
        """)
        st.markdown("### About Harvard Art Museums")
        st.page_link("https://www.harvardartmuseums.org/collections", label="Harvard Art Museums", icon="🏛️")

elif selected == "Data Collection":
            # ---- Dropdown to select a classification ---
            st.subheader("Select Classification")
            classifications_name = st.selectbox(
                    "Please select a classification",
                    ("Coins", "Paintings", "Sculpture","Photographs","Drawings"),
                    index=0 # Default to 'Select Classification'
                    )
            st.markdown("""
            Use this section to collect artifact data from the Harvard Art Museums API
            and store it in the connected SQL database.
            """)
             
            st.write("You selected:", classifications_name)
            menu = option_menu(None,["📥 Collect Data from API","💾 Migrate to SQL"], orientation="horizontal")

            if menu == "📥 Collect Data from API":
                 if st.button("📥 Collect Data from API"):
                    if classifications_name != "":
                        records = get_classifications(API_KEY, classifications_name)
                        art_metadata, media, colors = fetch_artifacts_by_classification(records)
                        st.success(f"Data fetched successfully! for {classifications_name}")
                        col1, col2, col3 = st.columns(3)
                        st.spinner(f"Collecting minimum 2500 records for {classifications_name}...")

                        with col1:
                                st.header("Artifacts_Metadata")
                                st.json(art_metadata)
                        with col2:
                                st.header("Artifacts_Media")
                                st.json(media)
                        with col3:
                                st.header("Artifacts_Colors")
                                st.json(colors) 
                    else:
                        st.error("No data fetched. Please try again. or kindly select classification") 
        
            if menu == "💾 Migrate to SQL":
                    st.subheader("Migrate Data to SQL")
                    cursor.execute("""select distinct(classification) from artifacts_metadata""")
                    result = cursor.fetchall()
                    list_classifications = [i[0] for i in result]
                    st.write("Existing Classifications in Database:", list_classifications)

                    st.subheader("Insert the fetched data into Database")
                    if st.button("💾 Insert into SQL"):
                        if classifications_name not in list_classifications:
                            records = get_classifications(API_KEY, classifications_name)
                            art_metadata, media, colors = fetch_artifacts_by_classification(records)
                            prepare_data_for_insertion(art_metadata, media, colors)
                            if prepare_data_for_insertion == None:
                                st.error("No data to insert. Please fetch data first.")
                            else:
                                st.success("Data Inserted successfully")
                            st.header("Inserted Data:")
                            st.divider()

                            st.subheader("👀 Artifacts Metadata")
                            cursor.execute("SELECT * FROM artifacts_metadata;")
                            results1 = cursor.fetchall()
                            columns = [i[0] for i in cursor.description]
                            df_metadata = pd.DataFrame(results1, columns=columns)
                            st.dataframe(df_metadata)

                            st.subheader("👀 Artifacts Media")    
                            cursor.execute("SELECT * FROM artifacts_media;")
                            results2 = cursor.fetchall()
                            columns = [i[0] for i in cursor.description]
                            df_media = pd.DataFrame(results2, columns=columns)
                            st.dataframe(df_media)

                            st.subheader("👀 Artifacts Colors")
                            cursor.execute("SELECT * FROM artifacts_colors;")
                            results3 = cursor.fetchall()
                            columns = [i[0] for i in cursor.description]
                            df_colors = pd.DataFrame(results3, columns=columns)
                            st.dataframe(df_colors)
                        else:
                            st.warning(f"Data for classification '{classifications_name}' already exists in the database.")
                        
elif selected == "SQL Queries":
            
            option = st.selectbox(
                "Select a query to run:",
                ("1. List all artifacts from the 11th century belonging to Byzantine culture.",
                "2. What are the unique cultures represented in the artifacts?",
                "3. List all artifacts from the Archaic Period.",
                "4. List artifact titles ordered by accession year in descending order.",
                "5. How many artifacts are there per department?",
                "6. Which artifacts have more than 1 image?",
                "7. What is the average rank of all artifacts?",
                "8. Which artifacts have a higher colorcount than mediacount?",
                "9. List all artifacts created between 1500 and 1600.",
                "10. How many artifacts have no media files?",
                "11. What are all the distinct hues used in the dataset?",
                "12. What are the top 5 most used colors by frequency?",
                "13. What is the average coverage percentage for each hue?",
                "14. List all colors used for a given artifact ID.",
                "15. What is the total number of color entries in the dataset?",
                "16. List artifact titles and hues for all artifacts belonging to the Byzantine culture.",
                "17. List each artifact title with its associated hues.",
                "18. Get artifact titles, cultures, and media ranks where the period is not null.",
                "19. Find artifact titles ranked in the top 10 that include the color hue 'Grey'.",
                "20. How many artifacts exist per classification, and what is the average media count for each?",
                "21. Find the total number of artifacts and their average display rank for each classification.",
                "22. Find the average `percent` coverage of all colors for artifacts using 'silver' as a `medium`",
                "23. Calculate the average `rank` only for artifacts that have more than 3 associated images",
                "24. List the titles of the 10 oldest artifacts (by `datebegin`) that have a `colorcount` greater than 5",
                "25. List all artifacts from the 20th century belonging to Roman and American culture"                
                ),index=None,placeholder="Select a query"
            )
            if option == "1. List all artifacts from the 11th century belonging to Byzantine culture.":
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM artifacts_metadata WHERE century = '11th century' AND culture = 'Byzantine';")
                    results = cursor.fetchall()
                    columns = [i[0] for i in cursor.description]
                    df = pd.DataFrame(results, columns=columns)
                    st.dataframe(df)

            elif option == "2. What are the unique cultures represented in the artifacts?":
                cursor.execute("SELECT DISTINCT culture FROM artifacts_metadata;")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)

            elif option == "3. List all artifacts from the Archaic Period.":
                cursor.execute("SELECT * FROM artifacts_metadata WHERE period = 'Archaic period';")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)

            elif option == "4. List artifact titles ordered by accession year in descending order.":
                cursor.execute("SELECT title, accessionyear FROM artifacts_metadata ORDER BY accessionyear DESC;")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)
            
            elif option == "5. How many artifacts are there per department?":
                cursor.execute("SELECT department, COUNT(*) AS artifact_count FROM artifacts_metadata GROUP BY department;")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)

            elif option == "6. Which artifacts have more than 1 image?":
                cursor.execute("select * from artifacts_media where image_count > 1;")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)

            elif option == "7. What is the average rank of all artifacts?":
                cursor.execute("select avg(item_rank) as Average_rank from artifacts_media;")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)

            elif option == "8. Which artifacts have a higher colorcount than mediacount?":
                cursor.execute("select * from artifacts_media where color_count > media_count;")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)

            elif option == "9. List all artifacts created between 1500 and 1600.":
                cursor.execute("select * from artifacts_media where date_begin >= 1500 and date_end <= 1600;")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)

            elif option == "10. How many artifacts have no media files?":
                cursor.execute("select count(*) as No_media_artifacts from artifacts_media where media_count = 0;")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)

            elif option == "11. What are all the distinct hues used in the dataset?":
                cursor.execute("select distinct(hue) from artifacts_colors;")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)

            elif option == "12. What are the top 5 most used colors by frequency?":
                cursor.execute("select hue, count(hue) as frequency from artifacts_colors group by hue order by frequency desc limit 5;")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)

            elif option == "13. What is the average coverage percentage for each hue?":  
                cursor.execute("select hue, AVG(percent) as average_coverage_percentage from artifacts_colors group by hue order by average_coverage_percentage desc;")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)

            elif option == "14. List all colors used for a given artifact ID.":
                artifact_id = st.text_input("Enter Artifact ID:")
                if st.button("Submit"):
                    cursor.execute("SELECT * FROM artifacts_colors WHERE object_id = %s;", (artifact_id,))
                # cursor.execute("SELECT * FROM artifacts_colors WHERE object_id = 195538;")  # Hardcoded artifact ID
                    results = cursor.fetchall()
                    columns = [i[0] for i in cursor.description]
                    df = pd.DataFrame(results, columns=columns)
                    st.dataframe(df)
            elif option == "15. What is the total number of color entries in the dataset?":
                cursor.execute("SELECT COUNT(*) AS total_color_entries FROM artifacts_colors;")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)
            elif option == "16. List artifact titles and hues for all artifacts belonging to the Byzantine culture.":
                cursor.execute("SELECT title, hue FROM artifacts_metadata AS T1 JOIN artifacts_colors AS T3 ON T1.id = T3.object_id WHERE T1.culture = 'Byzantine';")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)

            elif option == "17. List each artifact title with its associated hues.":
                cursor.execute("SELECT title, hue FROM artifacts_metadata AS T1 JOIN artifacts_colors AS T3 ON T1.id = T3.object_id;")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)

            elif option == "18. Get artifact titles, cultures, and media ranks where the period is not null.":
                cursor.execute("SELECT title, culture, item_rank FROM artifacts_metadata AS T1 JOIN artifacts_media AS T2 ON T1.id = T2.object_id WHERE T1.period IS NOT NULL;")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)

            elif option == "19. Find artifact titles ranked in the top 10 that include the color hue 'Grey'.":
                cursor.execute("SELECT title, hue, item_rank FROM artifacts_metadata AS T1 JOIN artifacts_media AS T2 ON T1.id = T2.object_id JOIN artifacts_colors AS T3 ON T1.id = T3.object_id WHERE hue = 'Grey' and item_rank is not null order by T1.title asc, T2.item_rank asc limit 10;")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)

            elif option == "20. How many artifacts exist per classification, and what is the average media count for each?": 
                cursor.execute("SELECT T1.classification, COUNT(T1.id) AS artifact_count, AVG(T2.media_count) AS average_media_count FROM artifacts_metadata AS T1 JOIN artifacts_media AS T2 ON T1.id = T2.object_id GROUP BY T1.classification;")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)

            elif option == "21. Find the total number of artifacts and their average display rank for each classification.":
                cursor.execute("SELECT T1.classification, COUNT(T1.id) AS total_artifacts, AVG(T2.item_rank) AS average_display_rank FROM artifacts_metadata AS T1 JOIN artifacts_media AS T2 ON T1.id = T2.object_id GROUP BY T1.classification;")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)

            elif option == "22. Find the average `percent` coverage of all colors for artifacts using 'silver' as a `medium`":
                cursor.execute("SELECT medium, AVG(percent) AS average_percent_coverage FROM artifacts_metadata AS T1 JOIN artifacts_colors AS T3 ON T1.id = T3.object_id WHERE T1.medium LIKE '%silver%' group by medium;")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)

            elif option == "23. Calculate the average `rank` only for artifacts that have more than 3 associated images":
                cursor.execute("SELECT AVG(item_rank) as average_rank FROM artifacts_media WHERE image_count > 3;")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)

            elif option == "24. List the titles of the 10 oldest artifacts (by `datebegin`) that have a `colorcount` greater than 5":
                cursor.execute("SELECT title, date_begin, color_count FROM artifacts_metadata AS T1 JOIN artifacts_media AS T2 ON T1.id = T2.object_id WHERE T2.color_count > 5 ORDER BY T2.date_begin ASC LIMIT 10;")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)

            elif option == "25. List all artifacts from the 20th century belonging to Roman and American culture":
                cursor.execute("SELECT * FROM artifacts_metadata WHERE century = '20th century' AND (culture = 'Roman' OR culture = 'American');")
                results = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)

            else:
                st.error("No query selected. Please choose a query from the dropdown.")

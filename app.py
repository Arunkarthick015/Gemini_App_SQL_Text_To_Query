from dotenv import load_dotenv
load_dotenv()


import streamlit as st
import os
import sqlite3
 
import google.generativeai as genai
import pandas as pd

# Configure our API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load GOogle GEMINI MODEL and Provide Query as Response
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel("gemini-2.5-pro")
    response=model.generate_content([prompt[0],question])
    print("The answer for",question,"is")
    return response.text

# Function to retrieve query from the sql database
def read_sql_query(sql,db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows,column_names

# Define the prompt properly

prompt = ["""
    You are an expert in converting normal english to SQL queries. I've the E-commerce database that has three tables.
    You are an expert in converting English questions to SQL query!
    The SQL database has three tables with the names table1, table2, table3 and 
          Eligibility has the following columns - 			  
    			eligibility_datetime_utc
    			item_id	
    			eligibility
    			message 

Ad_Sales_and_Metrics has the following columns
	date
	item_id
	ad_sales
	impressions
	ad_spend
	clicks
	units_sold
	
item_id is the primary key in table2 . 

Total_Sales_and_Metrics has the following columns:
	date
	item_id
	total_sales
	total_units_ordered
	
Join all the three tables with reference to the item id, if you want for your reference. Primary key is the column that has all unique values
\n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM table1 ;
    also the sql code should not have ``` in beginning or end and sql word in output
    
          
          The Three tables have the following data, first table has product eligibility mapped table, second has Product Level Ad Sales and Metrics Mapped and third has
          Product level total sales mapped.
          your job is to take the prompted question and convert into a sqllite query. You may also be required to join the tables to get the desired output.          
            So you need to convert the text into the correct query and then from that query when instructed you need to fetch the results from the database according to the query.
          For example if we have a Customers table and if I want to retrieve all the data or rows from that table i need to use the following query
          "SELECT * FROM Customers;"

          """]



# Stream lit app

st.set_page_config(page_title="I can Retrieve any SQL Query")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# If submit is clicked
if submit:
    response=get_gemini_response(question,prompt) # We get the sql query
    print(response)
    data,columns=read_sql_query(response,"ecommerce_data.db") # Passing it to find the result of the query
    st.divider()
    st.subheader("📌 Query:")
    st.text("The text is converted to the following query: ")
    st.subheader(response)
    st.code(response,language='sql')
    st.divider()
    st.subheader(f"📌 The Response:")
    st.text(f"for the question '{question}'is")
    
    df = pd.DataFrame(data,columns=columns)
    st.dataframe(df)
    st.divider()


    # Option for adding charts
    st.subheader("Charts")
    import matplotlib.pyplot as plt
    import plotly.express as px
    x_col = st.selectbox("Select X-axis column", df.columns)
    default_y_index = 1 if len(columns) > 1 else 0
    y_col = st.selectbox("Select Y-axis column", columns, index=default_y_index)
    st.plotly_chart(px.bar(df, x=x_col, y=y_col), use_container_width=True)



        
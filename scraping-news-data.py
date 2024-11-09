import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def scrap_news_data(): 
    url = "https://www.bbc.com/news/us-canada"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser") 
    
    newsTitle = []
    newsPublishDate = []
    newsSummary = []

    news_title = soup.find_all("h2", class_ = "sc-8ea7699c-3")
    for title in news_title:
        each_title = title.text
        newsTitle.append(each_title)

    news_publish_date = soup.find_all("span", class_ = "sc-6fba5bd4-1")
    for publish_date in news_publish_date:
        each_publish_date = publish_date.text
        newsPublishDate.append(each_publish_date)
        
    news_summary = soup.find_all("p", class_ = "sc-b8778340-4")
    for summary in news_summary:
        each_new_summary = summary.text
        newsSummary.append(each_new_summary)


    df = pd.DataFrame({
    'Title': newsTitle[0:10],
    'Publication Date': newsPublishDate[0:10],
    'Summary': newsSummary[0:10]
    })
    
    return df

def display_news_dashboard():
    df = scrap_news_data()

    st.title("Latest News Dashboard - BBC")
    st.subheader("Browse the latest news articles")

    st.write("### All News Articles")
    st.dataframe(df)

    search_keyword = st.text_input("Search articles by keyword:")
    if search_keyword:
        filtered_df = df[
            df['Title'].str.contains(search_keyword, case=False, na=False) |
            df['Summary'].str.contains(search_keyword, case=False, na=False)
        ]
        if not filtered_df.empty:
            st.write(f"### Search Results for '{search_keyword}'")
            st.dataframe(filtered_df)
        else:
            st.write("No articles found for the specified keyword.")

if __name__ == '__main__':
    display_news_dashboard()
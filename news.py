import streamlit as st
import requests

def fetch_news(api_key, keywords):
    """Fetch news articles from Newsdata.io API using the given keywords."""
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={keywords}&language=en"
    response = requests.get(url)
    if response.status_code == 200:
        news_data = response.json()
        if "results" in news_data:
            return news_data["results"]
        else:
            return []
    else:
        st.error(f"Failed to fetch news for {keywords}. Status code: {response.status_code}")
        return []

# Your Newsdata.io API key
API_KEY = "pub_611122f586a8fcd87bd13e911285ad9c31877"

# Topics and their corresponding keywords
topics = {
    "Fintech": "fintech",
    "Blockchain": "blockchain",
    "Cryptocurrency": "cryptocurrency",
    "Banking": "banking",
    "SaaS": "saas",
    "Fintech Innovation": "fintech innovation",
    "Payment Innovation": "payment innovation",
    "Financial Technology": "financial technology",
    "Artificial Intelligence": "artificial intelligence",
}

# Streamlit application
st.title("Latest News Aggregator")
st.write("Fetching the latest news across various topics in the financial and technological sectors.")

for topic, keywords in topics.items():
    st.subheader(topic)
    news_articles = fetch_news(API_KEY, keywords)

    if news_articles:
        for article in news_articles[:6]:  # Limit to 6 articles per topic
            st.markdown(f"### [{article['title']}]({article['link']})")
            st.write(f"Published by: {article.get('source_id', 'Unknown')}")
            st.write(f"Published on: {article.get('pubDate', 'Unknown')}")
            st.write("---")
    else:
        st.write(f"No news articles found for {topic}.")

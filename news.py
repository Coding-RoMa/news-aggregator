
import streamlit as st
import requests
from pytrends.request import TrendReq

def fetch_mediastack_news(api_key, keywords):
    """Fetch news articles from MediaStack API using the given keywords."""
    url = f"http://api.mediastack.com/v1/news?access_key={api_key}&keywords={keywords}&languages=en"
    response = requests.get(url)
    if response.status_code == 200:
        news_data = response.json()
        if "data" in news_data:
            return news_data["data"]
        else:
            return []
    else:
        st.error(f"Failed to fetch news for {keywords} from MediaStack. Status code: {response.status_code}")
        return []

def fetch_google_trends():
    """Fetch trending topics from Google Trends."""
    pytrends = TrendReq(hl="en-US", tz=360)
    trending_searches = pytrends.trending_searches(pn="united_states")  # Change location as needed
    trending_topics = trending_searches.head(10).values.flatten().tolist()
    return trending_topics

# API Key for MediaStack
MEDIASTACK_API_KEY = "ee3eb07348f915164106bf1328b7a790"

# Topics and their corresponding keywords
topics = {
    "Fintech": "fintech",
    "Blockchain": "blockchain",
    #"Cryptocurrency": "cryptocurrency",
    "Banking": "banking",
    #"SaaS": "saas",
    #"Fintech Innovation": "fintech innovation",
    "Payment Innovation": "payment innovation",
    #"Financial Technology": "financial technology",
    "Artificial Intelligence": "artificial intelligence",
}

# Streamlit application
st.title("Latest News Aggregator")
st.write("Fetching the latest news across various topics in the financial and technological sectors.")

# MediaStack News Section
st.header("News from MediaStack")
for topic, keywords in topics.items():
    st.subheader(topic)
    news_articles = fetch_mediastack_news(MEDIASTACK_API_KEY, keywords)

    if news_articles:
        for article in news_articles[:4]:  # Limit to 4 articles per topic
            st.markdown(f"### [{article['title']}]({article['url']})")
            st.write(f"Source: {article.get('source', 'Unknown')}")
            st.write(f"Published on: {article.get('published_at', 'Unknown')}")
            st.write("---")
    else:
        st.write(f"No news articles found for {topic}.")

# Google Trends Section
st.header("Trending Topics from Google Trends")
google_trends = fetch_google_trends()
if google_trends:
    for trend in google_trends:
        st.markdown(f"### {trend}")
        st.write("---")
else:
    st.write("No trending topics available from Google Trends.")


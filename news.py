import streamlit as st
import requests
from pytrends.request import TrendReq

def fetch_newsdata_news(api_key, keywords):
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
        st.error(f"Failed to fetch news for {keywords} from Newsdata.io. Status code: {response.status_code}")
        return []

def fetch_google_trends():
    """Fetch trending topics from Google Trends."""
    pytrends = TrendReq(hl="en-US", tz=360)
    trending_searches = pytrends.trending_searches(pn="united_states")  # Change location as needed
    trending_topics = trending_searches.head(10).values.flatten().tolist()
    return trending_topics

def fetch_newsapi_trending(api_key, keywords):
    """Fetch trending news articles from NewsAPI.org."""
    url = f"https://newsapi.org/v2/everything?q={keywords}&apiKey={api_key}&language=en"
    response = requests.get(url)
    if response.status_code == 200:
        news_data = response.json()
        return news_data.get("articles", [])
    else:
        st.error(f"Failed to fetch news for {keywords} from NewsAPI.org. Status code: {response.status_code}")
        return []

# API Keys
NEWSDATA_API_KEY = "pub_611122f586a8fcd87bd13e911285ad9c31877"
NEWSAPI_API_KEY = "50920c851b5f4f6a97e2e2246b4193f5"

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

# Newsdata.io Section
st.header("News from Newsdata.io")
for topic, keywords in topics.items():
    st.subheader(topic)
    news_articles = fetch_newsdata_news(NEWSDATA_API_KEY, keywords)

    if news_articles:
        for article in news_articles[:6]:  # Limit to 6 articles per topic
            st.markdown(f"### [{article['title']}]({article['link']})")
            st.write(f"Published by: {article.get('source_id', 'Unknown')}" or "Unknown")
            st.write(f"Published on: {article.get('pubDate', 'Unknown')}")
            st.write("---")
    else:
        st.write(f"No news articles found for {topic}.")

'''
# Google Trends Section
st.header("Trending Topics from Google Trends")
google_trends = fetch_google_trends()
if google_trends:
    for trend in google_trends:
        st.markdown(f"### {trend}")
        st.write("---")
else:
    st.write("No trending topics available from Google Trends.")

'''

# Google Trends Section: Top Stories for Specific Topics
st.header("Top Stories from Google Trends")
for topic in ["fintech", "financial technology"]:
    st.subheader(f"Top Stories for {topic.capitalize()}")
    top_stories = fetch_top_stories(topic)

    if top_stories:
        for story in top_stories.itertuples():
            st.markdown(f"### {story.query}")
            st.write(f"Relevance: {story.value}")
            st.write("---")
    else:
        st.write(f"No top stories found for {topic}.")



# NewsAPI.org Section
st.header("News from NewsAPI.org")
for topic, keywords in topics.items():
    st.subheader(topic)
    news_articles = fetch_newsapi_trending(NEWSAPI_API_KEY, keywords)

    if news_articles:
        for article in news_articles[:6]:  # Limit to 6 articles per topic
            st.markdown(f"### [{article['title']}]({article['url']})")
            st.write(f"Published by: {article['source']['name']}" or "Unknown")
            st.write(f"Published on: {article.get('publishedAt', 'Unknown')}")
            st.write("---")
    else:
        st.write(f"No news articles found for {topic}.")

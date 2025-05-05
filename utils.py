from newsapi import NewsApiClient
import praw
from pytrends.request import TrendReq

def get_newsapi_trends(api_key, top_n=5, country='us'):
    newsapi = NewsApiClient(api_key=api_key)
    resp = newsapi.get_top_headlines(country=country, page_size=top_n)
    return [a.get("title") for a in resp.get("articles", []) if a.get("title")]

def get_reddit_trends(client_id, client_secret, user_agent, subreddit='news', top_n=5):
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
    return [post.title for post in reddit.subreddit(subreddit).hot(limit=top_n)]

def get_google_trends(keywords, region='US'):
    pytrends = TrendReq()
    pytrends.build_payload(keywords, geo=region)
    df = pytrends.interest_over_time()
    if df.empty: return []
    return df.sort_values(by=df.columns[0], ascending=False).head().index.strftime('%Y-%m-%d').tolist()

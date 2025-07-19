import os
import tweepy
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Autentisering
client = tweepy.Client(
    consumer_key = 'C1V4vht8gXiYocrdGeL3wH6eP',
    consumer_secret = '6DR60sxa4brZZIbbhZNclETojVNk3ttYoUxT3E4TyXCW05M0jD',
    access_token = '1945544864776548352-RBCtzcnDGvZEmFrxGkc7BJq4igBr9e',
    access_token_secret = 'ey0z9xHP87dUJdyjHfUtKq3g1xcPExznqS2xB7ZCHKZG4',
    wait_on_rate_limit=True
)

# Användarinfo
user = client.get_user(username="promptpdfmaster")
user_id = user.data.id

# Hämta senaste 100 tweets
tweets = client.get_users_tweets(
    id=user_id,
    tweet_fields=["public_metrics", "created_at", "text"],
    max_results=100
)

# Extrahera statistik
data = []
for t in tweets.data:
    metrics = t.public_metrics
    data.append({
        "Text": t.text[:80] + "..." if len(t.text) > 80 else t.text,
        "Datum": t.created_at.strftime("%Y-%m-%d"),
        "Impressions": metrics.get("impression_count", 0),
        "Retweets": metrics["retweet_count"],
        "Likes": metrics["like_count"],
        "Replies": metrics["reply_count"],
        "Tweet ID": t.id
    })

df = pd.DataFrame(data)
df = df.sort_values(by="Impressions", ascending=False)

# === Streamlit UI ===
st.title("📊 Twitter-statistik för dina produkter")
st.write(f"Visar senaste {len(df)} tweets från @{user.data.username}")

st.dataframe(df, use_container_width=True)

st.markdown("---")
st.markdown("Tips: klicka på en Tweet ID för att öppna den manuellt.")

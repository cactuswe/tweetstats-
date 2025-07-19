import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st

# Byt till ditt faktiska användarnamn
username = "ditt_användarnamn"  # ex: "noahcreates"

# Hämta de senaste 100 tweetsen
tweets = []
for i, tweet in enumerate(sntwitter.TwitterUserScraper(username).get_items()):
    if i >= 100:
        break
    tweets.append({
        "Text": tweet.content[:100] + "..." if len(tweet.content) > 100 else tweet.content,
        "Datum": tweet.date.strftime("%Y-%m-%d"),
        "Impressions": tweet.viewCount,
        "Likes": tweet.likeCount,
        "Retweets": tweet.retweetCount,
        "Replies": tweet.replyCount,
        "Tweet URL": f"https://twitter.com/{username}/status/{tweet.id}"
    })

df = pd.DataFrame(tweets)

# Sortera efter impressions
df = df.sort_values(by="Impressions", ascending=False)

# === Streamlit UI ===
st.set_page_config(page_title="Twitter Stats", layout="wide")
st.title("📈 Twitter-statistik från scraping")
st.write(f"Visar senaste {len(df)} tweets från @{username}")

st.dataframe(df, use_container_width=True)
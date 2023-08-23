import requests
import os
import discord
from requests_oauthlib import OAuth1

TWITTER_ACCOUNT = "fabriciofes"  # Substitua pelo seu usuário do Twitter
DISCORD_CHANNEL_ID = 847553861035884548  # Substitua pelo ID do canal do Discord

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

    twitter_consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
    twitter_consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
    twitter_access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    twitter_access_secret = os.environ.get("TWITTER_ACCESS_SECRET")

    auth = OAuth1(
        twitter_consumer_key,
        client_secret=twitter_consumer_secret,
        resource_owner_key=twitter_access_token,
        resource_owner_secret=twitter_access_secret
    )

    response = requests.get("https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=" + TWITTER_ACCOUNT + "&count=5", auth=auth)
    tweets = response.json()

    if response.status_code == 200:
        for tweet in tweets:
            tweet_text = tweet["text"]
            tweet_url = f"https://twitter.com/{TWITTER_ACCOUNT}/status/{tweet['id_str']}"
            channel = client.get_channel(DISCORD_CHANNEL_ID)
            await channel.send(f"Novo tweet: {tweet_text}\nLink: {tweet_url}")
    else:
        print(f"Erro ao obter tweets: {tweets}")

discord_token = os.environ.get("DISCORD_TOKEN")
client.run(discord_token)

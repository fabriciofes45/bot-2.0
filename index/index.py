import requests
from dotenv import load_dotenv
import os
import discord

load_dotenv()

TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TWITTER_ACCOUNT = "fabriciofes"  # Substitua pelo seu usuário do Twitter
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = 847553861035884548  # Substitua pelo ID do canal do Discord

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

    headers = {
        "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"
    }

    response = requests.get(f"https://api.twitter.com/2/users/me/tweets", headers=headers)
    data = response.json()

    if response.status_code == 200:
        tweets = data.get("data", [])
        for tweet in tweets:
            tweet_text = tweet["text"]
            tweet_url = f"https://twitter.com/{TWITTER_ACCOUNT}/status/{tweet['id']}"
            channel = client.get_channel(DISCORD_CHANNEL_ID)
            await channel.send(f"Novo tweet: {tweet_text}\nLink: {tweet_url}")
    else:
        print(f"Erro ao obter tweets: {data}")

client.run(DISCORD_TOKEN)

import tweepy
import discord
import os

# Configurações do Twitter
TWITTER_API_KEY = os.environ['TWITTER_API_KEY']
TWITTER_API_SECRET = os.environ['TWITTER_API_SECRET']
TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']
TWITTER_ACCOUNT = "conta_do_twitter"

# Configurações do Discord
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
DISCORD_CHANNEL_NAME = "post"

# Inicialização da API do Twitter
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
twitter_api = tweepy.API(auth)

# Inicialização do cliente do Discord
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot do Discord conectado como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

# Função para buscar os tweets da conta do Twitter e postar no canal do Discord
async def post_tweets():
    channel = discord.utils.get(client.get_all_channels(), name=DISCORD_CHANNEL_NAME)
    
    if channel is not None:
        tweets = twitter_api.user_timeline(screen_name=TWITTER_ACCOUNT, count=5, tweet_mode="extended")
        for tweet in tweets:
            tweet_text = tweet.full_text
            tweet_url = f"https://twitter.com/{TWITTER_ACCOUNT}/status/{tweet.id}"
            await channel.send(f"Novo tweet: {tweet_text}\nLink: {tweet_url}")
    else:
        print(f"Canal '{DISCORD_CHANNEL_NAME}' não encontrado.")

@client.event
async def on_ready():
    print(f'Bot do Discord conectado como {client.user}')
    await post_tweets()  # Chama a função para buscar e postar tweets ao iniciar

# Executa o bot do Discord
client.run(DISCORD_TOKEN)

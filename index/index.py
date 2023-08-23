import os
import discord
from discord.ext import commands

DISCORD_CHANNEL_ID = 123456789012345678  # Substitua pelo ID do canal do Discord
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.channel.id == DISCORD_CHANNEL_ID:
        if message.author == client.user:
            return
        await forward_to_telegram(message)

async def forward_to_telegram(message):
    # Inserir lógica para encaminhar a mensagem para o bot do Telegram aqui
    # Use a biblioteca python-telegram-bot para enviar a mensagem para o canal do Telegram
    pass

def main():
    client.run(os.environ.get("DISCORD_TOKEN"))

if __name__ == "__main__":
    main()

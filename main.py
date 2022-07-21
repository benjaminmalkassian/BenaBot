import configparser
import asyncio
from BenaBotClient import bot

config = configparser.ConfigParser()
config.read("config.ini")
DISCORD_TOKEN = config['DEFAULT']['discord_token']

async def launch():

    # start the client
    async with bot:
        await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    #asyncio.run(launch())
    bot.run(DISCORD_TOKEN)
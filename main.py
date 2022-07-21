import configparser
from BenaBotClient import BenaBotClient

config = configparser.ConfigParser()
config.read("config.ini")
DISCORD_TOKEN = config['DEFAULT']['discord_token']

if __name__ == "__main__":
    bot = BenaBotClient()
    bot.run("DISCORD_TOKEN")
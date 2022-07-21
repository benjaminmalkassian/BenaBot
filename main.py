import configparser
from BenaBotClient import BenaBotClient

config = configparser.ConfigParser()
config.read("config.ini")
DISCORD_TOKEN = config['DEFAULT']['discord_token']
id_channel = "999646444925489232"


if __name__ == "__main__":
    bot = BenaBotClient()
    bot.run("OTk5NjQ3MTQ3Nzc3NTk3NTMy.GX3Mz7.1Nxao3oIdwJtrCoTOivLLRf6xlJFC-17KJq8NM")
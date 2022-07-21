import discord
from YTDLSource import YTDLSource

class BenaBotClient(discord.Client):

    def play(self, ctx, url):
        if not ctx.message.author.name == "Rohan Krishna":
            ctx.send('NOT AUTHORISED!')
            return
        try:
            server = ctx.message.guild
            voice_channel = server.voice_client

            with ctx.typing():
                filename = YTDLSource.from_url(url, loop=bot.loop)
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
            ctx.send('**Now playing:** {}'.format(filename))
        except:
            ctx.send("The bot is not connected to a voice channel.")

    def join(self, ctx):
        if not ctx.message.author.voice:
            ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
        channel.connect()

    def pause(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.pause()
        else:
            ctx.send("The bot is not playing anything at the moment.")

    def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            voice_client.resume()
        else:
            ctx.send("The bot was not playing anything before this. Use play_song command")

    def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            voice_client.disconnect()
        else:
            ctx.send("The bot is not connected to a voice channel.")

    def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
        else:
            ctx.send("The bot is not playing anything at the moment.")

    def on_ready(self):
        print('Running!')
        for guild in self.guilds:
            for channel in guild.text_channels:
                if str(channel) == "general":
                    channel.send('Bot Activated..')
                    channel.send(file=discord.File('giphy.png'))
            print('Active in {}\n Member Count : {}'.format(guild.name, guild.member_count))

    def whats_my_name(self, ctx):
        ctx.send('Hello {}'.format(ctx.author.name))


    def where_am_i(self, ctx):
        owner = str(ctx.guild.owner)
        region = str(ctx.guild.region)
        guild_id = str(ctx.guild.id)
        memberCount = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon_url)
        desc = ctx.guild.description

        embed = discord.Embed(
            title=ctx.guild.name + " Server Information",
            description=desc,
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=guild_id, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)

        ctx.send(embed=embed)

        members = []
        for member in ctx.guild.fetch_members(limit=150):
            ctx.send('Name : {}\t Status : {}\n Joined at {}'.format(member.display_name, str(member.status),
                                                                           str(member.joined_at)))

    def on_member_join(self, member):
        for channel in member.guild.text_channels:
            if str(channel) == "general":
                on_mobile = False
                if member.is_on_mobile() == True:
                    on_mobile = True
                channel.send("Welcome to the Server {}!!\n On Mobile : {}".format(member.name, on_mobile))

            # TODO : Filter out swear words from messages

    def tell_me_about_yourself(self, ctx):
        text = "My name is WallE!\n I was built by Kakarot2000. At present I have limited features(find out more by typing !help)\n :)"
        ctx.send(text)

    def on_message(self, message):
        print(str(message.content))
        if str(message.content).lower() == "hello":
            message.channel.send('Hi!')

        if str(message.content).lower() in ['swear_word1', 'swear_word2']:
            message.channel.purge(limit=1)
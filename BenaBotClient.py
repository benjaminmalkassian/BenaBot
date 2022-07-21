# This example requires the 'message_content' privileged intent to function.

import discord
import asyncio
from YTDLSource import YTDLSource
from discord.ext import commands
from discord.ui import Button, View, Select, InputText, Modal

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(""),
    description='BenaBot Music',
    intents=intents
)
client = discord.Client()
global_volume = 0.2

@bot.command()
async def join(ctx):
    """Joins a voice channel"""
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(ctx.author.voice.channel)
    if ctx.author.voice.channel:
        await ctx.author.voice.channel.connect()
    else:
        await ctx.send("You're not inside a vocal channel")

@bot.command()
async def leave(ctx):
    """Leave the current channel"""
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command()
async def play(ctx, *, url):
    """Streams from a url (same as yt, but doesn't predownload)"""
    try:
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
            ctx.voice_client.source.volume = global_volume
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=player.title))

        await ctx.send(f'Now playing: {player.title}')
    except:
        await ctx.send("Je ne suis pas dans un channel !")

@bot.command()
@commands.is_owner()
async def play_from_modal(ctx, url):
    """Streams from a url (same as yt, but doesn't predownload)"""
    #try:
    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        ctx.voice_client.source.volume = global_volume
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=player.title))

    await ctx.send(f'Now playing: {player.title}')
    #except:
    #    await ctx.send("Je ne suis pas dans un channel !")


@bot.command()
async def pause(ctx):
    """Pause if song is running"""
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@bot.command()
async def resume(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_paused():
        voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")

@bot.command()
async def volume(ctx, volume: int):
    """Changes the player's volume"""
    global global_volume
    global_volume = volume / 100

    if ctx.voice_client:
        ctx.voice_client.source.volume = global_volume
        #await ctx.send(f"Changed volume to {volume}%")

@bot.command()
@commands.is_owner()
async def stop(ctx):
    """Stops and disconnects the bot from voice"""
    await ctx.voice_client.disconnect()

@bot.command()
async def lecteur(ctx):
    button_join = Button(label="Join !", style=discord.ButtonStyle.green)
    async def button_join_callback(interaction):
        await join(ctx)
        await interaction.response.defer()
    button_join.callback = button_join_callback

    button_leave = Button(label="Leave !", style=discord.ButtonStyle.red)
    async def button_leave_callback(interaction):
        await leave(ctx)
        await interaction.response.defer()
    button_leave.callback = button_leave_callback

    button_pause = Button(label="Pause", style=discord.ButtonStyle.grey)
    async def button_pause_callback(interaction):
        await pause(ctx)
        await interaction.response.defer()
    button_pause.callback = button_pause_callback

    button_resume = Button(label="Reprendre", style=discord.ButtonStyle.grey)
    async def button_resume_callback(interaction):
        await resume(ctx)
        await interaction.response.defer()
    button_resume.callback = button_resume_callback

    select_volume = Select(
        placeholder="Changer le volume",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="1%",
                description="Volume a 1%",
                value="1"
            ),
            discord.SelectOption(
                label="5%",
                description="Volume a 5%",
                value="5"
            ),
            discord.SelectOption(
                label="10%",
                description="Volume a 10%",
                value="10"
            ),
            discord.SelectOption(
                label="25%",
                description="Volume a 25%",
                value="25"
            ),
            discord.SelectOption(
                label="50%",
                description="Volume a 50%",
                value="50"
            ),
            discord.SelectOption(
                label="75%",
                description="Volume a 75%",
                value="75"
            ),
            discord.SelectOption(
                label="100%",
                description="Volume a 100%",
                value="100"
            )
        ]
    )
    async def select_callback(interaction):
        await volume(ctx, int(interaction.data['values'][0]))
        await interaction.response.defer()
    select_volume.callback = select_callback

    song_to_play = Modal(InputText(label="Titre", style=discord.InputTextStyle.short), title="Titre")
    async def song_to_play_callback(interaction):
        await interaction.response.defer()
        await join(ctx)
        await asyncio.sleep(2)
        await play_from_modal(ctx, interaction.data['components'][0]['components'][0]['value'])

    song_to_play.callback = song_to_play_callback

    button_modal = Button(label="Choisis ton son", style=discord.ButtonStyle.blurple)
    async def button_modal_callback(interaction):
        await interaction.response.send_modal(song_to_play)
    button_modal.callback = button_modal_callback

    view = View()
    view.add_item(button_join)
    view.add_item(button_leave)
    view.add_item(button_pause)
    view.add_item(button_resume)
    view.add_item(select_volume)
    view.add_item(button_modal)
    await ctx.send("Lecteur !", view=view)

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    """Stops and disconnects the bot from voice"""
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    #await bot.change_presence(status='offline')
    await bot.close()

@play.before_invoke
@play_from_modal.before_invoke
async def ensure_voice(ctx):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()

@bot.event
async def on_ready():
    print("Ready !")

@bot.event
async def on_connect():
    print("Connected !")

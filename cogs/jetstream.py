import discord
from discord.ext import commands
from discord.utils import get
import asyncio
from discord.errors import ClientException
import urllib3

class jetstream(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        try:
            channel = ctx.author.voice.channel
            if channel.name == "Shared Flight Deck" or channel.name == "Shared Cockpit":
                await ctx.send("Can not join a private voice channel")
                return
            await channel.connect()
            await ctx.send("Connected to: " + str(ctx.author.voice.channel.name))
        except AttributeError:
            await ctx.send("You must be in a voice channel!")
            return
        except ClientException:
            await ctx.send("Already connected to a voice channel!")
            return

    @commands.command()
    async def leave(self, ctx):
        try:
            voice_channel = get(self.client.voice_clients, guild=ctx.guild)
            if (ctx.author in voice_channel.channel.members):
                try:
                    await ctx.guild.voice_client.disconnect()
                    await ctx.send("Left the voice channel")
                except:
                    await ctx.send("I am not in a voice channel")
            else:
                await ctx.send("You must be in a voice channel with the bot!")
        except:
            await ctx.send("I am not in a voice channel")

    @commands.command()
    async def forceleave(self, ctx):
        if ctx.message.author.id == 210125985616625674:
            voice_channel = get(self.client.voice_clients, guild=ctx.guild)
            try:
                await ctx.guild.voice_client.disconnect()
                await ctx.send("Bot force left the voice channel")
            except:
                await ctx.send("I am not in a voice channel")
        else:
            await ctx.send("This is a developer only command")

    @commands.command(aliases=['stop', 's'])
    async def pause(self, ctx):
        try:
            voice_channel = get(self.client.voice_clients, guild=ctx.guild)
            if (ctx.author in voice_channel.channel.members):
                if (ctx.voice_client.is_paused() == False):
                    ctx.voice_client.stop()
                    await ctx.send("Jetstream has been stopped!")
                else:
                    await ctx.send("Jetstream is not playing!")
                    print("Paused jetstream")
            else:
                await ctx.send("You must be in a voice channel with the bot!")
        except:
            await ctx.send("The bot is not currently playing anything.")
    
    @commands.command(aliases=['js', 'p', 'play'])
    async def jetstream(self, ctx):
        voice_channel = get(self.client.voice_clients, guild=ctx.guild)
        if (voice_channel == None):
            try:
                channel = ctx.author.voice.channel
                if channel.name == "Shared Flight Deck" or channel.name == "Shared Cockpit":
                    await ctx.send("Can not join a private voice channel")
                    return
                vc = await channel.connect()
                voice_channel = get(self.client.voice_clients, guild=ctx.guild)
            except AttributeError:
                await ctx.send("You must be in a voice channel!")
                return

        url = "http://listen.jetstreamradio.com:8000/autodj"

        loop = self.client.loop or asyncio.get_event_loop()
        
        try:
            ctx.voice_client.play(discord.FFmpegPCMAudio(url), after=lambda e: print('Bot Disconnected, Errors: ', e))
        except ClientException:
            await ctx.send("Already playing Jetstream Radio")
            return
        
        print("Starting jetstream")

        wait = 10 # Seconds

        self.client.loop.create_task(self.checkForUsers(voice_channel, ctx, wait, url))
        
        await ctx.send("Now playing Jet Stream Radio in: " + str(voice_channel.channel.name))
		
    @commands.command(aliases=['tfm'])
    async def truckersfm(self, ctx):
        if ctx.author.id == 214046408792080385:
            return
        voice_channel = get(self.client.voice_clients, guild=ctx.guild)
        if (voice_channel == None):
            try:
                channel = ctx.author.voice.channel
                if channel.name == "Shared Flight Deck" or channel.name == "Shared Cockpit":
                    await ctx.send("Can not join a private voice channel")
                    return
                vc = await channel.connect()
                voice_channel = get(self.client.voice_clients, guild=ctx.guild)
            except AttributeError:
                await ctx.send("You must be in a voice channel!")
                return

        url = "https://live.truckers.fm/"

        loop = self.client.loop or asyncio.get_event_loop()
        
        try:
            ctx.voice_client.play(discord.FFmpegPCMAudio(url), after=lambda e: print('Bot Disconnected, Errors: ', e))
        except ClientException:
            await ctx.send("Already playing TruckersFM Radio")
            return
        
        print("Starting TruckersFM")

        wait = 10 # Seconds

        self.client.loop.create_task(self.checkForUsers(voice_channel, ctx, wait, url))
        
        await ctx.send("Now playing TruckersFM Radio in: " + str(voice_channel.channel.name))

    async def checkForUsers(self, voice_channel, ctx, wait, url):
        while True:
            voice_channel = get(self.client.voice_clients, guild=ctx.guild)
            
            try:
                if len(voice_channel.channel.members) == 1 and voice_channel != None:
                    await ctx.voice_client.disconnect()
                    return

            except:
                pass
            await asyncio.sleep(int(wait))

    @commands.command(aliases=['np'])
    async def nowplaying(self, ctx):
        url = "https://jetstreamradio.com/radioapi.php?requester=web"

        http = urllib3.PoolManager()
        response = http.request('GET', url)
        data = response.data

        data = str(data)[2:][:-1]
        data = data.replace("&amp;", "&")

        embed = discord.Embed(title="Jetstream now playing", description=data, color=0x00ff00)
        embed.set_footer(text="Source https://www.jetstreamradio.com/")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(jetstream(client))
    print("Loaded jetstream")
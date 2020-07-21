import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import time
from discord.utils import get

class autoMod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener() #Auto mod
    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel):
            return
        if message.guild.id != 697092755704250448:
            return
        if message.author in discord.utils.get(message.author.guild.roles, name="Bots").members:
            return
        
        time = datetime.utcnow().replace(microsecond=0)
        msg = message.content.lower().replace("|", "").replace("\'", "").replace("\"", "").replace("\"", "").replace("`", "").replace("~", "").replace("*", "").replace(" ", "")
        bannedwords = ["fuc","fuk","nigg","cunt","cnut","bitch","bich","dick","d1ck","d!ck","dik","pussy","asshole","b1tch","b!tch","shit","penis","penis"]
        for word in bannedwords: #Banned word check
            if word in msg:
                await message.delete()
                for channel in message.guild.channels:
                    if str(channel) == "logs":
                        pfp = message.author.avatar_url
            
                        embed = discord.Embed(title=None, description=f"{message.author.mention} \n" + str(message.author) + "\nMessage: " + str(message.content) + "\nDeleted by automod",   color=0xffd700)
                        embed.set_thumbnail(url=(pfp))
                        embed.set_author(name="Message Deleted", icon_url=(pfp))
                        embed.timestamp = datetime.utcnow().replace(microsecond=0)

                        await channel.send(embed=embed)
                    
                tempmsg = await message.channel.send(f"{message.author.mention} watch your language.")
                await asyncio.sleep(10)
                await tempmsg.delete()
        
        '''
        total = 0 #Caps check
        upper = 0
        for char in message.content:
            if char.isupper():
                upper += 1
            total += 1

        if total <= 8:
            return
        elif (upper/total) >= 0.75:
            await message.delete()
            for channel in message.guild.channels:
                    if str(channel) == "logs":
                        pfp = message.author.avatar_url
            
                        embed = discord.Embed(title=None, description=f"{message.author.mention} \n" + str(message.author) + "\nMessage: " + str(message.content) + "\nDeleted by automod",   color=0xffd700)
                        embed.set_thumbnail(url=(pfp))
                        embed.set_author(name="Message Deleted", icon_url=(pfp))
                        embed.timestamp = datetime.utcnow().replace(microsecond=0)

                        await channel.send(embed=embed)
            tempmsg = await message.channel.send(f"{message.author.mention} watch the caps.")
            await asyncio.sleep(10)
            await tempmsg.delete()
            '''

def setup(client):
    client.add_cog(autoMod(client))
    print("Loaded autoMod")
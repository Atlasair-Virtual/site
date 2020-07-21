import discord
from discord.ext import commands
from discord.utils import get
from datetime import datetime
import asyncio

class mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_role("Staff")
    async def verify(self, ctx, user: discord.Member = None, *args):
        nickname = " ".join(args[:])
        if nickname == "":
            nick = "None"
        else:
            nick = nickname
        
        if nick != "None":
            await ctx.message.delete()
            pilot = get(user.guild.roles, name="Pilot")
            newMember = get(user.guild.roles, name="New Member")
            new_hire = discord.utils.get(ctx.guild.roles, name="New Hire")
            await user.add_roles(pilot)
            await user.add_roles(new_hire)
            await user.remove_roles(newMember)
            await user.edit(nick=nick)
            lounge = self.client.get_channel(697092755989594202)
            
            for channel in ctx.guild.channels:
                if str(channel) == "lounge":
                    await channel.send(f"Welcome {user.mention} to Atlas Air Virtual, please check out #regulations, and if you have any questions don't hesitate to ask")
                elif str(channel) == "logs":
                    pfp = user.avatar_url
                    
                    embed = discord.Embed(title=None, description=f"{user.mention} \n" + str(user), color=0xffd700)
                    embed.set_thumbnail(url=(pfp))
                    embed.set_author(name="Member Verified", icon_url=(pfp))
                    embed.timestamp = datetime.utcnow().replace(microsecond=0)

                    await channel.send(embed=embed)
        else:
            info = embed=discord.Embed(title="Command: !verify", description=f"**Description:** verifies a new user and gives them the pilot role and nickname \n**Usage:** !verify [discord tag] [realname + GTI(ID)] \n**Example:** \n!verify {ctx.author.mention} Collin Koldoff GTI0002", color=0x00ff00)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role("Staff")
    async def kick(self, ctx, user_name: discord.User = None, *args):
        staff = discord.utils.get(ctx.message.author.guild.roles, name="Staff")
        bots = discord.utils.get(ctx.message.author.guild.roles, name="Bots")
        reason = " ".join(args[:])
        if reason == "":
            reason = "No reason given"

        if user_name != None:
            if user_name in staff.members:
                await ctx.send("I can not kick a staff member")
            elif user_name in bots.members:
                await ctx.send("I can not kick a bot")
            else:
                await ctx.message.delete()
                await user_name.send("You have been kicked from Atlas Air Virtual. Reason: " + reason)

                pfp = user_name.avatar_url
                
                embed = discord.Embed(title=None, description=f"{user_name.mention} \n" + str(user_name) + "\n Kicked by: " + str(ctx.author) + "\n Reason: " + reason, color=0xffd700)
                embed.set_thumbnail(url=(pfp))
                embed.set_author(name="Member Kicked", icon_url=(pfp))
                embed.timestamp = datetime.utcnow().replace(microsecond=0)

                for channel in ctx.guild.channels:
                    if str(channel) == "logs":
                        await channel.send(embed=embed)

                await ctx.guild.kick(user_name)

                tempmsg = await ctx.send(f"{user_name.mention} has been kicked")
                await asyncio.sleep(10)
                await tempmsg.delete()
        else:
            embed = discord.Embed(title="Command: !kick", description=f"**Description:** Kicks a member from the server \n**Usage:** !kick [discord tag] [reason(optional)] \n**Example:** \n!kick {ctx.author.mention} you are stupid", color=0x00ff00)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role("Staff")
    async def ban(self, ctx, user_name: discord.User = None, *args):
        staff = discord.utils.get(ctx.message.author.guild.roles, name="Staff")
        bots = discord.utils.get(ctx.message.author.guild.roles, name="Bots")
        reason = " ".join(args[:])
        if reason == "":
            reason = "No reason given"

        if user_name != None:
            if user_name in staff.members:
                await ctx.send("I can not ban a staff member")
            elif user_name in bots.members:
                await ctx.send("I can not ban a bot")
            else:
                await ctx.message.delete()
                await user_name.send("You have been banned from Atlas Air Virtual. Reason: " + reason)

                pfp = user_name.avatar_url
                
                embed = discord.Embed(title=None, description=f"{user_name.mention} \n" + str(user_name) + "\n Banned by: " + str(ctx.author) + "\n Reason: " + reason, color=0xffd700)
                embed.set_thumbnail(url=(pfp))
                embed.set_author(name="Member Banned", icon_url=(pfp))
                embed.timestamp = datetime.utcnow().replace(microsecond=0)

                for channel in ctx.guild.channels:
                    if str(channel) == "logs":
                        await channel.send(embed=embed)

                await ctx.guild.ban(user_name, reason=reason, delete_message_days=0)
                tempmsg = await ctx.send(f"{user_name.mention} has been banned")
                await asyncio.sleep(10)
                await tempmsg.delete()
        else:
            embed = discord.Embed(title="Command: !ban", description=f"**Description:** Bans a member from the server \n**Usage:** !ban [discord tag] [reason(optional)] \n**Example:** \n!ban {ctx.author.mention} you are stupid", color=0x00ff00)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role("Staff")
    async def mute(self, ctx, user_name: discord.Member = None, *args):
        staff = discord.utils.get(ctx.message.author.guild.roles, name="Staff")
        bots = discord.utils.get(ctx.message.author.guild.roles, name="Bots")
        muted = discord.utils.get(ctx.message.author.guild.roles, name="Muted")
        reason = " ".join(args[:])
        if reason == "":
            reason = "No reason given"

        if user_name != None:
            if user_name in staff.members:
                await ctx.send("I can not mute a staff member")
            elif user_name in bots.members:
                await ctx.send("I can not mute a bot")
            elif muted in user_name.roles:
                await ctx.send("That user is already muted")
            else:
                await ctx.message.delete()
                await user_name.send("You have been muted in Atlas Air Virtual. Reason: " + reason)

                pfp = user_name.avatar_url
                
                embed = discord.Embed(title=None, description=f"{user_name.mention} \n" + str(user_name) + "\n Muted by: " + str(ctx.author) + "\n Reason: " + reason, color=0xffd700)
                embed.set_thumbnail(url=(pfp))
                embed.set_author(name="Member Muted", icon_url=(pfp))
                embed.timestamp = datetime.utcnow().replace(microsecond=0)

                for channel in ctx.guild.channels:
                    if str(channel) == "logs":
                        await channel.send(embed=embed)

                await user_name.add_roles(muted)
                await user_name.edit(mute=True)

                tempmsg = await ctx.send(f"{user_name.mention} has been muted")
                await asyncio.sleep(10)
                await tempmsg.delete()
        else:
            embed = discord.Embed(title="Command: !mute", description=f"**Description:** Prevents a member from speaking in voice or using a text channel \n**Usage:** !mute [discord tag] [reason(optional)] \n**Example:** \n!mute {ctx.author.mention} you are stupid", color=0x00ff00)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role("Staff")
    async def unmute(self, ctx, user_name: discord.Member = None, *args):
        staff = discord.utils.get(ctx.message.author.guild.roles, name="Staff")
        bots = discord.utils.get(ctx.message.author.guild.roles, name="Bots")
        muted = discord.utils.get(ctx.message.author.guild.roles, name="Muted")
        reason = " ".join(args[:])
        if reason == "":
            reason = "No reason given"

        if user_name != None:
            if muted in user_name.roles == False:
                await ctx.send("That user is not muted")
            else:
                await ctx.message.delete()
                await user_name.send("You have been unmuted in Atlas Air Virtual")

                pfp = user_name.avatar_url
                
                embed = discord.Embed(title=None, description=f"{user_name.mention} \n" + str(user_name) + "\n Unmuted by: " + str(ctx.author) + "\n Reason: " + reason, color=0xffd700)
                embed.set_thumbnail(url=(pfp))
                embed.set_author(name="Member Unmuted", icon_url=(pfp))
                embed.timestamp = datetime.utcnow().replace(microsecond=0)

                for channel in ctx.guild.channels:
                    if str(channel) == "logs":
                        await channel.send(embed=embed)

                await user_name.remove_roles(muted)
                await user_name.edit(mute=False)

                tempmsg = await ctx.send(f"{user_name.mention} has been unmuted")
                await asyncio.sleep(10)
                await tempmsg.delete()
        else:
            embed = discord.Embed(title="Command: !unmute", description=f"**Description:** Unmutes a member \n**Usage:** !unmute [discord tag] [reason(optional)] \n**Example:** \n!unmute {ctx.author.mention} you are stupid", color=0x00ff00)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role("Staff")
    async def clear(self, ctx, amount=0):
        if (amount == 0):
            info = embed=discord.Embed(title="Command: !clear", description="**Description:** Cleares a defined number of messages in the current channel \n**Usage:** !clear [number to clear] \n**Example:** \n!clear 50", color=0x00ff00)
            await ctx.send(embed=embed)
        elif (amount >= 100):
            value = amount
            while (amount >= 100):
                messages = []
                if (amount >= 100):
                    number = 100
                elif (amount < 100):
                    number = int(amount) + 1
                channel = ctx.message.channel
                messages = await channel.history(limit=number).flatten()
                await channel.delete_messages(messages)
                amount = amount - 100
                print(str(value) + " Messages Deleted")
        elif (amount > 0):
            messages = []
            number = int(amount) + 1
            channel = ctx.message.channel
            messages = await channel.history(limit=number).flatten()
            await channel.delete_messages(messages)
            print(str(amount) + " Messages Deleted")

    @commands.command()
    @commands.has_role("Staff")
    async def say(self, ctx, *, args=None):
        await ctx.message.delete()
        await ctx.send(args)

def setup(client):
    client.add_cog(mod(client))
    print("Loaded mod")
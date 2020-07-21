import discord
from discord.ext import commands
from discord.utils import get
from datetime import datetime
import traceback
import asyncio
import os
import urllib.request
from urllib.request import urlopen
import urllib3
import platform

TOKEN = "Njk3MDkzNzYyMzU0MTE4Nzc4.XpT5XQ.W6T6tDkj9Ku7f8d1Z6uLWM-mbK0"

if platform.system() == "Windows":
    client = commands.Bot(command_prefix='>', case_insensitive=True)
elif platform.system() == "Linux":
    client = commands.Bot(command_prefix='!', case_insensitive=True)

client.remove_command("help")

@client.command()
async def help(ctx, args=None):
    if args != None:
        args = str(args).lower()
    if args == "mod":
        staff = discord.utils.get(ctx.message.author.guild.roles, name="Staff")
        if ctx.author in staff.members:
            embed=discord.Embed(title="Staff Commands Menu", description="Use a command without arguments for more info", color=0x00ff00)
            embed.add_field(name="!verify", value="Verifies a member and assigns the pilot role", inline=False)
            embed.add_field(name="!kick", value="Removes a member from the server", inline=False)
            embed.add_field(name="!ban", value="Bans a member from the server", inline=False)
            embed.add_field(name="!mute", value="Prevents a user from sending messages or talking in voice chat", inline=False)
            embed.add_field(name="!unmute", value="Unmutes a member", inline=False)
            embed.add_field(name="!clear", value="Removes a defined number of messages from the channel", inline=False)
            embed.add_field(name="!reload", value="Reloads the defined cog (automod, avbot, info, jetstream, mod)", inline=False)
            embed.add_field(name="!rall", value="Reloads all cogs", inline=False)
            await ctx.send(embed=embed)
    elif args == "info":
        embed=discord.Embed(title="Info Commands Menu", description="Use a command without arguments for more info", color=0x00ff00)
        embed.add_field(name="!help info", value="Displays this window", inline=False)
        embed.add_field(name="!ping", value="Returns the latency of the bot, used to verify bot operational", inline=False)
        embed.add_field(name="!downloads", value="Sends the link to the Atlas Air Virtual download page", inline=False)
        embed.add_field(name="!staff", value="Gives a list of all staff members as well as their VA emails", inline=False)
        embed.add_field(name="!web, !site, !crew", value="Sends link to crew page for easy access", inline=False)
        embed.add_field(name="!regs, !reg", value="Sends a direct link to the airline regulations for easy access", inline=False)
        embed.add_field(name="!tutorial", value="Sends a direct link to the tutorial video for easy access", inline=False)
        embed.add_field(name="!github, !git", value="Sends a direct link to the github issues page. Use this to report bugs/issues", inline=False)
        embed.add_field(name="!info", value="Displays bot information as well as how to report bug fixes or give ideas", inline=False)
        embed.add_field(name="!737", value="Sends a direct link to the Atlas Air Virtual 737 checklist", inline=False)
        embed.add_field(name="!767", value="Sends a direct link to the Atlas Air Virtual 767 checklist and Normal Procedures", inline=False)
        embed.add_field(name="!747", value="Sends a direct link to the Atlas Air Virtual 747 checklist", inline=False)
        embed.add_field(name="!checklists", value="Sends a direct link to all of the Atlas Air Virtual checklists", inline=False)
        await ctx.send(embed=embed)
    elif args == "avbot":
        embed=discord.Embed(title="AvBot Commands Menu", description="Use a command without arguments for more info", color=0x00ff00)
        embed.add_field(name="!help avbot", value="Displays this window", inline=False)
        embed.add_field(name="!metar", value="Grabs the metar for a specified airport and decodes it", inline=False)
        embed.add_field(name="!rawmetar", value="Grabs the raw metar for a specified airport or airports separated by spaces", inline=False)
        embed.add_field(name="!zulu", value="Shows current zulu time", inline=False)
        embed.add_field(name="!route", value="Sends a link for the flight aware IFR Route Analyzer for the defined route", inline=False)
        embed.add_field(name="!vatsim", value="Grabs the information for the defined callsign on the vatsim network", inline=False)
        embed.add_field(name="!acars", value="Lists all of the current Atlas Air Virtual Pilots that are flying", inline=False)
        embed.add_field(name="!datis", value="Grabs and sends the Digital ATIS for the defined airport", inline=False)
        embed.add_field(name="!charts", value="Sends a link for the FAA charts for the specified airport", inline=False)
        embed.add_field(name="!taf", value="Grabs the taf for a specified airport and decodes it", inline=False)
        embed.add_field(name="!brief", value="Displays the METAR, TAF, and Charts for up to 3 airports", inline=False)
        await ctx.send(embed=embed)
    elif args == "jetstream":
        embed=discord.Embed(title="Jetstream Commands Menu", description="Use a command without arguments for more info", color=0x00ff00)
        embed.add_field(name="!help jetstream", value="Displays this window", inline=False)
        embed.add_field(name="!join", value="Joins the users voice channel", inline=False)
        embed.add_field(name="!pause, !stop, !s", value="Stops the jetstream radio", inline=False)
        embed.add_field(name="!jetstream, !js", value="Joins the users voice channel and streams jetstream radio", inline=False)
        embed.add_field(name="!np", value="Shows the current song playing on Jetstream Radio", inline=False)
        await ctx.send(embed=embed)
    elif args == None:
        embed=discord.Embed(title="Help Menu", description="Use one of the below commands to get info on a specific module", color=0x00ff00)
        embed.add_field(name="!help", value="Displays this window", inline=False)
        
        if ctx.guild.id == 697092755704250448:
            embed.add_field(name="!help info", value="List of commands for info about the airline", inline=False)
        
        embed.add_field(name="!help avbot", value="List of aviation related commands", inline=False)
        embed.add_field(name="!help jetstream", value="List of commands to work the Jetstream Radio", inline=False)
        staff = discord.utils.get(ctx.message.author.guild.roles, name="Staff")
        if ctx.guild.id == 697092755704250448:
            if ctx.author in staff.members:
                embed.add_field(name="!help mod", value="Staff only commands", inline=False)
        await ctx.send(embed=embed)

async def auto_roles(wait):
    await client.wait_until_ready()
    while True:
        server = client.get_guild(697092755704250448)

        pilot = discord.utils.get(server.roles, name="Pilot")
        inactive = discord.utils.get(server.roles, name="Inactive")
        loa = discord.utils.get(server.roles, name="LOA")

        new_hire = discord.utils.get(server.roles, name="New Hire")
        fo = discord.utils.get(server.roles, name="First Officer")
        senior_fo = discord.utils.get(server.roles, name="Senior First Officer")
        captain = discord.utils.get(server.roles, name="Captain")
        senior_captain = discord.utils.get(server.roles, name="Senior Captain")

        url = "https://crew.atlasair-virtual.com/index.php/datafeeds/pilotdata"
            
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        rawdata = response.data

        try:
            while ("</Pilot>" in str(rawdata)):
                data = str(rawdata)
 
                data = data.partition("<Pilot pilotid=")[2].partition("\">")[2]
                  
                rawdata = data.split("</Pilot>", 1)[1]
                data = data.split("</Pilot>", 1)[0]
                data = data.replace("><", ">\n<")
                    
                nickname = data.partition("<nickname>")[2].split("</nickname>", 1)[0]
                name = data.partition("<name>")[2].split("</name>", 1)[0]
                hub = data.partition("<hub>")[2].split("</hub>", 1)[0]
                retired = data.partition("<retired>")[2].split("</retired>", 1)[0]
                rank = data.partition("<rank>")[2].split("</rank>", 1)[0]
                
                member = None

                for user in server.members:
                    if str(nickname) in str(user.nick):
                        member = user
                        break
                if member != None:
                    if rank == "6" and member not in senior_captain.members:
                        await member.add_roles(senior_captain)
                        if member in fo.members:
                            await member.remove_roles(fo)
                        if member in senior_fo.members:
                            await member.remove_roles(senior_fo)
                        if member in captain.members:
                            await member.remove_roles(captain)
                        if member in new_hire.members:
                            await member.remove_roles(new_hire)
                    elif rank == "4" and member not in captain.members:
                        await member.add_roles(captain)
                        if member in new_hire.members:
                            await member.remove_roles(new_hire)
                        if member in fo.members:
                            await member.remove_roles(fo)
                        if member in senior_fo.members:
                            await member.remove_roles(senior_fo)
                        if member in senior_captain.members:
                            await member.remove_roles(senior_captain)
                    elif rank == "5" and member not in senior_fo.members:
                        await member.add_roles(senior_fo)
                        if member in new_hire.members:
                            await member.remove_roles(new_hire)
                        if member in fo.members:
                            await member.remove_roles(fo)
                        if member in captain.members:
                            await member.remove_roles(captain)
                        if member in senior_captain.members:
                            await member.remove_roles(senior_captain)
                    elif rank == "2" and member not in fo.members:
                        await member.add_roles(fo)
                        if member in new_hire.members:
                            await member.remove_roles(new_hire)
                        if member in senior_fo.members:
                            await member.remove_roles(senior_fo)
                        if member in captain.members:
                            await member.remove_roles(captain)
                        if member in senior_captain.members:
                            await member.remove_roles(senior_captain)
                    elif rank == "1" and member not in new_hire.members:
                        await member.add_roles(new_hire)
                        if member in fo.members:
                            await member.remove_roles(fo)
                        if member in senior_fo.members:
                            await member.remove_roles(senior_fo)
                        if member in captain.members:
                            await member.remove_roles(captain)
                        if member in senior_captain.members:
                            await member.remove_roles(senior_captain)

                    if str(retired) == "0" and (member in inactive.members or member in loa.members):
                        await member.add_roles(pilot)
                        await member.remove_roles(inactive)
                        await member.remove_roles(loa)
                    
                    elif str(retired) == "1" and (member in pilot.members or member in loa.members):
                        await member.add_roles(inactive)
                        await member.remove_roles(pilot)
                        await member.remove_roles(loa)

                    elif str(retired) == "3" and (member not in loa.members or member not in pilot.members):
                        await member.add_roles(loa)
                        await member.add_roles(pilot)
                        await member.remove_roles(inactive)

                
        except:
            pass

        await asyncio.sleep(int(wait))

@client.event
async def on_member_join(member):
    if member.guild.id == 697092755704250448:
        role = get(member.guild.roles, name="New Member")
        await member.add_roles(role)
        for channel in member.guild.channels:
            if str(channel) == "welcome":
                await channel.send(f"Welcome to the Atlas Air Virtual {member.mention}. \nAfter you have registered on out website, please put your full name, Pilot ID (GTI####), and vatsim CID in this channel and our staff team will verify you as soon as possible. \nWhile you wait, please be sure to read the #regulations channel and ask any questions if you have them.")
            elif str(channel) == "logs":
                pfp = member.avatar_url
                
                embed = discord.Embed(title=None, description=f"{member.mention} \n" + str(member), color=0xffd700)
                embed.set_thumbnail(url=(pfp))
                embed.set_author(name="Member Joined", icon_url=(pfp))
                embed.timestamp = datetime.utcnow().replace(microsecond=0)

                await channel.send(embed=embed)

@client.event
async def on_member_remove(member):
    if member.guild.id == 697092755704250448:
        for channel in member.guild.channels:
            if str(channel) == "logs":
                pfp = member.avatar_url
                
                embed = discord.Embed(title=None, description=f"{member.mention} \n" + str(member), color=0xffd700)
                embed.set_thumbnail(url=(pfp))
                embed.set_author(name="Member Left", icon_url=(pfp))
                embed.timestamp = datetime.utcnow().replace(microsecond=0)

                await channel.send(embed=embed)

@client.event
async def on_ready():
    logs = client.get_channel(697092756279001170)
    print('Ready!')
    await client.change_presence(activity=discord.Game(name="Atlas Air Virtual ACARS"))
    open('log.txt', 'w').close()

if client.command_prefix != '>':
    @client.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            print("Invalid command used")
        elif isinstance(error, commands.errors.MissingRole):
            tempmsg = await ctx.send("Insufficent Permissions")
            await asyncio.sleep(10)
            await tempmsg.delete()
        elif isinstance(error, commands.MissingRequiredArgument):
            tempmsg = await ctx.send("Missing Arguments")
            await asyncio.sleep(10)
            await tempmsg.delete()
        else:
            print(error)

@client.command()
@commands.has_role("Staff")
async def servers(ctx):
    if ctx.guild.name == "Atlas Air Virtual":
        await ctx.send('Servers connected to:')
        for guild in client.guilds:
            await ctx.send(guild.name)

@client.command()
@commands.has_role("Staff")
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")

@client.command()
@commands.has_role("Staff")
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
@commands.has_role("Staff")
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    print(f"Unloaded " + extension)

@client.command()
@commands.has_role("Staff")
async def rall(ctx):
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            client.unload_extension(f"cogs.{file[:-3]}")
            client.load_extension(f"cogs.{file[:-3]}")

    await ctx.send("All cogs reloaded")

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        client.load_extension(f"cogs.{file[:-3]}")

wait = 1*60 # Minutes to seconds

client.loop.create_task(auto_roles(wait))

client.run(TOKEN)
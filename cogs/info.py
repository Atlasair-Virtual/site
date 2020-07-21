import discord
from discord.ext import commands

class info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! ``{round(self.client.latency * 1000, 2)}ms``')

    @commands.command()
    async def downloads(self, ctx):
        await ctx.send("Atlas Air Virtual Downloads: <https://crew.atlasair-virtual.com/index.php/downloads>")

    @commands.command()
    async def staff(self, ctx):
        embed = discord.Embed(title=None, description="Jacob Singer GTI0001 - jacob@atlasair-virtual.com \nCollin Koldoff GTI0002 - collin@atlasair-virtual.com \nWebmaster (Anything Web Related) - webmaster@atlasair-virtual.com", color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command(aliases=['site', 'crew'])
    async def web(self, ctx):
        await ctx.send("Front Page: <https://atlasair-virtual.com/>")
        await ctx.send("Crew Center: <https://crew.atlasair-virtual.com/>")

    @commands.command(aliases=['regs', 'reg'])
    async def sop(self, ctx):
        await ctx.send("<https://atlasair-virtual.com/downloads/Atlas%20Air%20Virtual%20Regulations.pdf>")

    @commands.command()
    async def bug(self, ctx):
        await ctx.send("When reporting a bug found while using our website or SmartCARS please be thorough and provide as much detail as possible. This includes what actions were used to create this error, images of errors, steps to replicate the errors, logs from smartCARS found at \"C:\\Program Files (x86)\\smartCARS\\888\\en-US\\logs\", as well as any errors found in your browser console if applicable.")

    @commands.command()
    async def tutorial(self, ctx):
        await ctx.send("https://www.youtube.com/watch?v=Ad64GV3w_As")

    @commands.command(aliases=['git'])
    async def github(self, ctx):
        await ctx.send("https://github.com/Atlasair-Virtual/site/issues")

    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(title=None, description="This bot has been developed by Collin Koldoff (GTI0002) for Atlas Air Virtual.\nTo suggest changes/additions or to report bugs please private message Collin or send an email to collin@atlasair-virtual.com.", color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command(aliases=['767'])
    async def aav767(self, ctx):
        await ctx.send("<https://atlasair-virtual.com/downloads/Atlas%20Air%20Virtual%20Boeing%20767%20Normal%20Procedures.pdf>")
        await ctx.send("<https://atlasair-virtual.com/downloads/Atlas%20Air%20Virtual%20767%20Checklist.pdf>")

    @commands.command(aliases=['747'])
    async def aav747(self, ctx):
        await ctx.send("https://atlasair-virtual.com/downloads/Atlas%20Air%20Virtual%20747%20Checklist.pdf")
    
    @commands.command(aliases=['737'])
    async def aav737(self, ctx):
        await ctx.send("https://atlasair-virtual.com/downloads/Atlas%20Air%20Virtual%20737%20Checklist.pdf")

    @commands.command()
    async def checklists(self, ctx):
        await ctx.send("747 Checklist: https://atlasair-virtual.com/downloads/Atlas%20Air%20Virtual%20747%20Checklist.pdf")
        await ctx.send("767 Checklist: https://atlasair-virtual.com/downloads/Atlas%20Air%20Virtual%20767%20Checklist.pdf")
        await ctx.send("737 Checklist: https://atlasair-virtual.com/downloads/Atlas%20Air%20Virtual%20737%20Checklist.pdf")


def setup(client):
    client.add_cog(info(client))
    print("Loaded info")
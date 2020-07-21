import discord
from discord.ext import commands
from datetime import datetime
from datetime import date
from datetime import timedelta
import asyncio
import time
import urllib3
import xmltodict
import sys
import traceback

class avBot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def metar(self, ctx, icao=None):
        if icao == None:
            embed = discord.Embed(title="Command: !metar", description=f"**Description:** Fetches the metar for a specific airport \n**Usage:** !metar [icao] \n**Example:** \n!metar KORD", color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            url = "https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=" + icao + "&hoursBeforeNow=2&mostRecent=true"

            http = urllib3.PoolManager()
            response = http.request('GET', url)
            data = response.data

            data = str(data)
            metar = data.partition("<raw_text>")[2]
            metar = metar.split("</", 1)[0]
            try:
                icao = icao.upper()
                time = data.partition("<observation_time>")[2].split("</", 1)[0].replace("T", " ")
                winddir = data.partition("<wind_dir_degrees>")[2].split("</", 1)[0].zfill(3)
                windspd = data.partition("<wind_speed_kt>")[2].split("</", 1)[0]
                windgust = data.partition("<wind_gust_kt>")[2].split("</", 1)[0]
                try:
                    temp = str(round(float(data.partition("<temp_c>")[2].split("</", 1)[0]))) + " Degrees Celsius "
                except:
                    temp = "Unknown"
                try:
                    dew = str(round(float(data.partition("<dewpoint_c>")[2].split("</", 1)[0]))) + " Degrees Celsius "
                except:
                    dew = "Unknown"
                vis = metar.partition("KT ")[2].split(" ", 1)[0]
                if vis == "9999":
                    vis = "10"
                else:
                    vis = data.partition("<visibility_statute_mi>")[2].split("</", 1)[0]
				
                press = metar.partition("/" + str(round(float(data.partition("<dewpoint_c>")[2].split("</", 1)[0]))) + " ")[2]
                qnh = ""
                altim = ""
                if(press.startswith("Q")):
                    press = press.replace("Q", "")
                    for char in press:
                        if(char.isdigit()):
                            qnh = qnh + char
                        else:
                            break
                    press = "**QNH:** " + qnh + " hPa"
                
                elif(press.startswith("A")):
                    press = press.replace("A", "")
                    for char in press:
                        if(char.isdigit()):
                            altim = altim + char
                        else:
                            break
                    press = "**Altimeter:** " + altim + " inHg"

                else:
                    press = "Pressure Unknown"

                precip = data.partition("<wx_string>")[2].split("</wx")[0].split(" ")


                sky = str(data.partition("<sky_condition")[2].rsplit("</METAR")[0])
                num = sky.count("sky_cover")

                if winddir != "000":
                    wind = winddir + " Degrees, " + windspd + " Knots"
                    if windgust.isdigit():
                        wind = wind + ", Gusting to " + windgust + " Knots"
                elif winddir == "VRB":
                    wind = "Variable at " + windspd + " Knots"
                else:
                    wind = "Calm"

                skycover = []
                coveralt = []
                skycon = ""
                index = -1
                for x in range(sky.count("sky_cover")):
                    skycover.append(sky.partition("sky_cover=\"")[2].split("\"")[0])
                    sky = sky.replace("cover", "", 1)

                for x in range(sky.count("cloud_base_ft_agl")):
                    coveralt.append(sky.partition("cloud_base_ft_agl=\"")[2].split("\"")[0])
                    sky = sky.replace("cloud_base_ft_agl", "", 1)

                for item in precip:
                    if "-" in item:
                        skycon = skycon + "Light "
                    elif "+" in item:
                        skycon = skycon + "Heavy "
                    if "MI" in item:
                        skycon = skycon + "Shallow "
                    elif "BC" in item:
                        skycon = skycon + "Patches "
                    elif "BL" in item:
                        skycon = skycon + "Blowing "
                    elif "DR" in item:
                        skycon = skycon + "Low drifting "
                    elif "TS" in item:
                        skycon = skycon + "Thunderstorm "
                    elif "FZ" in item:
                        skycon = skycon + "Freezing "
                    
                    if "SH" in item:
                        skycon = skycon + "Showers, "
                    elif "PR" in item:
                        skycon = skycon + "Partial, "
                    elif "RA" in item:
                        skycon = skycon + "Rain, "
                    elif "SN" in item:
                        skycon = skycon + "Snow, "
                    elif "IC" in item:
                        skycon = skycon + "Ice Crystals, "
                    elif "GR" in item:
                        skycon = skycon + "Hail, "     
                    elif "UP" in item:
                        skycon = skycon + "Unknown Precipitation, "
                    elif "DZ" in item:
                        skycon = skycon + "Drizzle, "
                    elif "SG" in item:
                        skycon = skycon + "Snow Grains, "
                    elif "PL" in item:
                        skycon = skycon + "Ice Pellets, "
                    elif "GS" in item:
                        skycon = skycon + "Snow Pellets, "
                    
                    if "FG" in item:
                        skycon = skycon + "Fog, "
                    elif "VA" in item:
                        skycon = skycon + "Volcanic Ash, "
                    elif "BR" in item:
                        skycon = skycon + "Mist, "
                    elif "HZ" in item:
                        skycon = skycon + "Haze, "
                    elif "DU" in item:
                        skycon = skycon + "Widespread Dust, "
                    elif "FU" in item:
                        skycon = skycon + "Smoke, "

                if "CLR" in skycover[0]:
                    skycon = "Clear"
                elif "CAVOK" in skycover[0]:
                    skycon = "Clouds and Visibility OK"
                elif "SKC" in skycover[0]:
                    skycon = "Sky Clear"
                else:
                    for i in skycover:
                        index = index + 1
                        skycover = str(skycover).replace("\'", "").replace("[", "").replace("]", "")
                        if index != 0:
                            sky = sky + ", "
                        if str(i) == "FEW":
                            cover = "Few Clouds"
                        elif str(i) == "SCT":
                            cover = "Scattered Clouds"
                        elif str(i) == "BKN":
                            cover = "Broken Ceiling"
                        elif str(i) == "OVC":
                            cover = "Overcast Ceiling"
                        else:
                            cover = "Error"

                        skycon = skycon + cover + " at " + coveralt[index] + " Feet AGL, "

                    skycon = skycon[:-2]

                rules = data.partition("<flight_category>")[2].split("</", 1)[0]
            
                embed = discord.Embed(title="METAR for " + icao, description=None, color=0x091d60)
                embed.add_field(name="Raw Report", value=metar, inline=False)
                embed.add_field(name="Readable Report", value="**Station:** " + icao + "\n**Observed at:** " + time + "\n**Wind:** " + wind + "\n**Visibility:** " + vis + " Statute Miles \n**Temperature:** " + temp + "\n**Dew Point:** " + dew + "\n" + press + "\n**Sky Conditions:** " + skycon + "\n**Flight Rules:** " + rules, inline=False)
                embed.set_footer(text="This is not a source for an official weather briefing. Please obtain a weather briefing from the appropriate agency.")
                await ctx.send(embed=embed)
            
            except Exception:
                embed = discord.Embed(title="Could not find metar for " + icao, color=0x00ff00)
                embed.set_footer(text="Source: faa.gov")
                await ctx.send(embed=embed)

    @commands.command()
    async def rawmetar(self, ctx, *, icao=None):
        if icao == None:
            embed = discord.Embed(title="Command: !rawmetar", description=f"**Description:** Fetches the raw metar for one or multiple airports \n**Usage:** !rawmetar [icao] \n**Example:** \n!rawmetar KORD\n!rawmetar KORD KBOS KJFK KMIA", color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            icao = icao.split(" ")
            for apt in icao:    
                url = "https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=" + apt + "&hoursBeforeNow=1"

                http = urllib3.PoolManager()
                response = http.request('GET', url)
                data = response.data

                data = str(data)
                metar = data.partition("<raw_text>")[2]
                metar = metar.split("</", 1)[0]
                try:
                    await ctx.send(metar)
                except:
                    embed = discord.Embed(title="Could not find metar for " + apt, color=0x00ff00)
                    embed.set_footer(text="Source: faa.gov")
                    await ctx.send(embed=embed)
            
    @commands.command(aliases=['utc', 'z'])
    async def zulu(self, ctx):
        time = datetime.utcnow().replace(microsecond=0)
        embed=discord.Embed(title="Current Zulu Time", description=str(time).replace("-", "/")[5:] + " Z", color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command()
    async def route(self, ctx, dep=None, arr=None):
        if arr != None:
            await ctx.send("<https://flightaware.com/analysis/route.rvt?origin=" + dep + "&destination=" + arr + ">")
        else:
            embed = discord.Embed(title="Command: !route", description=f"**Description:** Sends a link for the flight aware IFR Route Analyzer for the defined route \n**Usage:** !route [dep] [arr] \n**Example:** \n!route KORD KBOS", color=0x00ff00)
            await ctx.send(embed=embed)
    
    @commands.command() 
    async def chartsfaa(self, ctx, icao=None):
        if icao != None:
            icao = icao.upper()
            if (icao.startswith("K") or icao.startswith("PA") or icao.startswith("PF") or icao.startswith("PH") or icao.startswith("PG") or icao.startswith("TJ") or icao.startswith("TI")):
                airac = self.getAirac()
                await ctx.send("<https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/dtpp/search/results/?cycle=" + airac + "&ident=" + icao + ">")
            else:
                await ctx.send("The FAA charts database does not contain charts for " + icao)
        else:
            embed = discord.Embed(title="Command: !charts", description=f"**Description:** Sends a link for the charts for the defined airport \n**Usage:** !charts [icao] \n**Example:** \n!charts KBOS", color=0x00ff00)
            await ctx.send(embed=embed)

    def getAirac(self):
        today = date.today()
        day = date(2020, 1, 2)
        year = 2020
        cycle = 1
        while (day < today):
            day = day + timedelta(days=28)
            cycle = cycle + 1
            if (today < day and today > day - timedelta(days=28)):
                day = day - timedelta(days=28)
                cycle = cycle - 1
                break
            if (day.year > year):
                year = year + 1
                cycle = 1
        airac = str(year)[-2:] + str(cycle).zfill(2)
        return airac

    @commands.command() 
    async def charts(self, ctx, icao=None):
        if icao != None:
            icao = icao.upper()
            embed = discord.Embed(title="Charts for " + icao, description="https://chartfox.org/" + icao, color=0x00ff00)
            embed.set_footer(text="Charts brought to you by https://chartfox.org/")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Command: !charts", description=f"**Description:** Sends a link for the charts for the defined airport \n**Usage:** !charts [icao] \n**Example:** \n!charts KBOS", color=0x00ff00)
            await ctx.send(embed=embed)

    @commands.command()
    async def vatsim(self, ctx, callsign=None):
        if callsign != None:
            callsign = callsign.upper()
            url = "http://cluster.data.vatsim.net/vatsim-data.txt"

            http = urllib3.PoolManager()
            response = http.request('GET', url)
            data = response.data
            if len(callsign) > 4 or len(callsign) == 4 or len(callsign) < 4:
                try:
                    data = callsign + str(data).split(callsign, 1)[1].rsplit("\\n")[0]
                    
                    data = data.split(":")

                    if (data[3] == "PILOT"):
                        callsign = data[0]
                        cid = data[1]
                        name = data[2]
                        type = data[3]
                        lat = data[5]
                        lng = data[6]
                        altitude = data[7]
                        gs = data[8]
                        acft = data[9]
                        dep = data[11]
                        arr = data[13]
                        plncruise = data[12]
                        xpndr = data[17]
                        remarks = data[29]
                        route = data[30]
                        embed = discord.Embed(title="Vatsim " + type + ": " + callsign + " " + dep + "-" + arr, color=0x00ff00)
                        embed.add_field(name="Callsign", value=callsign)
                        embed.add_field(name="Pilot", value=name)
                        embed.add_field(name="CID", value=cid)
                        embed.add_field(name="Departure", value=dep)
                        embed.add_field(name="Arrival", value=arr)
                        embed.add_field(name="Transponder", value=xpndr)
                        embed.add_field(name="Latitude", value=lat)
                        embed.add_field(name="Longitude", value=lng)
                        embed.add_field(name="Altitude", value=altitude)
                        embed.add_field(name="Groundspeed", value=gs)
                        embed.add_field(name="Aircraft", value=acft)
                        embed.add_field(name="Cruise Altitude", value=plncruise)
                        embed.add_field(name="Route", value=route, inline=False)
                        embed.add_field(name="Remarks", value=remarks, inline=False)
                        embed.set_footer(text="Source: VATSIM API")
                        await ctx.send(embed=embed)

                    else:
                        callsign = data[0]
                        cid = data[1]
                        name = data[2]
                        type = data[3]
                        freq = data[4]
                        server = data[14]
                        atis = data[35].replace("^\\xc2\\xa7", "\n")
                        if (atis == ''):
                            atis = "None"
                        positionint = data[18]
                        if ("_ATIS" in callsign):
                            position = "ATIS"
                        elif (positionint == "6"):
                            position = "Center/Enroute"
                        elif (positionint == "5"):
                            position = "Approach"
                        elif (positionint == "4"):
                            position = "Tower"
                        elif (positionint == "3"):
                            position = "Ground"
                        elif (positionint == "2"):
                            position = "Delivery"
                        elif (positionint == "1"):
                            position = "FSS"
                        elif (positionint == "0"):
                            position = "Observer"
                        else:
                            position = "Unknown"

                        embed = discord.Embed(title="Vatsim " + type + ": " + callsign, color=0x00ff00)
                        embed.add_field(name="Callsign", value=callsign)
                        embed.add_field(name="Controller", value=name)
                        embed.add_field(name="CID", value=cid)
                        embed.add_field(name="Frequency", value=freq)
                        embed.add_field(name="Position", value=position)
                        embed.add_field(name="Server", value=server)
                        embed.add_field(name="Controller Details", value=atis, inline=False)
                        embed.set_footer(text="Source: VATSIM API")
                        await ctx.send(embed=embed)
                except:
                    embed = discord.Embed(title="ERROR!", description="No Pilot/ATC with callsign '" + callsign + "'  is connect to the VATSIM network. The VATSIM data updates every two minutes. If you believe there is an error please try again later.", color=0x00ff00)
                    embed.set_footer(text="Source: VATSIM API")
                    await ctx.send(embed=embed)
            """
            elif len(callsign) == 4:
                embed = discord.Embed(title="Controllers online for: " + callsign, color=0x00ff00)
                try:
                    atis = callsign + "_ATIS" + str(data).split(callsign + "_ATIS", 1)[1].rsplit("\\n")[0]
                except:
                    pass
                aptdat = open("apt.dat", "r")
                try:
                    apt = callsign + aptdat.read().split(callsign, 1)[1].rsplit("\\n")[0]
                except:
                    embed.add_field(name=u"\u200B", value="Could not find airport " + callsign, inline=False)
                    embed.set_footer(text="Source: VATSIM API")
                    await ctx.send(embed=embed)
                    return
                fir = apt.split("|")[5]
                aptdat.close()

                firdat = open("fir.dat", "r")
                for line in firdat:
                    if fir in line:
                        firdetails = line
                        break
                
                fircode = firdetails.split("|")[2]

                controllers = []
                try:
                    while True:
                        controller = fircode + "_" + str(data).split(fircode + "_", 1)[1].rsplit("\\n")[0]
                        if controller.startswith(fircode + "_ATIS") == False:
                            controllers.append(controller)
                        data = str(data).split(controller)[1]
                except:
                    pass
                    
                if atis != None:
                    controllers.append(atis)
                index = 0
                for item in controllers:
                    if (index != 0):
                        embed.add_field(name=u"\u200B", value=u"\u200B", inline=False)
                    item = item.split(":")
                    callsign = item[0]
                    cid = item[1]
                    name = item[2]
                    freq = item[4]
                    positionint = item[18]
                    if ("_ATIS" in callsign):
                        position = "ATIS"
                    elif (positionint == "6"):
                        position = "Center/Enroute"
                    elif (positionint == "5"):
                        position = "Approach"
                    elif (positionint == "4"):
                        position = "Tower"
                    elif (positionint == "3"):
                        position = "Ground"
                    elif (positionint == "2"):
                        position = "Delivery"
                    elif (positionint == "1"):
                        position = "FSS"
                    elif (positionint == "0"):
                        position = "Observer"
                    else:
                        position = "Unknown"
                
                    embed.add_field(name="Callsign", value=callsign)
                    embed.add_field(name="Name", value=name)
                    embed.add_field(name="CID", value=cid)
                    embed.add_field(name="Position", value=position)
                    embed.add_field(name="Frequency", value=freq)
                    index += 1

                embed.set_footer(text="Source: VATSIM API")
                await ctx.send(embed=embed)
            """

        else:
            embed = discord.Embed(title="Command: !vatsim", description=f"**Description:** Grabs data for a vatsim callsign \n**Usage:** !vatsim [callsign] \n**Example:** \n!vatsim BOS_APP \n!vatsim N9669Q", color=0x00ff00)
            await ctx.send(embed=embed)
    
    @commands.command(aliases=['acars'])
    async def atlas(self, ctx):
        url = "https://crew.atlasair-virtual.com/index.php/datafeeds/acars"

        http = urllib3.PoolManager()
        response = http.request('GET', url)
        rawdata = response.data

        if ("</Flight>" not in str(rawdata)):
            embed = discord.Embed(title="Atlas Air Virtual ACARS", description="There are no aircraft currently Airborne", color=0x00ff00)
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(title="Atlas Air Virtual ACARS", color=0x00ff00)
        index = 0
        while ("</Flight>" in str(rawdata)):
            if index == 1:
                embed.add_field(name=u"\u200B", value=u"\u200B", inline=False)
            if index == 2:
                index = 0
                await ctx.send(embed=embed)
                embed = discord.Embed(color=0x00ff00)
            
            data = str(rawdata)

            data = data.partition("<Flight pilotid=")[2].partition("\">")[2]
                  
            rawdata = data.split("</Flight>", 1)[1]
            data = data.split("</Flight>", 1)[0]
            data = data.replace("><", ">\n<")
                    
            name = data.partition("<name>")[2].split("</name>", 1)[0]
            pilotid = data.partition("<pilotid>")[2].split("</pilotid>", 1)[0]
            flightnum = data.partition("<flightnum>")[2].split("</flightnum>", 1)[0]
            depicao = data.partition("<depicao>")[2].split("</depicao>", 1)[0]
            depname = data.partition("<depname>")[2].split("</depname>", 1)[0]
            arricao = data.partition("<arricao>")[2].split("</arricao>", 1)[0]
            arrname = data.partition("<arrname>")[2].split("</arrname>", 1)[0]
            dist = data.partition("<dist>")[2].split("</dist>", 1)[0]
            alt = data.partition("<alt>")[2].split("</alt>", 1)[0]
            gs = data.partition("<gs>")[2].split("</gs>", 1)[0]
            acft = data.partition("<acft>")[2].split("</acft>", 1)[0]
            ete = data.partition("<time>")[2].split("</time>", 1)[0]

            embed.add_field(name="Pilot", value=pilotid + " " + name)
            embed.add_field(name="Aircraft", value=acft)
            embed.add_field(name="ETE", value=ete)
            embed.add_field(name="Flight", value=flightnum)
            embed.add_field(name="DEP", value=depname + " (" + depicao + ")")
            embed.add_field(name="ARR", value=arrname + " (" + arricao + ")")
            embed.add_field(name="Distance", value=dist)
            embed.add_field(name="Ground Speed", value=gs)
            embed.add_field(name="Altitude", value=alt)

            index += 1

        await ctx.send(embed=embed)
            
    @commands.command()
    async def datis(self, ctx, icao=None):
        if (icao != None):
            url = "https://datis.clowd.io/" + icao

            http = urllib3.PoolManager()
            response = http.request('GET', url)
            data1 = response.data

            try:
                data1 = str(data1).split("<p class=\"text-monospace mt-3\" style=\"font-size:14px;white-space: pre-wrap;\">")[1].rsplit("</p>")[0].replace("\\n", "")
                if ("DEP" in data1[:10]):
                    type="DEP DATIS"
                else:
                    type="DATIS"
                embed = discord.Embed(title="DATIS for: " + icao, color=0x00ff00)
                embed.add_field(name=type, value=data1)
                embed.set_footer(text="Source: https://datis.clowd.io/")
                data = response.data
            except:
                embed = discord.Embed(title="Could not find a DATIS for: " + icao, color=0x00ff00)
                embed.set_footer(text="Source: https://datis.clowd.io/")
                await ctx.send(embed=embed)
                return

            try:
                data = str(data).split("<p class=\"text-monospace mt-3\" style=\"font-size:14px;white-space: pre-wrap;\">")[2].rsplit("</p>")[0].replace("\\n", "")
                type="ARR DATIS"
                embed.add_field(name=type, value=data)
                
            except:
                pass

            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Command: !datis", description=f"**Description:** Grabs the datis for an airport\n**Usage:** !datis [icao] \n**Example:** \n!datis KBOS \n!datis KORD", color=0x00ff00)
            await ctx.send(embed=embed)
    
    @commands.command()
    async def taf(self, ctx, icao=None):
        if icao == None:
            embed = discord.Embed(title="Command: !taf", description=f"**Description:** Fetches the taf for a specific airport \n**Usage:** !taf [icao] \n**Example:** \n!metar taf", color=0x00ff00)
            await ctx.send(embed=embed)
        else: 
            url = "https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=tafs&requestType=retrieve&format=xml&stationString=" + icao + "&hoursBeforeNow=24&timeType=issue&mostRecent=true"

            http = urllib3.PoolManager()
            response = http.request('GET', url)
            data = response.data
            rawdata = data

            data = str(data)
            taf = data.partition("<raw_text>")[2].split("</", 1)[0]
            issued = data.partition("<issue_time>")[2].split("</issue_time>", 1)[0]
            validstart = data.partition("<valid_time_from>")[2].split("</valid_time_from>", 1)[0]
            validend = data.partition("<valid_time_to>")[2].split("</valid_time_to>", 1)[0]
			
            embed = discord.Embed(title="TAF for " + icao, description=None, color=0x091d60)
            embed.add_field(name="Raw Report", value=taf, inline=False)

            while ("</forecast>" in str(rawdata)):
			
                data = str(rawdata)
                
                try:
                    rawdata = data.split("</forecast>", 1)[1]
                except:
                    await ctx.send("Loop broken")
                    break

                data = data.partition("<forecast>")[2].split("</forecast>", 1)[0]

                data = data.split("</forecast>", 1)[0]
                data = data.replace("><", ">\n<")
                
                fcststart = data.partition("<fcst_time_from>")[2].split("</fcst_time_from>", 1)[0]
                fcstend = data.partition("<fcst_time_to>")[2].split("</fcst_time_to>", 1)[0]
                winddeg = data.partition("<wind_dir_degrees>")[2].split("</wind_dir_degrees>", 1)[0]
                windspd = data.partition("<wind_speed_kt>")[2].split("</wind_speed_kt>", 1)[0]
                windgust = data.partition("<wind_gust_kt>")[2].split("</wind_gust_kt>", 1)[0]
                vis = data.partition("<visibility_statute_mi>")[2].split("</visibility_statute_mi>", 1)[0]
                precip = data.partition("<wx_string>")[2].split("</wx")[0].split(" ")
				
                if winddeg != "000":
                    wind = winddeg + " Degrees, " + windspd + " Knots"
                if windgust.isdigit():
                    wind = wind + ", Gusting to " + windgust + " Knots"
                elif winddeg == "VRB":
                    wind = "Variable at " + windspd + " Knots"
                elif windspd == 0:
                    wind = "Calm"
                                
                skycover = []
                coveralt = []
                skycon = ""
                index = -1

                if vis == "6.21":
                    vis = "10+"

                sky = str(data.partition("<sky_condition ")[2].rsplit("/\"")[0])

                for x in range(sky.count("sky_cover")):
                    skycover.append(sky.partition("sky_cover=\"")[2].split("\"")[0])
                    sky = sky.replace("cover", "", 1)

                for x in range(sky.count("cloud_base_ft_agl")):
                    coveralt.append(sky.partition("cloud_base_ft_agl=\"")[2].split("\"")[0])
                    sky = sky.replace("cloud_base_ft_agl", "", 1)

                for item in precip:
                    if "-" in item:
                        skycon = skycon + "Light "
                    elif "+" in item:
                        skycon = skycon + "Heavy "
                    
                    if "MI" in item:
                        skycon = skycon + "Shallow "
                    elif "BC" in item:
                        skycon = skycon + "Patches "
                    elif "BL" in item:
                        skycon = skycon + "Blowing "
                    elif "DR" in item:
                        skycon = skycon + "Low drifting "
                    elif "TS" in item:
                        skycon = skycon + "Thunderstorm "
                    elif "FZ" in item:
                        skycon = skycon + "Freezing "
                                        
                    if "SH" in item:
                        skycon = skycon + "Showers, "
                    elif "PR" in item:
                        skycon = skycon + "Partial, "
                    elif "RA" in item:
                        skycon = skycon + "Rain, "
                    elif "SN" in item:
                        skycon = skycon + "Snow, "
                    elif "IC" in item:
                        skycon = skycon + "Ice Crystals, "
                    elif "GR" in item:
                        skycon = skycon + "Hail, "     
                    elif "UP" in item:
                        skycon = skycon + "Unknown Precipitation, "
                    elif "DZ" in item:
                        skycon = skycon + "Drizzle, "
                    elif "SG" in item:
                        skycon = skycon + "Snow Grains, "
                    elif "PL" in item:
                        skycon = skycon + "Ice Pellets, "
                    elif "GS" in item:
                        skycon = skycon + "Snow Pellets, "
                                        
                    if "FG" in item:
                        skycon = skycon + "Fog, "
                    elif "VA" in item:
                        skycon = skycon + "Volcanic Ash, "
                    elif "BR" in item:
                        skycon = skycon + "Mist, "
                    elif "HZ" in item:
                        skycon = skycon + "Haze, "
                    elif "DU" in item:
                        skycon = skycon + "Widespread Dust, "
                    elif "FU" in item:
                        skycon = skycon + "Smoke, "

                    if "CLR" in skycover[0]:
                        skycon = "Clear"
                    elif "CAVOK" in skycover[0]:
                        skycon = "Clouds and Visibility OK"
                    elif "SKC" in skycover[0]:
                        skycon = "Sky Clear"
                    else:
                        for i in skycover:
                            index = index + 1
                            skycover = str(skycover).replace("\'", "").replace("[", "").replace("]", "")
                            if index != 0:
                                sky = sky + ", "
                            if str(i) == "FEW":
                                cover = "Few Clouds"
                            elif str(i) == "SCT":
                                cover = "Scattered Clouds"
                            elif str(i) == "BKN":
                                cover = "Broken Ceiling"
                            elif str(i) == "OVC":
                                cover = "Overcast Ceiling"
                            else:
                                cover = "Error"

                            skycon = skycon + cover + " at " + coveralt[index] + " Feet AGL, "

                            skycon = skycon[:-2]
            
                embed.add_field(name=fcststart + " - " + fcstend, value="**Station:** " + icao + "\n**Forecast Start:** " + fcststart + "\n**Forecast End:** " + fcstend + "\n**Wind:** " + wind + "\n**Visibility:** " + vis + " Statute Miles \n**Sky Conditions:** " + skycon, inline=False)
            try:
                embed.set_footer(text="This is not a source for an official weather briefing. Please obtain a weather briefing from the appropriate agency.")
                await ctx.send(embed=embed)
            except:
                await ctx.send("Cannot find taf for icao: " + icao)

    @commands.command()
    async def brief(self, ctx, icao1=None, icao2=None, icao3=None, icaoextra=None):
        if icao1 == None:
            embed = discord.Embed(title="Command: !brief", description=f"**Description:** Displays a briefing for one to three airport icao codes\n**Usage:** !brief [icao] [icao(optional)] [icao(optional)]\n**Example:** \n!brief KORD\n!rawmetar KORD KBOS KJFK", color=0x00ff00)
            await ctx.send(embed=embed)
        elif (icaoextra != None):
            embed = discord.Embed(title="ERROR!", description="This command has a maximum of 3 airports to reduce spam", color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            icao = ""
            icao = icao + icao1
            if icao2 != None:
                icao = icao + " " + icao2
            if icao3 != None:
                icao = icao + " " + icao3

            embed = discord.Embed(title="Briefing for " + icao, color=0x00ff00)
            icao = icao.split(" ")

            for apt in icao:
                metar = str(urllib3.PoolManager().request('GET', "https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=" + apt + "&hoursBeforeNow=2&mostRecent=true").data).partition("<raw_text>")[2].split("</", 1)[0]

                if (metar == ""):
                    metar = "METAR not found for " + apt

                taf = str(urllib3.PoolManager().request('GET', "https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=tafs&requestType=retrieve&format=xml&stationString=" + apt + "&hoursBeforeNow=24&timeType=issue&mostRecent=true").data).partition("<raw_text>")[2].split("</", 1)[0]

                if (taf == ""):
                    taf = "TAF not found for " + apt

                embed.add_field(name="**" + apt + " METAR**", value=metar, inline=False)
                embed.add_field(name="**" + apt + " TAF**", value=taf, inline=False)
                embed.add_field(name="**" + apt + " Charts**", value="https://chartfox.org/" + apt, inline=False)
            
            embed.set_footer(text="This is not a source for an official weather briefing. Please obtain a weather briefing from the appropriate agency.")
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(avBot(client))
    print("Loaded avBot")
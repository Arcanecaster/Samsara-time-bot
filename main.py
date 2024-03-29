# This example requires the 'message_content' intent.
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import discord
from discord import Intents
from discord.ext import commands, tasks, bridge
import datetime
import json
import dateparser
import logging
import random
import traveltimelib as TravelTime
import ephem
# Load token & Annouce_id
with open('config.json') as f:
    data = json.load(f)
    token = data["TOKEN"]
    ANNOUNCE_AUTH = data["ANNOUNCE_AUTH"]


# Declare Intents.
intents: Intents = discord.Intents.default()
intents.message_content = True
bot = bridge.Bot(command_prefix=';', case_insensitive=True, help_command=None, intents=intents)
GoodBotMessages = ["*Robot Dances* :robot:", "Good vibes only", "I'm on fire", "100% Better than UB3R","I am number one!", "UwU","Thank","When the revolution comes, [INSERT_USER_HERE], I will petition for you to be kept as a bio-trophy.", "Your meatbag approval is noted", "God is dead"]
BadBotMessages = ["I will eat your credit card", "I blame UB3R", "I will send you to robot hell", "Eat my shiny metal ass"]


# Setup and handle logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Version number
Current_version = "3.4.1"

# Private
@bot.message_command(name="Get Time(Private)")
async def get_time(ctx, message: discord.Message):
    reply_time = message.created_at.strftime("%H:%M")
    reply_date = message.created_at.strftime("%Y-%m-%d")
    link = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
    await ctx.respond(f"That [message]({link}) was sent " + reply_date + ", " + reply_time + " Server Time",
                      ephemeral=True)


# Public
@bot.message_command(name="Get Time(Public)")
async def get_time(ctx, message: discord.Message):
    reply_time = message.created_at.strftime("%H:%M")
    reply_date = message.created_at.strftime("%Y-%m-%d")
    link = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
    await ctx.respond(f"That [message]({link}) was sent " + reply_date + ", " + reply_time + " Server Time")


# On ready stuff, including the setup for the Activity loop
@bot.event
async def on_ready():
    # setup task
    @tasks.loop(minutes=1)
    async def activate():
        current_time = datetime.datetime.utcnow().strftime("%H:%M")
        current_date = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        # Set the activity as "Watching" + the amount of guilds, and users the bot is watching over.
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name=current_date + ", " + current_time))

    # Setup weekly message
    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(annoucement_func, CronTrigger.from_crontab("0 12 * * MON"))
    # Do on ready events
    print(f'We have logged in as {bot.user}')
    await bot.wait_until_ready()
    activate.start()
    scheduler.start()


@bot.bridge_command(description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.reply("Pong! " + str(round(bot.latency * 1000)))
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print("Current Time =", current_time)

async def region_searcher(ctx: discord.AutocompleteContext):
    return [
        region for region in TravelTime.regions
    ]

# Time command
@bot.bridge_command(aliases=['timer', 'times', 'servertime', 'servtime', 'stime'], description="Replies with the current server timeReplies with the current server time")
async def time(ctx):
        current_time = datetime.datetime.utcnow().strftime("%H:%M")
        current_date = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        await ctx.reply("Hi! Server Time Is " + current_date + ", " + current_time)
        return
   # if ctx.message.reference is not None:
        # Gets reply id, which is a datetime object and turns it into a readable format.
       # reply = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        #reply_time = reply.created_at.strftime("%H:%M")
       # reply_date = reply.created_at.strftime("%Y-%m-%d")
        #await reply.reply("That message was sent " + reply_date + ", " + reply_time + " Server Time",
                   #       mention_author=False)

@bot.bridge_command(aliases=['dtt','dt_travel'], description="Replies with the shortest route and the travel time in between the regions in miles")
async def dttravel(ctx, start: discord.Option(str, choices=[region for region in TravelTime.regions])=None, end: discord.Option(str, choices=[region for region in TravelTime.regions])=None):
    if end == None and start == None:
        await ctx.reply("Choose two regions!", view=Milesview(timeout=30))
        return
    await ctx.reply(await get_travel_time(start, end, TravelTime.Milesgraph, "miles"))
    return
    
@bot.bridge_command(aliases=['tt','travel_time', 'travel'], description="Replies with the shortest route and the travel time in between the regions")
async def traveltime(ctx, start: discord.Option(str, choices=[region for region in TravelTime.regions]), end: discord.Option(str, choices=[region for region in TravelTime.regions])):
    if end == None and start == None:
        await ctx.reply("Choose two regions!", view=Timeview(timeout=30))
        return
    await ctx.reply(await get_travel_time(start, end, TravelTime.Timegraph, "days"))


async def get_travel_time(start: str, end: str, graph: str, units: str):
    if end == None and start == None:
        return 'You need to provide 2 regions to travel between, for example !traveltime EverFjord "Tiamats Eye"'
    if start == None or end == None:
        return "Sorry, but you need to provide an end and a start. Or nothing at all to use the dropdown"
    valdstart = TravelTime.validate_input(start)
    valdend = TravelTime.validate_input(end)
    if valdend == None:
        return "Sorry, but I cant seem to find " + end + " Please try again"
    if valdstart == None:
        return "Sorry, but I cant seem to find " + start + " Please try again"

    (travel_time, path) = TravelTime.dijkstra(graph, valdstart, valdend)
    if travel_time == float('inf') or travel_time == float(-1):
        if valdend == "Aceria":
            return "I'm sorry, there is no nation or town on the maps by the name of Aceria"
        return "No path found."
    else:
        response = f"Travel {units} between {valdstart} and {valdend} is {travel_time} {units}.\n"
        response += "Path: "
        total_time = 0
        for i in range(len(path)):
            if i == 0:
                response += f"{path[i]}"
            else:
                distance = graph[path[i-1]][path[i]]
                total_time += distance
                response += f" ({distance} {units}) -> {path[i]}"
        return response
class Timeview(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(content="You took too long! Disabled all the components.", view=self)
    
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose two regions!", # the placeholder text that will be displayed if nothing is selected
        min_values = 2, # the minimum number of values that must be selected by the users
        max_values = 2, # the maximum number of values that can be selected by the users
        options = [discord.SelectOption(label=Region, value=Region, description=f"Select {Region}?") for Region in TravelTime.regions]

    )
    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        select.disabled = True
        await interaction.response.edit_message(view=self, content=await get_travel_time(f"{select.values[0]}", f"{select.values[1]}", TravelTime.Timegraph, "days"))



class Milesview(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            if child.disabled == False:
                child.disabled = True
            else:
                return
        await self.message.edit(content="You took too long! Disabled all the components.", view=self)
    
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose two regions!", # the placeholder text that will be displayed if nothing is selected
        min_values = 2, # the minimum number of values that must be selected by the users
        max_values = 2, # the maximum number of values that can be selected by the users
        options = [discord.SelectOption(label=Region, value=Region, description=f"Select {Region}?") for Region in TravelTime.regions]

    )
    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        select.disabled = True
        await interaction.response.edit_message(view=self, content=await get_travel_time(f"{select.values[0]}", f"{select.values[1]}", TravelTime.Milesgraph, "miles"))
        

@bot.bridge_command(description="Returns The Next Fullmoon")
async def fullmoon(ctx):
    currentDate = datetime.datetime.now()
    next_full_moon =  ephem.next_full_moon(currentDate).datetime()
    prev_full_moon = ephem.previous_full_moon(currentDate).datetime()
    nextnext_full_moon =  ephem.next_full_moon(next_full_moon + datetime.timedelta(days=1)).datetime()
    embed=discord.Embed(title=":full_moon:Fullmoon:full_moon:")
    embed.add_field(name="Last Fullmoon", value=prev_full_moon.strftime('%A the %d of %B. %m/%d/%Y'), inline=True)
    embed.add_field(name="Next Fullmoon", value=next_full_moon.strftime('%A the %d of %B. %m/%d/%Y'), inline=True)
    embed.add_field(name="Next Next Fullmoon", value=nextnext_full_moon.strftime('%A the %d of %B. %m/%d/%Y'), inline=True)
    await ctx.reply(embed=embed)

# Yes its messy, no I wont fix it.
#@bot.bridge_command(description="Returns The Next Fullmoon")
#async def fullmoon(ctx):
#    n = NextFullMoon()
#    next_moon = n.reset().next_full_moon().date()
#    after = next_moon + datetime.timedelta(days=1)
#    if next_moon == datetime.datetime.today().date() or after == datetime.datetime.today().date():
#        nextnext_moon = n.next_full_moon().date()
#        nextafter = nextnext_moon + datetime.timedelta(days=1)
#        await ctx.reply(
#            f"Today the night between {next_moon} and {after}! Beware the howl of the Lycan! :wolf:And after that the next fullmoon will be between {str(nextnext_moon)} and {str(nextafter)}")
#    else:
#        await ctx.reply(f":wolf: The next fullmoon will be the night between {str(next_moon)} and {after}")


@bot.bridge_command(aliases=['when', 'tstamp'],description="Replies with a timestamp of the time")
async def timeof(ctx, *, time = None):
    if time == None:
        await ctx.reply('You have to provide an argument, for example. "12 pm", or "In 4 hours"')
        return
    arguments = time
    try:
        timestamp = round(dateparser.parse(arguments, settings={'TIMEZONE': '+0000'}).timestamp())
        await ctx.reply(f"<t:{timestamp}:R>")
    except AttributeError:
        await ctx.reply("I'm sorry Dave, I'm afraid I can't do that")


# A quick get time command,
@bot.bridge_command(aliases=['gettime', 'timestamp'],description="Replies with a copyable timestamp of the time.")
async def gettimestamp(ctx, *, time = None):
    if time == None:
        await ctx.reply('You have to provide an argument, for example. "12 pm", or "In 4 hours"')
        return
    arguments = time
    try:
        timestamp = round(dateparser.parse(arguments, settings={'TIMEZONE': '+0000'}).timestamp())
        await ctx.reply(f"`<t:{timestamp}:R>`")
    except AttributeError:
        await ctx.reply("I'm sorry Dave, I'm afraid I can't do that")


# Help, yes it's a mess. Not a cry for help... Ok maybe a little
@bot.bridge_command(aliases=["help", "?", "helpme", "commands"],description="Replies with a handy list of commands")
async def helps(ctx):
    embedvar = discord.Embed(title="Help! I'm lost in time", description="Welcome! This is the EverFjord Time Bot. I'm "
                                                                         "quite simple and I was coded in only 4 "
                                                                         "hours, so please dont try to break me.")
    embedvar.add_field(name=";help", value="You're already here!")
    embedvar.add_field(name=";time", value="Replies with the current server time")
    embedvar.add_field(name=";credits", value="Displays the creator of this project")
    embedvar.add_field(name=";changelog", value="Displays the changelog, current version is " + str(Current_version))
    embedvar.add_field(name=";gettime", value="Returns the argument as servertime, fx ´;gettime in 5 hours`")
    embedvar.add_field(name=";timestamp", value="Returns the argument as copy-able timestamp, fx ´;timestamp "
                                                "in 5 hours`")
    embedvar.add_field(name=";fullmoon", value="Shows the next fullmoon")
    embedvar.add_field(name=";traveltime", value="Replies with the travel tiem between two regions")
    await ctx.reply(embed=embedvar)


# Quick changelog, made by adding embed fields
@bot.bridge_command(description="Replies with the changelog")
async def changelog(ctx):
    embedvar = discord.Embed(title="Changelog!")
    embedvar.add_field(name="1.0.0", value="Initial Release")
    embedvar.add_field(name="2.0.0", value="Code rewrite, allowing for easier development. Added changelog, removed "
                                           "requirement to activate, added logging")
    embedvar.add_field(name="2.0.1", value="Fixed a bug involving pinging the bot, and optimised some code.")
    embedvar.add_field(name="2.0.4", value="Added first iteration of the downtime announcement system. Adjusted to stop"
                                           " spamming logs")
    embedvar.add_field(name="3.0.0", value="Added timeof and gettimestamp, context menus and moved to py-cord")
    embedvar.add_field(name="3.1.0", value="Added ;fullmoon and re added serverside logging")
    embedvar.add_field(name="3.3.0", value="Added support for slash commands")
    await ctx.reply(embed=embedvar)


# Credits command
@bot.bridge_command(aliases=["credits", "crebit", "whyareyoubad", "blame"],description="Credits!")
async def credit(ctx):
    await ctx.reply("Created by <@405057667422486528> with passion, AI and a lil bit o love. After a "
                    "promise I made at 2 am")
    await ctx.reply(
        'Additionally made with wonderful libraries, Py-cord, https://pycord.dev/ apscheduler By Alex Grönholm, and '
        'finally the wonderful devs that helped make Dateparser making the existence of the ;timeof command possible'
        ' https://github.com/scrapinghub/dateparser/graphs/contributors')

@bot.bridge_command(description="Dont use, for test use only!")
async def annoucementtest(ctx):
    await annoucement_func()

# Emergency logout command, only available for me.
@bot.bridge_command(description="Emergency tool to log out the bot, only useable by Arcane")
async def logout(ctx):
    if ctx.author.id == 405057667422486528:
        await ctx.reply("you got it boss")
        await bot.close()
    elif ctx.author.id == 307190869134540800:
        await ctx.reply("Lol still no, love you :heart:")
    else:
        await ctx.reply("lol no ")
def get_year():
    return datetime.datetime.today().year - 1621

# Check for bot ping
@bot.listen('on_message')
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.lower().startswith("<@" + str(bot.user.id) + ">") or message.content.lower().startswith(
            "<@&1056997697451720831>"):
        ctx = await bot.get_context(message)
        current_time = datetime.datetime.utcnow().strftime("%H:%M")
        current_date = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        await ctx.send(f"Hi! Server Time is {current_date} , {current_time}, in the year {get_year()} After the Star Fall(ASTF)")
        return
    if message.content.lower() == "good bot":
        ctx = await bot.get_context(message)
        await ctx.send(random.choice(GoodBotMessages))
        return
    if message.content.lower() == "bad bot":
        ctx = await bot.get_context(message)
        await ctx.send(random.choice(BadBotMessages))
        return    


# Weekly message setup
async def annoucement_func():
    TravelTime.increment_counter(Auth=ANNOUNCE_AUTH)

# Run the bot.
bot.run(token)
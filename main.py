import discord, asyncio, os, json, random, aiohttp, DiscordUtils
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from discord.utils import get
from keep_alive import keep_alive
import random
from discord.ext import commands
import aiohttp
from google_images_search import GoogleImagesSearch
from googleapiclient.discovery import build

intents = discord.Intents().all()

prefix = "-"
bot = commands.Bot(command_prefix=prefix, intents=intents, case_insensitive=True)
bot.ses = aiohttp.ClientSession()

engine = '23f228912a6f6ecbe'
api_key = os.environ['google']
key = os.environ['image_key']
gis = GoogleImagesSearch(id, engine)

@bot.event
async def on_ready():
    print("Ready")

async def tasks():
    await bot.wait_until_ready()

    statuses = ["Jamie Oliver Fail", "People who eat chili jam", "=help", "Uncle Gordon roast people"]

    while True:
        await bot.change_presence(activity=discord.Activity(
                    type=discord.ActivityType.watching,name=random.choice(statuses)))
        await asyncio.sleep(10)

@bot.event
async def on_message_delete(message):
    global sma, smc
    if str(message.channel.id) in sma:
        sma[str(message.channel.id)].append(message.author)
    else:
        sma[str(message.channel.id)] = [message.author]

    if str(message.channel.id) in smc:
        smc[str(message.channel.id)].append(message.content)
    else:
        smc[str(message.channel.id)] = [message.content]

    await asyncio.sleep(3600)  # resets after an hour
    smc[str(message.channel.id)].remove(message.content)
    sma[str(message.channel.id)].remove(message.author)

smc = {}
sma = {}

badwords = ['fuck', 'fuk', 'fuc', 'porn', 'purn', 'bitch', 'bitc', 'bich']


def has_profanities(content):
    splitters = " ._/?|][}{)(*&^%$#@!-+=`~<>"
    for i in badwords:  # Go through the list of bad words;
        if i.lower() in content.lower():
            return True
        for splitter in splitters:
            if i in "".join(content.lower().split(splitter)):
                return True
    return False

#@bot.event
#async def on_message(message):
    
###  if has_profanities(message.content):
    #    await message.delete()
   #     msg = await message.channel.send(
     #       f"{message.author.mention} Haiya keep it family friendly", delete_after=7)
       

#    await bot.process_commands(message)

@bot.command()
async def snipe(ctx):
    if str(ctx.channel.id) not in smc:
        await ctx.message.delete()
        await ctx.send('Nothing to snipe', delete_after=2)
        
    else:
        embed = discord.Embed(description="{}".format(smc[str(ctx.channel.id)][-1]))
        embed.set_footer(text="Sent by %s" % sma[str(ctx.channel.id)][-1], icon_url=sma[str(ctx.channel.id)][-1].avatar_url)
        embed.color = 0x1abc9c
        await ctx.message.delete()
        await ctx.send(embed=embed)

    
@bot.command()
async def listsnipe(ctx):
    if ctx.message.author.guild_permissions.manage_messages:
        if str(ctx.channel.id) not in smc:
            await ctx.channel.send("Theres nothing to snipe.")
            return
        embed = discord.Embed()
        embed.color = 0x1abc9c
        max_length = 5
        if len(smc[str(ctx.channel.id)]) <= max_length:
            snipe_list = smc[str(ctx.channel.id)]
        else:
            snipe_list = smc[str(ctx.channel.id)][:max_length]
        for i, x in enumerate(snipe_list):
            if len(ctx.message.embeds) > 0:
                embed.add_field(name="Sent by %s" %
                                sma[str(ctx.channel.id)][i],
                                value="Embed Object",
                                inline=False)
            else:
                embed.add_field(name="Sent by %s" %
                                sma[str(ctx.channel.id)][i],
                                value=x,
                                inline=False)

        embed.set_footer(
            text="In order of earliest to latest deleted messages.")
        await ctx.send(embed=embed)
        return

@bot.command(aliases=['userinfo'])
async def define(ctx, member: discord.Member):
    roles = member.roles
    whois = discord.Embed(title=member.name + "#" + member.discriminator, description=member.mention, colour=member.colour, timestamp=ctx.message.created_at)
    whois.add_field(name='ID:', value=member.id, inline=False)
    whois.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
    whois.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
    whois.add_field(name='Roles:', value="\n" .join([role.mention for role in roles[1:]]), inline=False)
    whois.add_field(name='Highest Role:',value=member.top_role.mention,inline=False)
    whois.add_field(name='Discriminator:', value=member.discriminator)
    whois.set_author(name=member.name, icon_url=member.avatar_url)
    whois.set_footer(text='Info for ' + member.display_name + '. Requested by ' + ctx.author.name + "#" + ctx.author.discriminator)

    await ctx.send(embed=whois)

#HELP================================================================================

bot.remove_command("help")
@bot.command()
async def help(ctx):
    contents = [

    "**Pages:** \n General",

    "**General:**\n Chef - Determine your chef by taling a short quiz \n 8Ball - Ask uncle Roger your deep thoughts! \n Image - Find cool images on the web \n 8Ball - Ask about your future! \n Coinflip - Quick coinflip \n Fight - Fight a another user!  \n Truth or Dare - Challenge yourself!"
    ]

    embeds = []
    for i, content in enumerate(contents):
        split_content = content.split(" \n ")
        title = split_content[0]
        embed = discord.Embed(title=title, inline=True, description="\n".join(split_content[1:]))
        embed.color= 0xc27c0e
        # for command in split_content[1:]:
        #     command_content = command.split("\n")
        #     print(command_content)
        #     embed.add_field(name=command_content[0], value=command_content[1])
        embed.set_footer(text="Page %s/%s. Made by amechanos" % (str(i+1), str(len(contents))) )
        embeds.append(embed)

    # discord.utils paginator (simple way to use reaction thing)
    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
    paginator.add_reaction('⬅️', "back")
    paginator.add_reaction('➡️', "next")
    await paginator.run(embeds)


#FUN=================================================================================================

questions = [
    ("What is the best kitchen utensil?", ["wok", "rice cooker"], ["saucepan", "colander"]),
    ("What type of jam is usable in cooking?", ["none", "no jam"], ["chili jam", "apple jam"]),
    ("What is the best seasoning?", ["msg", "fish sauce", "soy sauce", "soyasauce"], ["none", "no seasoning"])
]
@bot.command()
async def chef(ctx):
    score = 0
    
    for q in questions:

        question = await ctx.send(q[0])
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await bot.wait_for("message", check=check)
        if msg.content.lower() in q[1]:
            score += 10
        elif msg.content.lower() in q[2]:
            score += 1
        elif has_profanities(msg.content):
            score +=0
        else:
            score += 5

    r = {
        10: "**Jamie Oliver**!",
        15: "**Nigella Lawson!**",
        20: "**Nick DioGivanni!**",
        25: "**Gordon Ramsay!**",
        29: "**Chef Wang Gang!!**",
        30: "**Uncle Roger!** \n _You got perfect score Fuyioh!_"
    }
    result = discord.Embed(title="If you were a chef, you would be:")
    result.color=0x11806a
    for i, t in enumerate(r):
        if i-1 < 0: n = 0
        else: n = list(r)[i-1]
        if score > n and t <= score:
            result.description = r[t]  
    await ctx.send(embed=result)


@bot.command()
async def coinflip(ctx):
  flip = random.choice(range(0,2))
  if flip == 1:
    em = discord.Embed(title="Coin Flip Result", description="You Got Heads!")
    em.color= 0x1abc9c
    await ctx.send(embed=em)
  else:
    em = discord.Embed(title="Coin Flip Result", description="You Got Tails!")
    em.color= 0x1abc9c
    await ctx.send(embed=em)
    
@bot.command(name="8ball")
async def _8ball(ctx, *q): # q = question
    with open("8ball.txt", "r") as f:
        ball = f.readlines()
        f.close()

    if q == None:
        await ctx.send("You did not provide a question")
    else:
        reply = random.choice(ball)
        em = discord.Embed(title="8Ball Results")
        em.color= 0x1abc9c
        em.add_field(name=" ".join(q), value=reply)
        await ctx.send(embed=em)

@bot.command()
async def td(ctx):
    await ctx.send("Truth or dare?")
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
                    
    msg = await bot.wait_for("message", check=check)
    if msg.content.lower() in ["t", "truth"]:
        with open("truth.txt", "r") as f:
            t = f.readlines()
            f.close()
        reply = random.choice(t)
        await ctx.send(reply)
    elif msg.content.lower() in ["d", "dare"]:
        with open("dares.txt", "r") as f:
            d = f.readlines()
            f.close()
        reply = random.choice(d)
        await ctx.send(reply)
    else:
        await ctx.send("Invalid answer, please try again")

@bot.command()
async def image(ctx, *, search):
    ran = random.randint(0, 9)
    resource = build("customsearch", "v1", developerKey=api_key).cse()
    result = resource.list(
        q=f"{search}", cx="23f228912a6f6ecbe", searchType="image"
    ).execute()
    url = result["items"][ran]["link"]
    embed1 = discord.Embed(title=f"Here Your Image ({search.title()})")
    embed1.set_image(url=url)
    await ctx.send(embed=embed1)

@bot.command(aliases=["duel"])
async def fight(ctx, user: discord.Member):
    turn = 0 #adding a turn variable for turn taking
    cma = ctx.message.author
    health = 100
    ohealth = 100
    powers = "slap poke choke drown" # change moves here
    powers = powers.split()
    moves = "***Moves:*** "+ ", ".join(powers)
    
    if user == cma:
        await ctx.send(f"Haiya....You can't fight yourself {cma.mention}", delete_after=5)
    elif user == 875176497764261968:
        await ctx.send(f"Haiya...So weak so you fight Uncle Roger. Dissapointment", delete_after=5)
    else:
        # confirmation to duel
        mes = await ctx.send(f"{user.mention}, will you accept or decline the duel? **[a/d]**")
        def check(msg):
            return msg.author == user and msg.channel == ctx.channel
        msg = await bot.wait_for("message", check=check)
        if msg.content.lower() in ["a", "accept", "y", "yes"]:
            await mes.edit(content="Starting match..")
            await asyncio.sleep(1)
            while True:
                if health <= 0:
                    await ctx.send(f"{user.mention} won the battle!")
                    return
                elif ohealth <= 0:
                    await ctx.send(f"{cma.mention} won the battle!")
                    return
                else:
                    if turn == 0:          
                        mes = await ctx.send(f"What do you want to do {cma.mention}? \n {moves}")
                        def check(msg):
                            return msg.author == cma and msg.channel == ctx.channel
                        msg = await bot.wait_for("message", check=check)
                        print(msg.content)
                        if msg.content.lower() in powers:
                            ohealth -= random.randint(5, 20)  
                            await mes.edit(content=f"Successful hit! \n **{user.mention}'s health:** {ohealth}")
                            turn += 1
                        elif msg.content.lower() not in powers:
                            await ctx.send("What you thinking? Not valis move!", delete_after=3)
                            return True
                        else:
                            await asyncio.sleep(10)
                            await mes.edit(content=f"Haiya....{cma.mention} give up, such a pussy")
                            break
                        
                    elif turn == 1:
                        mes = await ctx.send(f"What do you want to do {user.mention}? \n {moves}")
                        def check(msg):
                            return msg.author == user and msg.channel == ctx.channel
                        msg = await bot.wait_for("message", check=check)
                        if msg.content.lower() in powers:
                            health -= random.randint(5, 20)
                            await mes.edit(content=f"You slapped {cma.mention} with a wok! \n **{cma.mention}'s health:** {health}")
                            turn -= 1
                        elif msg.content.lower() not in powers:
                            await ctx.send("What you thinking? Not valis move!", delete_after=3)
                            return True
                        else:
                            await asyncio.sleep(10)
                            await mes.edit(content=f"Haiya....{user.mention} give up, such a pussy")
                            break  
                    else:
                        return
                    await asyncio.sleep(2)
        elif msg.content.lower() in ["d", "deny", "decline", "no", "n"]:
            await mes.edit(content=f"Haiya {user} such a pussy")
            await asyncio.sleep(3)
            await mes.delete()
            return
        

        

keep_alive()    
bot.loop.create_task(tasks())
bot.run(os.getenv("TOKEN"))
import discord
import bs4 as bs
import urllib.request
import re
from discord.ext import commands

token = open("token.txt","r").read()
client = discord.Client() #starts the discord client

@client.event #event wrapper
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    print(f"{message.channel}: {message.author}: {message.content}")
    if message.content.lower() == "siege_stats.close()" :
        await message.channel.send('logging out!')
        await client.close()
    l = len(message.content)
    name = str(message.content[7:l])
    url = "https://r6.tracker.network/profile/pc/" + name
    if message.content.lower().startswith('!stats'):
        class AppURLopener(urllib.request.FancyURLopener):
            version = "Mozilla/5.0"

        opener = AppURLopener()
        response = opener.open(url)

        soup = bs.BeautifulSoup(response,'lxml')

        ranked_kd = soup.find('div',{'data-stat' : 'RankedKDRatio'})
        print(ranked_kd.string)

        ranked_kills = soup.find('div', {'data-stat' : 'RankedKillsPerMatch'})
        print(ranked_kills.string)

        unranked_kd = soup.find('div',{'data-stat' : 'UnRankedKDRatio'})
        print(unranked_kd.string)

        unranked_kills = soup.find('div', {'data-stat' : 'UnRankedKillsPerMatch'})
        print(unranked_kills.string)

        levels = soup .find_all('div',{'class':'trn-defstat__value'})

        i = 0
        for i in range(0,2,1):
            print(levels[i].string)

        await message.channel.send(f'name : \n{name} \n\nlevel : {levels[0].string} \n Ranked KD : {ranked_kd.string} \n Ranked kpm : {ranked_kills.string} \n Highest MMR : {levels[1].string}')

client.run(token)

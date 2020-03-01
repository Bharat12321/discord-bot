import os
import requests
import settings
from discord.ext.commands import Bot
from sqlalchemy import create_engine, text
from model import search_history, engine

bot = Bot(command_prefix=settings.COMMAND_PREFIX)
    
def run():
    bot.run(settings.BOT_TOKEN)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return

    if message.content.startswith('hi'):
        msg = 'Hey {0.author.mention}'.format(message)
        await bot.send_message(message.channel, msg)

    if message.content.startswith('!google'):
        # get search value from message
        search_string = message.content.replace("!google", "")

        __author_id = message.author.id
        __search_string = search_string.strip()

        # add user search history in db
        conn = engine.connect()
        ins = search_history.insert().values(
            user=str(__author_id),
            search_key=str(__search_string))

        result = conn.execute(ins)
        conn.close()

        # Call google API to find search urls
        API_ENDPOINT = settings.GOOGLE_ENDPOINT+""+str(__search_string)
        res = requests.get(url=API_ENDPOINT)
        res_data = res.json()
        
        links = list()
        if 'items' in res_data:
            for url in res_data['items']:
                url = url['link']
                links.append(url)

        msg = "Here is your top 5 links for your search :\n"
        send_urls = ' \n'.join(links[:5])
        msg += send_urls
        await bot.send_message(message.channel, msg)

    if message.content.startswith('!recent'):
        msg = 'Hey {0.author.mention}'.format(message)
        search_string = message.content.replace("!recent", "")
        __author_id = message.author.id
        __search_string = search_string.strip()
        print(__search_string, " __search_string")

        conn = engine.connect()
        t = text("SELECT * FROM search_history WHERE user = '"+__author_id+"' AND search_key LIKE '%"+__search_string+"%'")
        result = conn.execute(t)
        recent_searched_list = list()

        for row in result:
            print (row, " row ")
            recent_searched_list.append(row['search_key'])

        msg = None
        if recent_searched_list:
            msg = "Your recently searches are :\n"
            send_search_history = ' \n'.join(recent_searched_list)
            msg += send_search_history
        else:
            msg = "Their is no recent searches"
        await bot.send_message(message.channel, msg)
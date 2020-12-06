from creds import BOT_TOKEN, DB  # importing credentials of mongodb database and bot token

from discord.ext import commands
from googlesearch import search

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():  # checking the server connection
    print("Logged in as {0}".format(client.user))


@client.event
async def on_message(message):
    if message.content.startswith('$hi'):
        await message.channel.send('Hey!')  # replying hey yo the hi

    elif message.content.startswith('!google'):
        search_content = " ".join(
            str(message.content).split(' ')[1:])  # splitting string so that !google does not count as search text
        DB["save_search_text"].insert_one(
            {"user_text": search_content})  # saving search text in mongo collection named as save_search_text
        for j in search(search_content, tld="co.in", num=1, stop=5, pause=2):
            await message.channel.send(j)

    elif message.content.startswith('!recent'):
        search_text = " ".join(str(message.content).split(' ')[1:])
        recent_searches = list(DB["save_search_text"].find({"user_text": {"$regex": search_text}}, {"_id": 0}))  # fetching regex match for recent searches
        for recent_search in recent_searches:
            await message.channel.send(recent_search.get("user_text"))


client.run(BOT_TOKEN)  # running the client by passing bot token

import discord
from discord.ext import commands
import os
import requests
import json

cookies = {
    '_ga': 'GA1.2.735792174.1600309507',
    'locale': 'en-US',
}
at = os.environ.get('USER_TOKEN')

headers = {
    'Host': 'discord.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/json',
    'Authorization': at,
    'Origin': 'https://discord.com',
    'Connection': 'close',
}

def help_embed():
    source_code = 'You can get source code from here: https://github.com/0x0is1/Avtarical'

    embed = discord.Embed(title="Avtarical", color=0x03f8fc)
    embed.add_field(
        name="Description:", value="A simple discord bot particularly designed for pfp preview purpose.", inline=False)
    embed.add_field(
        name="**Commands:**\n", value="`.pfp` \n `.pfp [USER_ID]` \n `.pfp [USER_ID] [QUALITY]` \n **Example:** \n To get self pfp: `.pfp` \n To get pfp with id: `.pfp 1234567890` \n To get pfp with id and quality: `.pfp 1234567890 1024`", inline=False)
    embed.add_field(
        name="Invite: ", value="You can get invite link by typing `.invite`")
    embed.add_field(name="Source: ", value=source_code, inline=False)
    embed.add_field(name='Author: ', value='0x0is1', inline=False)
    return embed

def invite_embed():
    embed = discord.Embed(title='Avtarical bot invite',
                          url='https://discord.com/api/oauth2/authorize?client_id=757685102183448709&permissions=26688&scope=bot',
                          description='Invite avtarical bot on your server.')
    return embed

def get_pfp(user_id):
    url = 'https://discord.com/api/v8/users/' + str(user_id) + '/profile'
    response = requests.get(url, headers=headers, cookies=cookies)
    return response.content


bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('bot is Online.')


@bot.command(name="help", description="Returns all commands available")
async def help(ctx):
    embed = help_embed()
    await ctx.send(embed=embed)

@bot.command()
async def invite(ctx):
    embed=invite_embed()
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong! `{}ms`'.format(round(bot.latency * 1000)))


@bot.command()
async def pfp(ctx, user_id=1, quality=1024):
    if user_id == 1:
        user_id = ctx.message.author.id
    response = get_pfp(user_id).decode('utf-8')
    jdata = json.loads(response)
    try:
        username = jdata['user']['username'] + \
            '#' + jdata['user']['discriminator']
        av = jdata['user']['avatar']
        link = 'https://cdn.discordapp.com/avatars/' + \
            str(user_id) + '/' + av + '.webp?size=' + str(quality)
        await ctx.send(link)
        await ctx.send('Username: {}'.format(username))
    except Exception:
        await ctx.send("The user id might be wrong or they don't have pfp. you have to type `.pfp <USER_ID HERE>` to get an user's pfp.")


auth_token = os.environ.get('AVATARICAL_BOT_TOKEN')
bot.run(auth_token)

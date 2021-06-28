import discord
# from local_settings import TOKEN
from settings import TOKEN
from scrape import game_news, fx_news, fx_info, baby_news

client = discord.Client()


# 起動時の処理
@client.event
async def on_ready():
    print('ログインしました')


# メッセージ受信時
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # メッセージが「/umu」の場合
    if message.content == '/umu':
        await message.channel.send('うむ')

    # メッセージが「/weather」の場合
    if message.content == '/weather':
        embed = discord.Embed(title="天気予報", description="")
        await message.channel.send(embed=embed)

    # メッセージが「/gamenews」の場合
    if message.content == '/gamenews':
        res = game_news()
        embed = discord.Embed(title="ゲームニュース", description=res)
        await message.channel.send(embed=embed)

    # メッセージが「/fxnews」の場合
    if message.content == '/fxnews':
        res = fx_news()
        embed = discord.Embed(title="FXニュース", description=res)
        await message.channel.send(embed=embed)

    # メッセージが「/fxinfo」の場合
    if message.content == '/fxinfo':
        res = fx_info()
        embed = discord.Embed(title="FX情報", description=res)
        await message.channel.send(embed=embed)

    # メッセージが「/babynews」の場合
    if message.content == '/babynews':
        res = baby_news()
        embed = discord.Embed(title="赤ちゃんニュース", description=res)
        await message.channel.send(embed=embed)

    # テスト用
    if message.content == '/test':
        embed = discord.Embed(title="title", description="description[リンク](https://www.google.com/?hl=ja)")
        await message.channel.send(embed=embed)


    # botが話しかけられた場合
    if client.user in message.mentions:
        await message.channel.send(f'{message.author.mention}')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)

from datetime import datetime

import MeCab
import discord
from asari.api import Sonar
from discord.ext import tasks
# from local_settings import TOKEN
from config import TEST_CHANNEL_ID
from settings import TOKEN
from scrape import epic_news, game_news, fx_news, fx_info, baby_news

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
        embed = discord.Embed(title="育児ニュース", description=res)
        await message.channel.send(embed=embed)


    # メッセージが「/parse」から始まる場合
    if message.content.startswith('/parse'):
        split_message = message.content.split(' ')
        if len(split_message) == 2:
            mecab = MeCab.Tagger()
            print("mecab:" + mecab.parse(split_message[1]))
            await message.channel.send(mecab.parse(split_message[1]))
        else:
            await message.channel.send("書式エラー：「/parse 〇〇」")

    # メッセージが「/asari」から始まる場合
    if message.content.startswith('/asari'):
        split_message = message.content.split(' ')
        if len(split_message) == 2:
            sonar = Sonar()
            resdict = sonar.ping(text=split_message[1])
            confidence = [d.get('confidence') for d in resdict['classes'] if d.get('class_name') == resdict['top_class']][0]
            result = '感情：' + resdict['top_class'] + '\n' + 'スコア：' + str(confidence)
            await message.channel.send(result)
        else:
            await message.channel.send("書式エラー：「/asari 〇〇」")

    # メッセージが「/epic」から始まる場合
    if message.content.startswith('/epic'):
        res = epic_news()
        embed = discord.Embed(title="今週の無料ゲーム", description=res)
        await message.channel.send(embed=embed)

    # テスト用
    if message.content == '/test':
        embed = discord.Embed(title="title", description="description[リンク](https://www.google.com/?hl=ja)")
        await message.channel.send(embed=embed)


    # botが話しかけられた場合
    if client.user in message.mentions:
        await message.channel.send(f'{message.author.mention}')


# 定期実行
@tasks.loop(seconds=60)
async def periodically():
    now = datetime.now().strftime('%H:%M')
    print('曜日：' + str(datetime.today().weekday()) + ' 時間：' + now)
    # 毎週月曜日の23:00に実行
    if datetime.today().weekday() == 0:
        if now == '23:00':
            res = baby_news()
            embed = discord.Embed(title="育児ニュース", description=res)
            channel = client.get_channel(TEST_CHANNEL_ID)
            await channel.send(embed=embed)

    # 毎週金曜日の23:00に実行
    if datetime.today().weekday() == 4:
        if now == '23:00':
            res = epic_news()
            embed = discord.Embed(title="今週の無料ゲーム", description=res)
            channel = client.get_channel(TEST_CHANNEL_ID)
            await channel.send(embed=embed)

# 定期実行スクリプト
periodically.start()
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)

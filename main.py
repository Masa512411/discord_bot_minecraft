import os
import asyncio
import time
import boto3
import discord
from discord import app_commands
from keep_alive import keep_alive

keep_alive()
TOKEN = os.environ['DISCORD_TOKEN']
INSTANCE_ID = os.environ['INSTANCE-ID']
client = discord.Client(intents=discord.Intents.default())
aws_access_key_id = os.environ['ACCESS_KEY']
aws_secret_access_key = os.environ['SECRET_ACCESS_KEY']

ec2 = boto3.resource('ec2',
                     region_name='ap-southeast-2',
                     aws_access_key_id=aws_access_key_id,
                     aws_secret_access_key=aws_secret_access_key)
instance = ec2.Instance(INSTANCE_ID)
tree = app_commands.CommandTree(client)


# 起動時に動作する処理
@client.event
async def on_ready():
  # 起動したらターミナルにログイン通知が表示される
  print('ログインしました')
  await tree.sync()


@tree.command(name="test", description="テストコマンドです。")
async def test_command(interaction: discord.Interaction):
  await interaction.response.send_message("てすと！")


@tree.command(name="start", description="サーバーの起動")
async def start_server(interaction: discord.Interaction):
  await interaction.response.defer()
  if instance.state['Name'] == 'stopped':
    instance.start()
    print("わっしょ1")

    while instance.state['Name'] != 'running':
      await asyncio.sleep(5)
      instance.reload()

    ip = instance.public_ip_address
    print(ip)
    #await interaction.channel.send(f"{instance.state['Name']}")
    await interaction.followup.send(f"start : {ip}")

    # 非同期処理が完了するまで待機する
    await asyncio.sleep(5)  # 適切な待機時間を設定してください
    print("処理が完了しました！")
  else:
    await interaction.followup.send("時間をおいてください")


@tree.command(name="stop", description="サーバーの停止")
async def stop_server(interaction: discord.Interaction):
  instance.stop()

  print("STOP")
  await interaction.response.send_message("stop server")


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
  # メッセージ送信者がBotだった場合は無視する
  if message.author.bot:
    return


# Botの起動とDiscordサーバーへの接続
try:
  client.run(TOKEN)
except:
  os.system("kill 1")


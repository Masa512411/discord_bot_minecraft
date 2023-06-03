import os
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

ec2 = boto3.client('ec2',
                   region_name='ap-southeast-2',
                   aws_access_key_id=aws_access_key_id,
                   aws_secret_access_key=aws_secret_access_key)
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
  response = ec2.start_instances(InstanceIds=[INSTANCE_ID])
  data = ec2.describe_instances(
    InstanceIds=[INSTANCE_ID]
)
  
  ip = data['Reservations'][0]['Instances'][0]['PublicIpAddress']
  print(response)
  await interaction.response.send_message(f"start : {ip}")

@tree.command(name="stop", description="サーバーの停止")
async def start_server(interaction: discord.Interaction):
  response = ec2.stop_instances(InstanceIds=[INSTANCE_ID])

  await interaction.response.send_message(f"stop server")

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
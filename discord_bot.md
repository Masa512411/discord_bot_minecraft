# Discordのbot作成
AWS EC2の起動と停止をDiscordから行えるようにするためのbot作成

## 使用するサービス
- [Repl.it](https://replit.com/~)
- discord.py
- python

## Repl.itの常時起動
Repl.itはタブをとじるとbotが停止してしまうが、
リクエストを受け取り続けさえすれば Bot が常時稼働できる

` keep_alive.py `
```
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

```
上記のファイルを作成したらmain.pyに以下を追記
``` 
from keep_alive import keep_alive # 追記

keep_alive() # 追記
client.run(TOKEN)
```

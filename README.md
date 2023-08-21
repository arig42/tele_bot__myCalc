# Tele bot for calculation


## Test

```

export TELEGRAM_BOT_TOKEN=123456789:QWERTY

uvicorn main:app

curl --request POST \
     --url https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "url": "{HOST/tl",
}
'
```


## Deploy on https://adaptable.io

`uvicorn main:app --host 0.0.0.0 --port 80`


## Note

- tele msg:

```
{
  "update_id": 725624489,
  "message": {
    "message_id": 3,
    "from": {
      "id": 439122005,
      "is_bot": false,
      "first_name": "y",
      "last_name": "z",
      "username": "x",
      "language_code": "en"
    },
    "chat": {
      "id": 439122005,
      "first_name": "y",
      "last_name": "z",
      "username": "x",
      "type": "private"
    },
    "date": 1692631152,
    "text": "hi"
  }
}
```

- Update permission to read messages from group: Chat with BotFather `/setprivacy`
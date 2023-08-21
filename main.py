import os
import logging
import requests
import json
from fastapi import FastAPI, Request

logging.basicConfig(level=logging.INFO)

app = FastAPI()


def send_tl_msg(data):
    url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    payload = {
        'chat_id': data['chat_id'], 
        'reply_to_message_id': data['message_id'], 
        'text': data['text'],
        }
    requests.post(url, json=payload, headers=headers)


def process_tl_msg(data):
    return {
        'chat_id': data.get('message', {}).get('chat', {}).get('id'),
        'message_id': data.get('message', {}).get('message_id'),
        'text': data.get('message', {}).get('text')
    }


def echo_tl_msg(data):
    logging.info(f'tl_msg: {json.dumps(data)}')
    msg = process_tl_msg(data)
    send_tl_msg(data)
    return 0


def handle_tl_msg(data):
    logging.info(f'tl_msg: {json.dumps(data)}')
    data = process_tl_msg(data)
    msg = data['text'] or ''
    logging.info(msg.startswith('/c'))
    if msg == '/start':
        data['text'] = 'Hello'
        send_tl_msg(data)

    elif msg.startswith('/c'):
        _msg = msg[2:]
        data['text'] = eval(_msg)
        send_tl_msg(data)

    else:
        send_tl_msg(data)
    return 0


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/tl")
async def tele(request: Request):
    try:
        handle_tl_msg(await request.json())
    except Exception as e:
        raise e
        return {"message": repr(e)}
    return {"message": "OK"}

import os
import logging
import requests
import json
from fastapi import FastAPI, Request

logging.basicConfig(level=logging.INFO)

app = FastAPI()
i = 0

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


def cmd_calculate(cmd):
    return eval(cmd)


def cmd_modulus10(data):
    return sum([int(_) for _ in list(data.strip())]) % 10


def cmd_divide(cmd):
    """
    Handle: `/d 100:H 50:N 50 | 4`
    """
    global i

    def increase_by_one():
        global i
        i+=1
        return i

    cmd= cmd[2:]
    _input = cmd.split('|')
    details = _input[0].strip()
    num =  int(_input[1]) if len(_input) > 1 else 2  # DEFAULT = 2
    separator = ',' if details.find(',') != -1 else ' '

    i = 0
    res = {}
    for detail in details.split(separator):
        _detail = detail.split(':')
        val = float(_detail[0])
        p = _detail[1].strip() if len(_detail) > 1 else str(increase_by_one())
        print(i)
        try:
            res[p] += val
        except KeyError:
            res[p] = val
    
    total = sum([v for v in res.values()])
    if len(res.keys()) < num:
        for _ in range(len(res.keys()), num):
            res[str(increase_by_one())] = 0 
    
    per_person = round(total / len(res.keys()), 1)

    return json.dumps({k: (per_person - v) for k, v in res.items()})


def handle_tl_msg(data):
    logging.info(f'tl_msg: {json.dumps(data)}')
    data = process_tl_msg(data)
    msg = data['text'] or ''
    
    if msg.startswith('/c'):
        data['text'] = cmd_calculate(msg[2:])
        send_tl_msg(data)

    elif msg.startswith('/d'):
        data['text'] = cmd_divide(msg)
        send_tl_msg(data)

    elif msg.startswith('/m'):
        data['text'] = cmd_modulus10(msg[2:])
        send_tl_msg(data)

    else:
        pass
        # send_tl_msg(data)
    return 0


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/tl")
async def tele(request: Request):
    try:
        handle_tl_msg(await request.json())
    except Exception as e:
        # raise e
        return {"message": repr(e)}
    return {"message": "OK"}

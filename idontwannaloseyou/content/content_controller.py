from megawrapper import MegaWrapper
from logger_utils import LoggerFactory
from content_service import ContentService
from flask import Flask
from flask import request, jsonify, Response
import json
import os
import threading


app = Flask(__name__)
LOGGER = LoggerFactory.get_logger(__name__)

@app.route("/content", methods=["POST"])
async def download():
    if body := json.loads(request.get_data()) or not isinstance(body, list):
                   
        thread = threading.Thread(target=wrapper_async, args=[body])
        thread.start()

        return "", 202
    return jsonify({'erro': 'Payload submetido é inválido'}), 400

def wrapper_async(body):
    import asyncio
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    loop.run_until_complete(callback(body))
    loop.close()
    
async def callback(body):
    client = ContentService()
    return await client.download_content(body)


if __name__ == "__main__":
    import os
    app.run(port=os.getenv("HTTP_PORT"), threaded=True)
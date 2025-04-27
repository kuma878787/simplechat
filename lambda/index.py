import json
import os
import urllib.request  # ★これを使う！
import re

# ngrok経由でアクセスするFastAPIサーバーのURL
FASTAPI_URL = os.environ.get("FASTAPI_URL", "https://d28f-34-125-235-220.ngrok-free.app")  # ←ここは自分のngrok URLに書き換える！

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))
        
        # リクエストボディの解析
        body = json.loads(event['body'])
        message = body['message']
        
        print("Processing message:", message)
        
        # FastAPIへ送るリクエストを作成
        payload = {
            "prompt": message,
            "max_new_tokens": 512,
            "do_sample": True,
            "temperature": 0.7,
            "top_p": 0.9
        }
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}

        print(f"Sending request to FastAPI server at {FASTAPI_URL} with payload: {payload}")
        
        # FastAPIサーバーにリクエストを送る
        req = urllib.request.Request(FASTAPI_URL, data=data, headers=headers)
        with urllib.request.urlopen(req) as response:
            response_body = json.loads(response.read().decode("utf-8"))
        
        print("FastAPI server response:", response_body)
        
        # 応答を取得
        assistant_response = response_body['generated_text']
        
        # 成功レスポンス
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": True,
                "response": assistant_response,
            })
        }
        
    except Exception as error:
        print("Error:", str(error))
        
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "error": str(error)
            })
        }

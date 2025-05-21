import json
import boto3
import os
from datetime import datetime, timezone

dynamodb = boto3.client('dynamodb')
table = dynamodb.Table(os.environ['PORTFOLIO_TABLE'])

def lambda_handler(event, context):
    try :
        body = json.loads(event.get("body", "{}"))
        user_id = body.get("user_id")
        symbol = body.get("symbol")

        if not user_id or symbol:
            return {
                "body": json.dumps({"error": "Missing user_id or symbol"})
            }
        
        item = {
            "user_id": user_id,
            "symbol": symbol,
            "added_on": datetime.now(timezone.utc).isoformat()
        }

        table.put_item(Item = item)

        return {
            "body": json.dumps({"message": f"{symbol} added for user {user_id}"})
        }

    except Exception as e :
        return {
            "body": json.dumps({"error": str(e)})
        }
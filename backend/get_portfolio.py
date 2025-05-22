import json
import boto3
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.client('dynamodb')
table = dynamodb.Table(os.environ['PORTFOLIO_TABLE'])

def lambda_handler(event, context):
    user_id = event.get("queryStringParameters", {}).get("user_id")

    if not user_id:
        return {
            "body", json.dumps("Error", "Missing user id")
        }

    try:
        response = table.query(
            KeyConditionExpression = Key('user_id').eq(user_id)
        )

        items = response.get("Items", [])

        return {
            "body": json.dumps({
                "user_id": user_id,
                "portfolio": items
            })
        }

    except Exception as e:
        return {
            "body": json.dumps({"Error": str(e)})
            }
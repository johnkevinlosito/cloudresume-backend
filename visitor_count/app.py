import json
import boto3
import os

def lambda_handler(event, context):
    db = boto3.resource('dynamodb')
    table = db.Table(os.environ['DynamoDBTable'])
    siteUrl =  event['queryStringParameters']['siteUrl'] 
    # siteUrl = 'cloudresume.johnkevinlosito.com'
    response = table.update_item(
        Key = {
            'siteUrl' : siteUrl
        },
        UpdateExpression="SET visitCount = if_not_exists(visitCount, :start) + :inc",

        ExpressionAttributeValues={
            ':inc': 1,
            ':start': 1,
        },
        ReturnValues="UPDATED_NEW"
    )
    res_obj = {
        'visitCount': str(response['Attributes']['visitCount'])
    }
    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin':'*'},
        'body' : json.dumps(res_obj)
    }
    

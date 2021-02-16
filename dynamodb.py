import boto3
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key


def get_resource():
    return boto3.resource('dynamodb',
                              aws_access_key_id='ACCESS_KEY',
                              aws_secret_access_key='SECRET_ACCESS_KEY',
                              region_name='eu-north-1')


def create_user_table(dynamodb=None):
    if not dynamodb:
        dynamodb = get_resource()

    table = dynamodb.create_table(
        TableName = 'Users',
        KeySchema = [
            {
                'AttributeName': 'userid',
                'KeyType': 'HASH'   # Partition key
            },
            {
                'AttributeName': 'username',
                'KeyType': 'RANGE'   # Sort key
            }
        ],
        AttributeDefinitions = [
            {
                'AttributeName': 'userid',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'username',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput = {
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    return table


def store_users(users, dynamodb=None):
    if not dynamodb:
        dynamodb = get_resource()

    table = dynamodb.Table('Users')
    for user in users:
        print(f'Adding user {user["username"]}')
        table.put_item(Item=user)


def get_user_by_id_username(id, username, dynamodb=None):
    if not dynamodb:
        dynamodb = get_resource()

    table = dynamodb.Table('Users')

    try:
        response = table.get_item(Key={'userid': id, 'username': username})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']


def get_user_by_id(id, dynamodb=None):
    if not dynamodb:
        dynamodb = get_resource()

    table = dynamodb.Table('Users')

    try:
        response = table.query(KeyConditionExpression=Key('userid').eq(id))
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Items']


def get_all_users(dynamodb=None):
    if not dynamodb:
        dynamodb = get_resource()

    table = dynamodb.Table('Users')

    try:
        response = table.scan()
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Items']

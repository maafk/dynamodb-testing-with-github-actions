import boto3
from unittest import TestCase, mock

from update_item import UpdateItem
import os
import json

client = boto3.client(
    'dynamodb', 
    endpoint_url='http://localhost:8000',
    aws_access_key_id='ABC123',
    aws_secret_access_key='DEF456')


TEST_TABLE_NAME = "SampleTestTableKittens"
TEST_SITE_URL = "rainbowkittensloths.com"

class DynamoTest(TestCase):
    def setUp(self):
        # Create table
        client.create_table(
            TableName=TEST_TABLE_NAME,
            KeySchema=[
                {
                    "AttributeName": "site_url",
                    "KeyType": "HASH"
                }
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "site_url",
                    "AttributeType": "S"
                }
            ],
            BillingMode="PAY_PER_REQUEST"
        )

    def tearDown(self):
        client.delete_table(
            TableName=TEST_TABLE_NAME
        )

    @mock.patch('update_item.TABLE_NAME', TEST_TABLE_NAME)
    @mock.patch('update_item.SITE_URL', TEST_SITE_URL)
    def test_update(self):
        test_obj = UpdateItem(client)
        response = test_obj.update_count()
        body_response = json.loads(response["body"])
        # assert count was incremented by one
        self.assertEqual(200, response['statusCode'])
        # assert incremented by 1
        self.assertEqual("1", body_response["Visit_Count"])

    @mock.patch('update_item.TABLE_NAME', TEST_TABLE_NAME)
    @mock.patch('update_item.SITE_URL', TEST_SITE_URL)
    def test_update_when_already_exists(self):
        test_obj = UpdateItem(client)
        response = test_obj.update_count()
        body_response = json.loads(response["body"])
        # assert count was incremented by one
        self.assertEqual(200, response['statusCode'])
        # assert incremented by 1
        self.assertEqual("1", body_response["Visit_Count"])

        response2 = test_obj.update_count()
        body_response2 = json.loads(response2["body"])
        self.assertEqual("2", body_response["Visit_Count"])
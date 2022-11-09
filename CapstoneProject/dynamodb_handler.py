import boto3
from decouple import config


# PATCH IN AWS CREDENTIALS BEFORE EVERY USE
AWS_ACCESS_KEY_ID     =""
AWS_SECRET_ACCESS_KEY =""
AWS_SESSION_TOKEN     =""
REGION_NAME           ="us-east-1"


client = boto3.client(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    aws_session_token     = AWS_SESSION_TOKEN,
    region_name           = REGION_NAME,
)

resource = boto3.resource(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    aws_session_token     = AWS_SESSION_TOKEN,
    region_name           = REGION_NAME,
)

# Creates our DynamoDb Table called "Food"
def CreatATableFood():
        
    client.create_table(
        AttributeDefinitions = [ # Name and type of the attributes 
            {
                'AttributeName': 'id',  # Name of the attribute
                'AttributeType': 'N',   # N -> Number (S -> String, B-> Binary)

                'AttributeName': 'food',
                'AttributeType': 'S',

                'AttributeName': 'price',
                'AttributeType': 'N',

                'AttributeName': 'truck',
                'AttributeType': 'S'
            }
        ],
        TableName = 'Food', # Name of the table 
        KeySchema = [       # Partition key/sort key attribute 
            {
                'AttributeName': 'id',   # 'HASH' -> partition key, 'RANGE' -> sort key
                'KeyType'      : 'HASH', 
            
                'AttributeName': 'truck',
                'KeyType'      : 'RANGE'
            }
        ],
        BillingMode = 'PAY_PER_REQUEST',
        Tags = [ # OPTIONAL 
            {
                'Key'  : 'test-resource',
                'Value': 'dynamodb-test'            }
        ]
    )


FoodTable = resource.Table('Food') # Defines FoodTable resource

def addItemToFood(id, food, price, type, truck): # Adds an item with attributes to the table
    response = FoodTable.put_item(
        Item = {
            'id'    :  id,
            'truck' :  truck,
            'food'  :  food,
            'price' :  price,
            'type'  :  type
        }
    )  
    return response


def GetItemFromFood(id): # Reads the attributes of an item from the DB with given ID
    response = FoodTable.get_item(
        Key = {
            'id'     : id,
        },
        AttributesToGet=[
            'id', 'food', 'price', 'type', 'truck'
        ]
    )   
    return response


def UpdateItemInFood(id, data:dict): # Updates an item listing in the DB | MORE FEATURES TO COME
    response = FoodTable.update_item(
        Key = {
            'id': id
        },
        AttributeUpdates={
            'food': {
                'Value'  : data['food'],
                'Action' : 'PUT' # available options -> DELETE(delete), PUT(set), ADD(increment)
            },
            'price': {
                'Value'  : data['price'],
                'Action' : 'PUT'
            }
          
        },
        ReturnValues = "UPDATED_NEW" # returns the new updated values
    )   
    return response

#### "LIKE" FEATURE BELOW IS IN BETA | NOT FULLY CONFIGURED ####

def LikeAFood(id):
    response = FoodTable.update_item(
        Key = {
            'id': id
        },
        AttributeUpdates = {
            'likes': {
                'Value'  : 1,   # Add '1' to the existing value
                'Action' : 'ADD'
            }
        },
        ReturnValues = "UPDATED_NEW"
    )    # The 'likes' value will be of type Decimal, which should be  converted to python int type, to pass the response in json format.    response['Attributes']['likes'] = int(response['Attributes']['likes']) 
    return response



def DeleteAnItemFromFood(id): # Deletes an entry from the DB altogether
    response = FoodTable.delete_item(
        Key = {
            'id': id
        }
    )    
    return response

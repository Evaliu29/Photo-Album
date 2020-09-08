from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from botocore.vendored import requests
import json
import boto3


def lambda_handler(event, context):
    id_recieved = '19953647'
    # content_recieved = "show me person and dog."
    print(event)
    content_recieved = event["params"]["querystring"]["q"]
    client = boto3.client('lex-runtime','us-east-1',verify=False)
    botresponse = client.post_text(
        botName='photo',
        botAlias='sarsa',
        userId=id_recieved,
        sessionAttributes={},
        requestAttributes={},
        inputText=content_recieved
    )
    
    response = {}
    response["id"] = id
    response["content"] = botresponse["message"]
    
    
    
    words = response["content"]
    keyword = words.split("+")
    photo_list = []
    for key in keyword:
          if key != "null":
             es_url = 'https://vpc-myphotos-xoaohoqea74p5cdtwn7sklyzce.us-east-2.es.amazonaws.com/photos/_search?q=' + key
             response = requests.get(es_url)
             data = response.json()
             for res in data["hits"]["hits"]:
                 photo_name = str(res["_source"]["objectKey"])
                 print(photo_name)
                 if photo_name not in photo_list:
                     photo_list.append(photo_name)

    return {
        'statusCode': 200,
        # 'elasticsearch': json.dumps(str(photo_set))
        'response': photo_list
        }


  

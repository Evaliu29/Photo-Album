import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

def lambda_handler(event, context):
    
    # get photo name and bucket
    s3 = event["Records"][0]["s3"]
    bucket = s3["bucket"]["name"]
    objectName = s3["object"]["key"]
    
    print(bucket)
    print(objectName)
    # get photo
    s3_client = boto3.client("s3")
    photo_res = s3_client.get_object(Bucket=bucket,Key=objectName)
    timestamp = photo_res['LastModified'].strftime('%Y-%m-%dT%H:%M:%S')
    photo_b = photo_res["Body"].read()
    # get labels
    rekog_client = boto3.client('rekognition')
    labels_res = rekog_client.detect_labels(
        Image={
            'Bytes': photo_b,
        },
        MaxLabels=123,MinConfidence=80.0)
    # build json object
    
    labels_all_info = labels_res["Labels"] 
    labels = []
    # parents = []
    for info in labels_all_info:
        labels.append(info["Name"])
    print(labels)
    result = {"objectKey":objectName,"bucket":bucket,"createdTimestamp": timestamp,"labels": labels}
    print(result)
    
    host = "vpc-myphotos-xoaohoqea74p5cdtwn7sklyzce.us-east-2.es.amazonaws.com"
    awsauth = AWS4Auth()

    es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    index_res = es.index(index="photos", doc_type="img", body=result)
    print(index_res)
    

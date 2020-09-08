import json
import base64
import boto3

def lambda_handler(event, context):
    # TODO implement
    print(event)
    filename = event["name"]
    file = event["file"]
    start = file.index("base64,")+7
    file_real = file[start:]
    bfile = bytes(file_real, 'utf-8')
    image_string = base64.decodestring(bfile)
    s3_client = boto3.client("s3")
    response = s3_client.put_object(Body=image_string, 
                      Bucket = "hw3-photo-bucket", 
                      Key = filename,
                      ACL='public-read',
                      ContentType= "images/jpeg")
    print("get s3 response")
    print(response)
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

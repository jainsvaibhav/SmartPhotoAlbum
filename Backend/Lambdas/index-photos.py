import json
import boto3
import requests
# from botocore.vendored import requests
import datetime


def lambda_handler(event, context):
    # s3client = boto3.client('s3')
    # metadata = s3client.head_object(Bucket='assign02-photos', Key="photo-1554151228-14d9def656e4.jpeg")
    # print("metadata", metadata['Metadata']["customlabel"])
    # given_labels = metadata['Metadata']["customlabel"].split(",")
    # print(given_labels)
    # TODO implement
    #print(json.dumps(event, indent=4, sort_keys=True))
    
    s3client = boto3.client('s3')
    s3_info = event['Records'][0]['s3']
    # print("s3_info", event)

    bucket_name = s3_info['bucket']['name']
    key_name = s3_info['object']['key']
    print("bucket", bucket_name, "key", key_name)
    metadata = s3client.head_object(Bucket=bucket_name, Key=key_name)
    print("metdata", metadata)
    given_labels = metadata.get('Metadata').get("customlabel")
    if given_labels:
        given_labels = given_labels.split(",")
    # given_labels = metadata['Metadata']["customlabel"].split(",")
        given_labels = [x.strip() for x in given_labels]
    else:
        given_labels = []
    print("given_labels", given_labels)
    #print(bucket_name)
    client = boto3.client('rekognition')
    pass_object = {'S3Object':{'Bucket':bucket_name,'Name':key_name}}
    
    resp = client.detect_labels(Image=pass_object)
    #print('<---------Now response object---------->')
    #print(json.dumps(resp, indent=4, sort_keys=True))
    timestamp =str(datetime.datetime.now())
    labels = []
    labels += given_labels
    #temp = resp['Labels'][0]['Name']
    for i in range(len(resp['Labels'])):
        labels.append(resp['Labels'][i]['Name'])
    print('<------------Now label list----------------->')
    print(labels)
    format = {'objectKey':key_name,'bucket':bucket_name,'createdTimestamp':timestamp,'labels':labels}
    required_json = json.dumps(format)
    print(required_json)
    #change url
    url = "https://search-photos-tb7fkcnibgpl6lv5l2vtnnzb2a.us-east-1.es.amazonaws.com/photos/_doc"
    headers = {"Content-Type": "application/json"}
    r = requests.post(url, data=json.dumps(format).encode("utf-8"), headers=headers,auth=('assign02', 'Assign@02'))
    #resp_elastic = requests.get(url2,headers={"Content-Type": "application/json"}).json()
    #print('<------------------GET-------------------->')
    print(r.text)
    #print(json.dumps(resp_elastic, indent=4, sort_keys=True))
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

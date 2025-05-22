from lambda_function import lambda_handler
from main import handle_text
import json

event ={
  "resource": "/",
  "path": "/",
  "httpMethod": "POST",
  "headers": {
    "content-type": "application/json; charset=utf-8",
    "Host": "g0z0jst2h9.execute-api.us-west-2.amazonaws.com",
    "User-Agent": "LineBotWebhook/2.0",
    "X-Amzn-Trace-Id": "Root=1-682ed4b1-72bc329b15b32d6f15b19b6c",
    "X-Forwarded-For": "147.92.150.196",
    "X-Forwarded-Port": "443",
    "X-Forwarded-Proto": "https",
    "x-line-signature": "dibw1BYfyxCvz24SNk6iSwEO9rlWa0A5lRbzx+P6JLo="
  },
  "multiValueHeaders": {
    "content-type": ["application/json; charset=utf-8"],
    "Host": ["g0z0jst2h9.execute-api.us-west-2.amazonaws.com"],
    "User-Agent": ["LineBotWebhook/2.0"],
    "X-Amzn-Trace-Id": ["Root=1-682ed4b1-72bc329b15b32d6f15b19b6c"],
    "X-Forwarded-For": ["147.92.150.196"],
    "X-Forwarded-Port": ["443"],
    "X-Forwarded-Proto": ["https"],
    "x-line-signature": ["dibw1BYfyxCvz24SNk6iSwEO9rlWa0A5lRbzx+P6JLo="]
  },
  "queryStringParameters": None,
  "multiValueQueryStringParameters": None,
  "pathParameters": None,
  "stageVariables": None,
  "requestContext": {
    "resourceId": "sy60rqhhni",
    "resourcePath": "/",
    "httpMethod": "POST",
    "extendedRequestId": "K9Yr2FDevHcELyg=",
    "requestTime": "22/May/2025:07:39:29 +0000",
    "path": "/dev",
    "accountId": "885964308498",
    "protocol": "HTTP/1.1",
    "stage": "dev",
    "domainPrefix": "g0z0jst2h9",
    "requestTimeEpoch": 1747899569874,
    "requestId": "b4cab704-6c8c-4cf6-8f04-82e8e4afd9a5",
    "identity": {
      "cognitoIdentityPoolId": None,
      "accountId": None,
      "cognitoIdentityId": None,
      "caller": None,
      "sourceIp": "147.92.150.196",
      "principalOrgId": None,
      "accessKey": None,
      "cognitoAuthenticationType": None,
      "cognitoAuthenticationProvider": None,
      "userArn": None,
      "userAgent": "LineBotWebhook/2.0",
      "user": None
    },
    "domainName": "g0z0jst2h9.execute-api.us-west-2.amazonaws.com",
    "deploymentId": "za18su",
    "apiId": "g0z0jst2h9"
  },
  "body": "{\"destination\":\"Ue148f938f1291ddf04c5ce94cd64f91d\",\"events\":[{\"type\":\"message\",\"message\":{\"type\":\"text\",\"id\":\"562151265547583991\",\"quoteToken\":\"172hlPX3x4AcmJ0uJ-ixYQBZeLuO35fz_EWdqsWorqlr5f39-X4tthh090LTX7kYE7c7aYSpdoftdt7O28NVeyTzMhsQXRFtS2JZ1Cw5-f1utQwxhgTWzQhmV8O2KQ2IJRRBd8YP9niDaEYMrWkJ4g\",\"text\":\"あ\"},\"webhookEventId\":\"01JVVEXN54RNC8WEN9W088QFR3\",\"deliveryContext\":{\"isRedelivery\":false},\"timestamp\":1747899569004,\"source\":{\"type\":\"user\",\"userId\":\"U8f56cd9b4b68e5ca3fb0d9b7a7ece549\"},\"replyToken\":\"31a76df593b049bf9951dfbbbffa712e\",\"mode\":\"active\"}]}",
  "isBase64Encoded": False
}

context = {
    
}

body = json.loads(event["body"])
events = body["events"][0]["message"]["text"]
message = events
print(handle_text(message))
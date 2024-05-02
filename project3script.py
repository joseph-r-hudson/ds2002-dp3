import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/rck7ye"
sqs = boto3.client('sqs')

orders=[]
words=[]
handles=[]

def get_message(amount_of_messages):
    for i in range(amount_of_messages):
        try:
            # Receive message from SQS queue. Each message has two MessageAttributes: order and word
            # You want to extract these two attributes to reassemble the message
            response = sqs.receive_message(
                QueueUrl=url,
                AttributeNames=[
                    'All'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ]
            )
            # Check if there is a message in the queue or not
            if "Messages" in response:
                # extract the two message attributes you want to use as variables
                # extract the handle for deletion later
                order = response['Messages'][0]['MessageAttributes']['order']['StringValue']
                word = response['Messages'][0]['MessageAttributes']['word']['StringValue']
                handle = response['Messages'][0]['ReceiptHandle']
                orders.append(order)
                words.append(word)
                handles.append(handle)
                print(f"Order: {order}")
                print(f"Word: {word}")

                # Print the message attributes - this is what you want to work with to reassemble the messag

            # If there is no message in the queue, print a message and exit    
            else:
                exit(1)
                
        # Handle any errors that may occur connecting to SQS
        except ClientError as e:
            print(e.response['Error']['Message'])
    

get_message(10)


pairs = zip(orders, words)
sorted_pairs = sorted(pairs, key=lambda x: x[0])
sorted_words = [pair[1] for pair in sorted_pairs]

phrase=""
for i in sorted_words:

    phrase+= " "+i

print(phrase)

def delete_message(handle):
    try:
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])

for i in handles:
  delete_message(i)
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 20:03:41 2020

@author: Shreya_agrawal
"""

import json
import boto3
from tweet_prep import Preprocessor
from datetime import datetime
import time

#connecting to low level interfaces using Boto3 to access Sagemaker for model
#inferencing and s3 for logging json payload

runtime = boto3.client("runtime.sagemaker")
s3_access = boto3.client("s3")

my_prep = Preprocessor(pad_length_tweet=50, max_length_dictionary=100000)


def lambda_handler(event, context):
    
    request_time = datetime.now()
    tweet = event["tweet"]
    
    #preprocessing and storing the time
    t_start_prep = time.time()
    features = my_prep.tweet_process(tweet)
    t_stop_prep = time.time()

    sentiment_model_payload = {
        'features_input' : features
        }
    
    #output of sentiment model created earlier
    #model inference being run and time stored
    t_start_model = time.time()
    output = runtime.invoke_endpoint(
            EndpointName = "ai-sentiment-model", 
            ContentType = "application/json",
            Body = json.dumps(sentiment_model_payload))
    
    result = json.loads(output["Body"].read().decode())
    t_stop_model = time.time()
    
    response = {}    
    #post-processing logic, converting numbers to sentiment
    
    #response["Date and Time of request"] = str(request_time)
    #response["Tweet"] = tweet
    
    if result["predictions"][0][0] >= 0.5:
        response["sentiment"] = "positive"
    else:
        response["sentiment"] = "negative"
               
    #calculating preprocessing time
    prep_time =  t_stop_prep - t_start_prep 
    #calculating model inference time
    model_time =  t_stop_model - t_start_model 
    
    #response["Probability"] = result["predictions"][0][0]
    #response["Preprocessing Time"] = str(round(prep_time, 2))
    #response["Model Inference Time"] = str(round(model_time, 2))
    
    #s3_access.put_object(
            #Body = json.dumps(response),
            #Bucket = "assign5-aiops",
            #Key = "Payload.{}.txt".format(response["Date and Time of request"]))
            
        
  
    print("Result: " + json.dumps(response, indent = 2))
   
    
    return response
# import py library to call AWS APIs
import boto3
import botocore 

import json
import os
import logging

# init logger
logger = logging.getLogger()
logger.setLevel("INFO")

def lambda_handler(event, context):
    """
    Main Lambda Handler Func
    params:
        event: dictionary containing lambda func event data
        context: lambda runtime context
    returns:
        dictionary with status message
    """
    try:
        text = event['Text']
        source_lang = event['Source-Lang']
        target_lang = event['Target-Lang']
        
        logger.info(f"Translate requested for {text} in language {source_lang} to language {target_lang}")
        return {
            "statusCode": 200,
            "message": "Request Success"
        }
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise




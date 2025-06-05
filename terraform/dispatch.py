import boto3
import json
import logging

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS Translate client
translate = boto3.client('translate')

def lambda_handler(event, context):
    """
    Lambda function to translate input text from source to target language.
    
    Parameters:
        event (dict): Lambda event payload
        context (LambdaContext): Runtime context (unused)
        
    Returns:
        dict: HTTP-style response with translation or error message
    """
    try:
        # Parse input from HTTP POST body
        body = json.loads(event.get("body", "{}"))
        text = body.get("Text")
        source_lang = body.get("Source-Lang", "en")
        target_lang = body.get("Target-Lang", "es")
        
        if not text:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'Text' in request body."})
            }
        
        logger.info(f"Translating: '{text}' from {source_lang} to {target_lang}")
        
        # Perform translation
        response = translate.translate_text(
            Text=text,
            SourceLanguageCode=source_lang,
            TargetLanguageCode=target_lang
        )
        
        translated_text = response.get("TranslatedText", "")
        return {
            "statusCode": 200,
            "body": json.dumps({
                "original": text,
                "translated": translated_text,
                "source_language": source_lang,
                "target_language": target_lang
            })
        }
    
    except Exception as e:
        logger.error(f"Translation failed: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"})
        }



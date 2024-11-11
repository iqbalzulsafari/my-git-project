import os
import time
from dotenv import load_dotenv
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes

load_dotenv()

# Load credentials from environment variables
endpoint = os.getenv('AZURE_ENDPOINT')
key = os.getenv('AZURE_SUBSCRIPTION_KEY')

# Ensure that credentials are loaded properly
if not endpoint or not key:
    raise ValueError("Azure credentials not set. Ensure AZURE_ENDPOINT and AZURE_SUBSCRIPTION_KEY are configured.")

# Initialize the Computer Vision Client with the credentials
credentials = CognitiveServicesCredentials(key)
client = ComputerVisionClient(endpoint=endpoint, credentials=credentials)

def read_image(uri):
    numberOfCharsInOperationId = 36
    maxRetries = 10

    # SDK call to start the read operation
    rawHttpResponse = client.read(uri, language="en", raw=True)

    # Extract the operation ID from the response headers
    operationLocation = rawHttpResponse.headers["Operation-Location"]
    operationId = operationLocation[-numberOfCharsInOperationId:]

    # Get the result of the read operation
    retry = 0
    result = client.get_read_result(operationId)

    # Retry while the status is 'notstarted' or 'running'
    while retry < maxRetries:
        if result.status.lower() not in ['notstarted', 'running']:
            break
        time.sleep(1)
        result = client.get_read_result(operationId)
        retry += 1
    
    if retry == maxRetries:
        return "Max retries reached"

    # Check if the operation was successful
    if result.status == OperationStatusCodes.succeeded:
        return " ".join([line.text for line in result.analyze_result.read_results[0].lines])
    else:
        return "Error: Text extraction failed"

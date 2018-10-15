from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import http.client
import urllib.request
import urllib.parse
import urllib.error
import base64
import requests
import time
import json


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def transcribeImage(request):
    if request.method != 'GET':
        return JsonResponse({'status_code': 400, 'message': "Error, please use GET." }, status=400)

    print ("IN T I")
    imageURL = request.GET.get('imageURL', '')
    print ("IMAGE URL: " + imageURL)
    # Keys
    endpoint = 'https://westus.api.cognitive.microsoft.com/vision/v1.0/recognizeText?handwriting=true'
    api_key = '1f35edac14fb482dbe11ae493fbb6652'

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': api_key,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'handwriting': 'true',
    })

    body = {'url': imageURL }

    try:
        response = requests.request('POST', endpoint, json=body, data=None, headers=headers, params=None)
        print ("REQUEST MADE")
        if response.status_code != 202:
            # Display JSON data and exit if the REST API call was not successful.
            parsed = json.loads(response.text)
            print ("Error:")
            print (json.dumps(parsed, sort_keys=True, indent=2))
            exit()

        # grab the 'Operation-Location' from the response
        operationLocation = response.headers['Operation-Location']

        print('\nHandwritten text submitted. Waiting 10 seconds to retrieve the recognized text.\n')
        time.sleep(10)

        # Execute the second REST API call and get the response.
        response = requests.request('GET', operationLocation, json=None, data=None, headers=headers, params=None)

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(response.text)

        lines = parsed['recognitionResult']['lines']

        # this opens the file for writing
        with open("mynote.txt", "w") as f:
            for line in reversed(lines):
                print(line['text'])
                # write the value to the file
                f.write(line['text'])

        return JsonResponse({'status_code': 200, 'pandaDescription': descriptionJson}, status=200)

    except Exception as e:
        print('Error:')
        print(e)

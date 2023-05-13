from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def submit_choice(request):
    if request.method == 'POST':
        data = parseJsonToDictionary(request.body)
        return JsonResponse({'status': 'success', "data": data})
    else:
        return JsonResponse({'status': 'error'})


def parseJsonToDictionary(body):
    return json.loads(body.decode("utf-8"))
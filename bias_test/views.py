from django.http import JsonResponse

def submit_choice(request):
    print(request)
    if request.method == 'POST':
        question_index = request.POST.get('question_index')
        choice_index = request.POST.get('choice_index')
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})
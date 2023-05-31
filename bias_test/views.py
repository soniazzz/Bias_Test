from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bias_test.models import BiasTestQuestion, User
from django.core.exceptions import ObjectDoesNotExist

import json
def calculate_result(result):
    for key in result:
        result[key] = result[key] *2/3
    return result
@csrf_exempt
def submit_choice(request):
    if request.method == 'POST':
        #get user responses
        data = parseJsonToDictionary(request.body)
        print(data)
        responses = data.get('responses')
        user_id = data.get('user_id')

        #convert responses
        result = calculate_result(responses)



        # Retrieve the user instance with the given user_id
        user = User.objects.get(user_id=user_id)

        # Update the possibility biases fields based on the result dictionary
        user.update_possibility_biases(result)

        print("Responses:", result)
        print("User_ID:", user_id)

        return JsonResponse({'status': 'success', "data": data})
    else:
        return JsonResponse({'status': 'error'})





def parseJsonToDictionary(body):
    return json.loads(body.decode("utf-8"))


@csrf_exempt
def get_questions(request):
    if request.method == 'GET':
        try:
            # Retrieve 2 random questions from the database
            questions = BiasTestQuestion.objects.order_by('?')[:5]
            # Convert the questions to a list of dictionaries
            questions_list = []
            for question in questions:
                question_dict = {
                    'question': question.question_text,
                    'choices': [
                        {'option': question.option_A, 'points': question.point_for_optionA},
                        {'option': question.option_B, 'points': question.point_for_optionB},
                        {'option': question.option_C, 'points': question.point_for_optionC},
                        {'option': question.option_D, 'points': question.point_for_optionD},
                    ],
                    'index': question.test_for_bias_index
                }
                questions_list.append(question_dict)
        except:
            errormessgae="error_here:("
        # Return the questions as a JSON response
        return JsonResponse(questions_list, safe=False)


def get_bias_results(request, user_id):
    if request.method == 'GET':
        print("hahah")
        try:
            user = User.objects.get(user_id=user_id)
            data = {
                "possibility_biases_1": user.possibility_biases_1,
                "possibility_biases_2": user.possibility_biases_2,
                "possibility_biases_3": user.possibility_biases_3,
                "possibility_biases_4": user.possibility_biases_4,
                "possibility_biases_5": user.possibility_biases_5,
            }
            print(data)
            return JsonResponse(data, safe=False)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)



@csrf_exempt
def signup(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        result={}
        result["username"] = data.get("username")
        result["password"] = data.get("password")
        result["phone_number"] = data.get("phone_number")
        result["team"] = data.get("team")

        if User.objects.filter(user_name=result["username"]).exists():
            print("Username already exists.")
            return JsonResponse({"error": "Username already exists."})

        # Create a new user instance and set the fields
        user = User(user_name=result["username"], phone_number=result["phone_number"], team=result["team"],password=result["password"])
        user.save()

        return JsonResponse({"user_id": user.user_id})
        print("signup" + user.user_id)

    return JsonResponse({"error": "Invalid request method."})

@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        try:
            user = User.objects.get(user_name=username)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "User does not exist."})

        if user.password == password:
            print(user.user_id)
            return JsonResponse({"user_id": user.user_id})
        else:
            return JsonResponse({"error": "Wrong password."})

        return JsonResponse({"error": "Error in login."})
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bias_test.models import BiasTestQuestion, User, UserSession, Article
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import datetime, timedelta
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

            p1 = str(int(user.possibility_biases_1 * 100)) + "%"
            p2 = str(int(user.possibility_biases_2 * 100)) + "%"
            p3 = str(int(user.possibility_biases_3 * 100)) + "%"
            p4 = str(int(user.possibility_biases_4 * 100)) + "%"
            p5 = str(int(user.possibility_biases_5 * 100)) + "%"

            data = {
                "Possibility of Gender Bias": p1,
                "Possibility of Racial Bias": p2,
                "Possibility of Age Bias": p3,
                "Possibility of Height Bias": p4,
                "Possibility of Affinity Bias": p5,
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
            UserSession.objects.filter(session_token=user.user_id).delete()
            UserSession(session_token=user.user_id).save()
            return JsonResponse({"user_id": user.user_id})
        else:
            return JsonResponse({"error": "Wrong password."})

        return JsonResponse({"error": "Error in login."})


def get_profile(request, user_id):
    if not is_session_valid(user_id):
        return HttpResponseForbidden()

    if request.method == 'GET':
        print(request.session.get("user_id"))
        print("profile")
        try:
            user = User.objects.get(user_id=user_id)
            p1 = str(int(user.possibility_biases_1 * 100)) + "%"
            p2 = str(int(user.possibility_biases_2 * 100)) + "%"
            p3 = str(int(user.possibility_biases_3 * 100)) + "%"
            p4 = str(int(user.possibility_biases_4 * 100)) + "%"
            p5 = str(int(user.possibility_biases_5 * 100)) + "%"
            name= user.user_name
            phone=user.phone_number
            team=user.team
            avatar=user.avatar

            # Retrieve 5 random articles from the database
            articles = Article.objects.order_by('?')[:5]
            # Convert the questions to a list of dictionaries
            articles_list = []
            for article in articles:
                article_dict = {
                    'bias_index': article.bias_index,
                    'head': article.head,
                    'brief': article.brief,
                    'img': article.img,
                    'link': article.link
                }
                articles_list.append(article_dict)



            data = {
                "Possibility of Gender Bias": p1,
                "Possibility of Racial Bias": p2,
                "Possibility of Age Bias": p3,
                "Possibility of Height Bias": p4,
                "Possibility of Affinity Bias": p5,
            }

            info= {
                "name": name,
                "phone": phone,
                "team": team,
                "avatar": avatar,
            }


            package={"data":data,"info":info, "articles_list":articles_list}

            return JsonResponse(package, safe=False)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)


@csrf_exempt
def editProfile(request, user_id):

    if request.method == "POST":
        user = User.objects.get(user_id=user_id)
        data = json.loads(request.body)
        print(data)
        result={}
        result["username"] = data.get("username")
        result["phone_number"] = data.get("phone_number")
        result["team"] = data.get("team")
        result["avatar"]=data.get("avatar")

        if ((User.objects.filter(user_name=result["username"]).exists()) and ((result["username"]!=user.user_name))):
                print("Username already exists.")
                return JsonResponse({"error": "Username already exists."})

        # Create a new user instance and set the fields
        user.user_name=result["username"]
        user.team=result["team"]
        user.phone_number=result["phone_number"]
        user.avatar=result["avatar"]
        user.save()

        return JsonResponse({"user_id": user.user_id})


    return JsonResponse({"error": "Invalid request method."})

@csrf_exempt
def authenticate_session_token(request):
    if request.method == 'POST':
        data = parseJsonToDictionary(request.body)
        if is_session_valid(data.get("session_token")):
            return HttpResponse("Success")
        else:
            return HttpResponseForbidden("Failure")


SESSION_EXPIRY = timedelta(hours=6)
def is_session_valid(user_id):
    stored_session = UserSession.objects.filter(session_token=user_id).first()
    if stored_session is None:
        return False

    creation_datetime = stored_session.creation_timestamp
    if timezone.now() - creation_datetime > SESSION_EXPIRY:
        stored_session.delete()
        return False

    return True


def get_articles(request):
    if request.method == 'GET':
        try:
            # Retrieve 5 random articles from the database
            articles = Article.objects.order_by('?')[:5]
            # Convert the questions to a list of dictionaries
            articles_list = []
            for article in articles:
                article_dict = {
                    'bias_index': article.bias_index,
                    'head': article.head,
                    'brief': article.brief,
                    'img': article.img,
                    'link': article.link
                }
                articles_list.append(article_dict)
        except:
            errormessgae="error_here:("
        # Return the questions as a JSON response
        return JsonResponse(articles_list, safe=False)


@csrf_exempt
def logout(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get("user_id")

        UserSession.objects.filter(session_token=user_id).delete()
        return JsonResponse({"status": "Logged out."})

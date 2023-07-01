from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bias_test.models import BiasTestQuestion, User, UserSession, Article, Post, Reply
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import datetime, timedelta
from random import shuffle
import json


def calculate_result(result):
    for key in result:
        result[key] = result[key] / 4 / 10
    return result


@csrf_exempt
def submit_choice(request):
    if request.method == 'POST':
        # get user responses
        data = parseJsonToDictionary(request.body)
        print(data)
        responses = data.get('responses')
        user_id = data.get('user_id')

        # convert responses
        result = calculate_result(responses)

        # Retrieve the user instance with the given user_id
        user = User.objects.get(user_id=user_id)

        # Update the possibility biases fields based on the result dictionary
        user.update_possibility_biases(result)

        ##print("Responses:", result)
        ##print("User_ID:", user_id)

        return JsonResponse({'status': 'success', "data": data})
    else:
        return JsonResponse({'status': 'error'})


def parseJsonToDictionary(body):
    return json.loads(body.decode("utf-8"))


@csrf_exempt
def get_questions(request):
    if request.method == 'GET':
        try:
            questions_list = []

            # Retrieve 2 random questions for each bias type index
            for bias_type_index in range(1, 6):
                questions = BiasTestQuestion.objects.filter(test_for_bias_index=bias_type_index).order_by('?')[:2]

                # Convert the questions to a list of dictionaries
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

            # Shuffle the questions to randomize the order

            shuffle(questions_list)
        except:
            errormessgae = "error_here:("
        # Return the questions as a JSON response
        return JsonResponse(questions_list, safe=False)


def get_bias_results(request, user_id):
    if request.method == 'GET':
        ##print("hahah")
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
            ##print(data)
            return JsonResponse(data, safe=False)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)


@csrf_exempt
def signup(request):
    if request.method == "POST":
        data = json.loads(request.body)
        ##print(data)
        result = {}
        result["username"] = data.get("username")
        result["password"] = data.get("password")
        result["phone_number"] = data.get("phone_number")
        result["team"] = data.get("team")

        if User.objects.filter(user_name=result["username"]).exists():
            ##print("Username already exists.")
            return JsonResponse({"error": "Username already exists."})

        # Create a new user instance and set the fields
        user = User(user_name=result["username"], phone_number=result["phone_number"], team=result["team"],
                    password=result["password"])
        user.save()

        return JsonResponse({"user_id": user.user_id})
        ##print("signup" + user.user_id)

    return JsonResponse({"error": "Invalid request method."})


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        ##print(username,password)

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
        ##print(request.session.get("user_id"))
        ##print("profile")
        try:
            user = User.objects.get(user_id=user_id)
            p1 = str(int(user.possibility_biases_1 * 100)) + "%"
            p2 = str(int(user.possibility_biases_2 * 100)) + "%"
            p3 = str(int(user.possibility_biases_3 * 100)) + "%"
            p4 = str(int(user.possibility_biases_4 * 100)) + "%"
            p5 = str(int(user.possibility_biases_5 * 100)) + "%"
            name = user.user_name
            phone = user.phone_number
            team = user.team
            avatar = user.avatar

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

            info = {
                "name": name,
                "phone": phone,
                "team": team,
                "avatar": avatar,
            }

            package = {"data": data, "info": info, "articles_list": articles_list}

            return JsonResponse(package, safe=False)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)


@csrf_exempt
def editProfile(request, user_id):
    if request.method == "POST":
        user = User.objects.get(user_id=user_id)
        data = json.loads(request.body)
        ##print(data)
        result = {}
        result["username"] = data.get("username")
        result["phone_number"] = data.get("phone_number")
        result["team"] = data.get("team")
        result["avatar"] = data.get("avatar")

        if ((User.objects.filter(user_name=result["username"]).exists()) and ((result["username"] != user.user_name))):
            ##print("Username already exists.")
            return JsonResponse({"error": "Username already exists."})

        # Create a new user instance and set the fields
        user.user_name = result["username"]
        user.team = result["team"]
        user.phone_number = result["phone_number"]
        user.avatar = result["avatar"]
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
        articles_list = []
        for bias in range(1, 6):
            try:
                # Retrieve a random article with the current bias_index
                article = Article.objects.filter(bias_index=bias).order_by('?').first()
                if article:
                    article_dict = {
                        'bias_index': article.bias_index,
                        'head': article.head,
                        'brief': article.brief,
                        'img': article.img,
                        'link': article.link
                    }
                    articles_list.append(article_dict)
                shuffle(articles_list)
            except ObjectDoesNotExist:
                pass

        recommend_article = Article.objects.order_by('?').first()
        if recommend_article:
            recommend_info = {
                'bias_index': recommend_article.bias_index,
                'head': recommend_article.head,
                'brief': recommend_article.brief,
                'img': recommend_article.img,
                'link': recommend_article.link
            }
        else:
            recommend_info = None

        result_dic = {"article": articles_list, 'recommend': recommend_info}

        # Return the questions as a JSON response
        return JsonResponse(result_dic, safe=False)


def get_articles_of_type(request, bias_index, page):
    if request.method == 'GET':
        articles_per_page = 6
        start = (page - 1) * articles_per_page
        end = page * articles_per_page

        articles = Article.objects.filter(bias_index=bias_index)[start:end]
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

        recommend_article = Article.objects.filter(bias_index=bias_index).order_by('?').first()
        if recommend_article:
            recommend_info = {
                'bias_index': recommend_article.bias_index,
                'head': recommend_article.head,
                'brief': recommend_article.brief,
                'img': recommend_article.img,
                'link': recommend_article.link
            }
        else:
            recommend_info = None

        total_articles = len(Article.objects.filter(bias_index=bias_index))



        result_dic = {"article": articles_list, 'recommend': recommend_info, 'total': total_articles}
        return JsonResponse(result_dic, safe=False)


@csrf_exempt
def logout(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get("user_id")

        UserSession.objects.filter(session_token=user_id).delete()
        return JsonResponse({"status": "Logged out."})


def get_posts_of_type(request, bias_index):
    if request.method == 'GET':
        print(bias_index)


        if bias_index == 0:
            posts = Post.objects.all()


        elif bias_index == 6:
            posts = Post.objects.order_by('?')[:4]

        else:
            posts = Post.objects.filter(bias_index=bias_index)

        posts_list = []
        for post in posts:
            user = User.objects.get(user_id=post.poster_id)
            print(post.post_id)
            replies = fetch_replies(post.post_id, None)
            post_dict = {
                'title': post.post_title,
                'poster': user.user_name,
                'details': post.post_details,
                'postDate': post.post_time,
                'numberOfReplies': count_replies(replies),
                'bias_index': post.bias_index,
                'post_index': post.post_id
            }
            posts_list.append(post_dict)

        result_dic = {"posts": posts_list}
        return JsonResponse(result_dic, safe=False)


def count_replies(reply_list):
    total_count = 0
    for reply in reply_list:
        total_count += 1  # Count the current reply
        total_count += count_replies(reply['replies'])  # Count all sub-replies
    print('num of replies:'+str(total_count))
    return total_count


# views.py
def fetch_replies(post_index, parent_reply):
    replies = Reply.objects.filter(post_id=post_index, parent_reply=parent_reply)
    reply_list = []
    for reply in replies:
        print(reply)
        user = User.objects.get(user_id=reply.poster_id)
        reply_data = {
            'id': reply.reply_index,
            'title': reply.title,
            'poster': user.user_name,
            'avatar': user.avatar,
            'postDate': reply.post_date,
            'details': reply.details,
            'replies': fetch_replies(post_index, reply)
        }

        reply_list.append(reply_data)


    return reply_list


def get_post(request, post_index):
    if request.method == 'GET':
        post = Post.objects.get(post_id=post_index)
        user = User.objects.get(user_id=post.poster_id)

        # Fetch replies
        replies = fetch_replies(post_index, None)

        post_dict = {
            'title': post.post_title,
            'poster': user.user_name,
            'details': post.post_details,
            'postDate': post.post_time,
            'numberOfReplies': count_replies(replies),
            'posterAvatar': user.avatar,
            'bias_index': post.bias_index,
            'post_index': post.post_id,
        }

        result_dic = {"post": post_dict, 'replies': replies}
        print (result_dic['replies'])
        return JsonResponse(result_dic, safe=False)


@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post = Post(
            bias_index=data['bias_index'],
            poster_id=data['poster_id'],
            post_title=data['post_title'],
            post_details=data['post_details']
        )
        post.save()
        return JsonResponse({'status': 'success', 'post_id': post.post_id})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

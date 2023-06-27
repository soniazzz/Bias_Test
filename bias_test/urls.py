from django.urls import path
from .views import submit_choice,get_questions, get_bias_results, signup, login, get_profile,editProfile, authenticate_session_token, get_articles, get_articles_of_type, logout, get_posts_of_type
urlpatterns = [
    path('api/submit-choice/', submit_choice, name='submit_choice'),
    path('api/get-questions/', get_questions, name='get_questions'),
    path('api/get-bias-results/<int:user_id>/', get_bias_results, name='get_bias_results'),
    path('api/get-profile/<int:user_id>/', get_profile, name='get_profile'),
    path('api/signup/', signup, name='signup'),
    path('api/login/', login, name='login'),
    path('api/edit-profile/<int:user_id>/', editProfile, name='editProfile'),
    path('api/authenticate-session', authenticate_session_token, name='authenticate-session'),
    path('api/get-articles/', get_articles, name='get_articles'),
    path('api/get-articles_of_type/<int:bias_index>/<int:page>/', get_articles_of_type, name='get_articles_of_type'),
    path('api/logout/', logout, name='logout'),
    path('api/posts/<int:bias_index>/', get_posts_of_type, name='posts-of-type')
]

from django.urls import path
from .views import submit_choice,get_questions, get_bias_results

urlpatterns = [
    path('api/submit-choice/', submit_choice, name='submit_choice'),
    path('api/get-questions/', get_questions, name='get_questions'),
    path('api/get-bias-results/<int:user_id>/', get_bias_results, name='get_bias_results'),
]
from django.urls import path
from .views import submit_choice,get_questions

urlpatterns = [
    path('api/submit-choice/', submit_choice, name='submit_choice'),
    path('api/get-questions/', get_questions, name='get_questions'),
]
from django.urls import path
from .views import submit_choice

urlpatterns = [
    path('api/submit-choice/', submit_choice, name='submit_choice'),
]
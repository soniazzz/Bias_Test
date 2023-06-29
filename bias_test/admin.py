from django.contrib import admin
from .models import BiasTestQuestion,User, UserSession, Article, Post, Reply

admin.site.register(BiasTestQuestion)
admin.site.register(User)
admin.site.register(UserSession)
admin.site.register(Article)
admin.site.register(Post)
admin.site.register(Reply)
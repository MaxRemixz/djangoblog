from django.contrib import admin
from .models import User, Blog_Articles, Comment

admin.site.register(User)
admin.site.register(Blog_Articles)
admin.site.register(Comment)

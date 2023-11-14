from django.contrib import admin

# Register your models here.
from .models import Hub, Article

admin.site.register(Hub)
admin.site.register(Article)

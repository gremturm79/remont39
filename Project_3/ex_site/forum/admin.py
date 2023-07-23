from django.contrib import admin
from .models import Category, Thread, Reply

admin.site.register(Category)
admin.site.register(Reply)
admin.site.register(Thread)

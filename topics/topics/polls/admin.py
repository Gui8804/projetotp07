from django.contrib import admin
from .models import Topic


class TopicsAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'description']
    
admin.site.register(Topic)

# Register your models here.

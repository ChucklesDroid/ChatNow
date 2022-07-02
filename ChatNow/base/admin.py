from django.contrib import admin
from .models import Topic, Room, Messages

admin.site.register(Topic)
admin.site.register(Room)
admin.site.register(Messages)


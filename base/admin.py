from django.contrib import admin
from .models import User, Base, Agent
# Register your models here.

admin.site.register(User)
admin.site.register(Base)
admin.site.register(Agent)
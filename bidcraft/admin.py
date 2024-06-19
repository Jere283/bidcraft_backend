from django.contrib import admin
from .models import User
from .models import Role

admin.site.register(User)
admin.site.register(Role)


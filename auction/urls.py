
from django.contrib import admin
from django.urls import path

from users import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('newUser/', v.register_new_user.as_view())
]

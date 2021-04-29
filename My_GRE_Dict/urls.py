"""My_GRE_Dict URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pages.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('manage/', manage_view),
    path('manage/clear_db', clear_database),
    path('manage/refresh_words', refresh_words),
    path('manage/reset_all_weights_to_max', reset_all_weights_to_max),
    path('manage/initialize_db_with_magoosh1000', initialize_db_with_magoosh1000),
    path('add_new_word', add_new_word),
]

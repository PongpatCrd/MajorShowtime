"""MajorShowtime URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from major_showtime.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('movies/', movies, name="movies"),
    path('movies/movies_status_configs/', movie_status_configs, name="movies_status_configs"),
    path('movies/movies_configs/', add_or_update_movie_detail, name="add_or_update_movie_detail"),
    path('movies/create_movie_detail_edit_modal/', create_movie_detail_edit_modal, name="create_movie_detail_edit_modal"),
    path('times/', time_setting, name="time_setting"),
    path('times/create_best_time_modal', update_branch_times, name="update_branch_time"),
    path('showtime/', showtimes, name="showtimes"),
    path('showtime/updates', update_showtime_screen_details, name="update_showtimes"),
    path('regions/', region_setting, name="region_setting"),
    path('region_create_or_update/', create_or_update_region, name="create_or_update_region")
]

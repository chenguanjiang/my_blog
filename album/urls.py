from django.urls import path

from album import views

app_name = 'album'

urlpatterns = [
    path('album-list/', views.album_list, name='album_list'),
]

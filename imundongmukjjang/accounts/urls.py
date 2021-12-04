from django.urls import path
#from imundongmukjjang.views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name="accounts"

urlpatterns = [
    #path('search/', map_search, name="map_search"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
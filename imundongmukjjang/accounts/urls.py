from django.urls import path
#from imundongmukjjang.views import *
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name="accounts"

urlpatterns = [
    #path('search/', map_search, name="map_search"),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('mypage/', mypage, name="mypage"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
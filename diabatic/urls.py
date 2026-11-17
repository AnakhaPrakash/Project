"""diabatic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.first),
    path('index/',views.index),

    path('login/logint',views.logint),
    path('login/',views.login, name="login"),
    path('userss',views.userss),
    path('adduser',views.adduser),
    path('logout/',views.logout),
    path('viewuser/',views.viewuser),
    path('viewresult',views.viewresult , name='viewresult'),
    path('addexpert/',views.addexpert, name="addexpert"),
    path('expert',views.expert),
    path('viewexpert/',views.viewexpert),
    path('prediction/pred',views.pred, name="pred"),
    path('prediction/',views.prediction, name='prediction'),
    path('viewresults',views.viewresults),
    path('diet/',views.diet),
    path('rec/',views.rec),
    path('rec/addrec',views.addrec),
    path('forget_password',views.forget_password, name="forget_password"),
    path('feedback',views.feedback),
    path('addfeedback',views.addfeedback),
    path('viewfeedback',views.viewfeedback),
    path('viewrecomment',views.viewrecomment, name="recommendations_list"),
    
    path('edit_recommendation/<int:id>/',views.edit_recommendation, name="edit_recommendation"),
    
    path('viewrequest/',views.viewrequest, name="viewrequest"),
    path('accept/<int:id>/',views.accept, name="accept"),
    path('reject/<int:id>/',views.reject, name="reject"),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('chatbot-response/', views.chatbot_response, name='chatbot-response'),

    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

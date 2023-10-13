"""
URL configuration for projectname project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from appname import views

urlpatterns = [
    path('', include('appname.urls')), 
    path('admin/', admin.site.urls),
    path('test/', views.test, name='test'),
    path('initialize/', views.initialize, name='initialize'),
    path('moveshoulderup/', views.moveShoulderUp, name='moveshoulderup'),
    path('moveshoulderdown/', views.moveShoulderDown, name='moveshoulderDown'),
    path('moveelbowup/', views.moveElbowUp, name='moveshoulderDown'),
    path('moveelbowdown/', views.moveElbowDown, name='moveshoulderDown'),
    path('movewristup/', views.moveWristUp, name='moveshoulderDown'),
    path('movewristdown/', views.moveWristDown, name='moveshoulderDown'),
    path('videostream/', views.videostream, name='moveshoulderup'),
    path('forward2_left2/', views.forward2_left2, name='moveshoulderup'),
    path('forward2_left1/', views.forward2_left1, name='moveshoulderup'),
    path('forward2_left0/', views.forward2_left0, name='moveshoulderup'),
    path('forward1_left0/', views.forward1_left0, name='moveshoulderup'),
    path('forward2_right1/', views.forward2_right1, name='moveshoulderup'),
    path('forward2_right2/', views.forward2_right2, name='moveshoulderup'),
    path('forward1_left2/', views.forward1_left2, name='moveshoulderup'),
    path('forward1_left1/', views.forward1_left1, name='moveshoulderup'),
    path('forward1_left0/', views.forward1_left0, name='moveshoulderup'),
    path('forward1_right1/', views.forward1_right1, name='moveshoulderup'),
    path('forward1_right2/', views.forward1_right2, name='moveshoulderup'),
    path('forward0_left2/', views.forward0_left2, name='moveshoulderup'),
    path('forward0_left0/', views.forward0_left0, name='moveshoulderup'),
    path('forward0_right1/', views.forward0_right1, name='moveshoulderup'),
    path('forward0_right2/', views.forward0_right2, name='moveshoulderup'),
    path('backward1_left2/', views.backward1_left2, name='moveshoulderup'),
    path('backward1_left1/', views.backward1_left1, name='moveshoulderup'),
    path('backward1_left0/', views.backward1_left0, name='moveshoulderup'),
    path('backward1_right1/', views.backward1_right1, name='moveshoulderup'),
    path('backward1_right2/', views.backward1_right2, name='moveshoulderup'),
    path('backward2_left2/', views.backward2_left2, name='moveshoulderup'),
    path('backward2_left1/', views.backward2_left1, name='moveshoulderup'),
    path('backward2_left0/', views.backward2_left0, name='moveshoulderup'),
    path('backward2_right1/', views.backward2_right1, name='moveshoulderup'),
    path('backward2_right2/', views.backward2_right2, name='moveshoulderup'),

]


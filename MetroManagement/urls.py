"""MetroManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from central.views import manager_view, passenger_view, add_station_view, add_train_view, book_ticket_view, home_view, post_booking_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='HomeView'),
    path('manage/', manager_view, name='ManagerView'),
    path('book/', passenger_view, name='PassengerView'),
    path('book/<int:id>/', book_ticket_view, name='TicketView'),
    path('book/<int:id>/successful', post_booking_view),
    path('manage/addtrain/', add_train_view),
    path('manage/addstation/', add_station_view),
]

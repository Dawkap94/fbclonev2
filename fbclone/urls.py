"""
URL configuration for twarzksiazka project.

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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.create_post, name="mainpage"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_request, name="register"),
    path('messenger/<int:user_id>/', views.messenger, name="messenger"),
    path('messenger/delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('logout/', views.logout_request, name="logout"),
    path('account_management/', views.account_management, name="account"),
    path('friends/', views.friends, name="friends"),
    path('user/<int:user_id>/', views.profile, name='profile'),
    path('add-friend/<int:user_id>/', views.add_friend, name='add_friend'),
    path('remove-friend/<int:user_id>/', views.remove_friend, name='remove_friend'),
    path('friend-requests/', views.friend_requests, name='friend_requests'),
    path('accept-friend-request/<int:friend_request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('decline-friend-request/<int:friend_request_id>/', views.decline_friend_request,
         name='decline_friend_request'),
    path('cancel-friend-request/<int:friend_request_id>/', views.cancel_friend_request, name='cancel_friend_request'),
    path('user/<int:user_id>/friends/', views.user_friends, name='user_friends'),
    path('user/<int:user_id>/timeline/', views.user_timeline, name='user_timeline'),
    path('user/<int:user_id>/about/', views.user_about, name='user_about'),
    path('search_results/', views.search_results, name='search_results'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

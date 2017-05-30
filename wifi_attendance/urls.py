"""wifi_attendance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from .views import HomeView, QRView
from users.views import LoginView, AuthorizationCheckView, AuthorizeView, JoinView, LogoutView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name="index"),
    url(r'^qrcode$', QRView.as_view(), name="qrcode"),
    url(r'^login$', LoginView.as_view(), name="login"),
    url(r'^authorize$', AuthorizeView.as_view(), name="authorize"),
    url(r'^check-auth$', AuthorizationCheckView.as_view(), name="checkAuthorization"),
    url(r'^join$', JoinView.as_view(), name="join"),
    url(r'^logout$', LogoutView.as_view(), name="logout"),
    url(r'^admin/', admin.site.urls),
]

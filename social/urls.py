from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', LaUne.as_view(), name='home'),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('profile/edit/', EditProfileView.as_view(), name="edit_profile"),
    path('register/', RegisterView.as_view(), name="register"),
    path('search/', SearchView.as_view(), name="search"),
    path('<nick>/', ProfilePage, name="profile"),

] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS) +\
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

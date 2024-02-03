from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from apps.authentication.login import views as loginviewsets


urlpatterns = [
    path('user/login', loginviewsets.LoginView.as_view(), name='login'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
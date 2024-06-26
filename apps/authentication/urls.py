from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from apps.authentication.login import views as loginviewsets
from apps.authentication.modules import views as modulesviews


urlpatterns = [
    path('user/login/', loginviewsets.UserLogin.as_view(), name='login'),
    path('user/logout/', loginviewsets.UserLogout.as_view(), name='login'),

    path('teste/', loginviewsets.Teste.as_view(), name='teste'),

    path('login/', loginviewsets.LoginView.as_view(), name='teste'),
    path('login_group/', loginviewsets.LoginGroupView.as_view(), name='teste'),
    
    path('modules/update/', modulesviews.UpdateSystemModules.as_view(), name='upd_modules'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
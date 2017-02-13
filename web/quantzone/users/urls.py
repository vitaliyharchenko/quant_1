from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^logout$', views.logout_view, name='logout_view'),
    url(r'^login$', views.login_view, name='login_view'),
    url(r'^reg$', views.reg_view, name='reg_view'),
    url(r'^confirm/(?P<activation_key>.*.{5,100})$', views.reg_confirm, name='confirm'),

    url(r'^user/(?P<user_id>\d+)$', views.user_view, name='user_view'),
    url(r'^user/update$', views.user_update_view, name="user_update_view"),
    url(r'^user/changepass$', views.user_changepass_view, name="user_changepass_view"),
    url(r'^user/resetpass$', views.resetpass_view, name="resetpass_view"),
    url(r'^unsetvkid$', views.unsetvkid, name="unsetvkid"),
]

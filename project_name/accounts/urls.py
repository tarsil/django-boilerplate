from django.conf.urls import url

import accounts.views

accounts_urlpatterns = [
    url(r'^user/create/$', accounts.views.RegisterProfileView.as_view(), name='add-user'),
]

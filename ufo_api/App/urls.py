from App.views import Predict
from django.conf.urls import url

app_name = 'App'

urlpatterns = [
    url(r'^predict/$', Predict.as_view(), name="predict"),
]
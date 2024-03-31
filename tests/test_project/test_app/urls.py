from django.urls import path

from test_app.views import TestView

urlpatterns = [
    path('', TestView.as_view(), name='test_view'),
]

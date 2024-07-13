from django.urls import path

from test_app.views import TestView

urlpatterns = [
    path('api/', TestView.as_view(), name='test_view'),
    path('api/<int:pk>/', TestView.as_view(), name='test_view'),
]

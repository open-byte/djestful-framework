from django.urls import path
from djestful.routers import Router
from test_app.views import TestView, TestView2


router = Router()
router.include('api', TestView, basename='test_view')
router.include('api', TestView2, basename='test_view2')


urlpatterns = [

   ## path('api/<int:pk>/', TestView.as_view(), name='test_view'),
]

urlpatterns += router.urls
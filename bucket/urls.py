from django.urls import path
from . import views


app_name = 'bucket'

urlpatterns = [
    path('', views.bucket_detail, name='detail'),
    path('add/<int:product_id>/', views.bucket_add, name='bucket_add'),
    path('remove/<int:product_id>/', views.bucket_remove, name='bucket_remove'),
]

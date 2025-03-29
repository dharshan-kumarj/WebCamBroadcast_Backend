from django.contrib import admin
from django.urls import path
from broadcast_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/get-stream-id/', views.get_stream_id, name='get_stream_id'),
    path('broadcast/', views.broadcaster_page, name='broadcaster_page'),
    path('view/<str:stream_id>/', views.viewer_page, name='viewer_page'),
]
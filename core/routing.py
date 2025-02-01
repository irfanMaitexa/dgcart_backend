from django.urls import re_path
from .consumers import CartConsumer

websocket_urlpatterns = [
    re_path(r'ws/cart/(?P<customer_id>\d+)/$', CartConsumer.as_asgi()),
]

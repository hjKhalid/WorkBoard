# # routing.py

# from django.urls import re_path
# from workboards.consumers import TaskConsumer

# websocket_urlpatterns = [
#     re_path(r'ws/tasks/(?P<workboard_id>\d+)/$', TaskConsumer.as_asgi()),  # WebSocket route for tasks
# ]
# #
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws', consumers.SocketConsumer.as_asgi()),
]

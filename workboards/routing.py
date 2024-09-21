# # routing.py

# from django.urls import re_path
# from boards import consumers  # Assuming your consumers are in boards app

# websocket_urlpatterns = [
#     re_path(r'ws/tasks/', consumers.TaskConsumer.as_asgi()),  # Point to your consumer
# ]
# routing.py

from django.urls import re_path
from boards.consumers import TaskConsumer  # Adjust to your app and consumer

websocket_urlpatterns = [
    re_path(r'ws/tasks/', TaskConsumer.as_asgi()),
]

from django.urls import path

from .views import PostNotification, FollowNotification, ThreadNotification, RemoveNotification



urlpatterns = [
    path('<int:notification_pk>/post/<int:post_pk>', PostNotification.as_view(), name='post-notification'),
    path('<int:notification_pk>/profile/<int:profile_pk>', FollowNotification.as_view(), name='follow-notification'),
    path('<int:notification_pk>/thread/<int:object_pk>', ThreadNotification.as_view(), name='thread-notification'),
    path('delete/<int:notification_pk>', RemoveNotification.as_view(), name='notification-delete'),
]
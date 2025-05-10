from django.urls import path

from habit.views import HabitList, HabitOwnList, HabitCreate, HabitUpdate, HabitDetail, HabitDestroy
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('', HabitList.as_view(), name='habit-list'),
    path('<int:pk>/', HabitDetail.as_view(), name='habit-detail'),
    path('create/', HabitCreate.as_view(), name='habit-create'),
    path('<int:pk>/update/', HabitUpdate.as_view(), name='habit-update'),
    path('<int:pk>/delete/', HabitDestroy.as_view(), name='habit-delete'),
    path('own/', HabitOwnList.as_view(), name='habit-own'),
]

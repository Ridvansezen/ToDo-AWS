from django.urls import path
from task import views

urlpatterns = [
    path("", views.ListTaskView.as_view(), name="task_list"),
    path("create/", views.TodoTaskCreateView.as_view(), name="task_create"),
    path("update/<int:id>", views.UpdateTaskView.as_view(), name="task_update"),
    path("delete/<int:id>", views.DeleteTaskView.as_view(), name="task_delete"),
]
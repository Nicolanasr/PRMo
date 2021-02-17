from django.urls import path
from . import views

app_name='dashboard'

urlpatterns = [
    path('', views.index1),
    path('<slug:group>/', views.index, name="index"),
    path('<slug:group_from_url>/task/create', views.createTask, name="addTask"),
    path('task/<int:task>', views.task, name="task"),
    path('task/<int:task>/edit', views.editTask, name="editTask"),
    path('task/<int:task>/delete', views.deleteTask, name="deleteTask"),
    path('task/<int:task>/done', views.markTaskDone, name="TaskDone"),
    path('<slug:group>/tasks_review', views.TaskReview, name="TaskReview"),
    path('task/<int:task>/add_comment', views.addComment, name="addComment"),
    path('task/<int:task>/delete_comment/<int:comment_id>', views.deleteComment, name="deleteComment"),


    # path('<slug:group>/test', views.test, name="testtaks"),

]

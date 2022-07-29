from django.urls import path
from . import views


urlpatterns = [
    path('create', views.answer_new),
    path('<int:id>/edit', views.answer_edit),
    path('', views.answer_list),
    path('<int:id>', views.answer_detail),
    path('<int:id>/delete', views.answer_delete),
    path('ticket/<int:id>', views.ticket_answers)
]

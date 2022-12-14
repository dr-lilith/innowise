from django.urls import path
from . import views


urlpatterns = [
    path('create', views.ticket_new),
    path('<int:id>/edit', views.ticket_edit),
    path('pages/<int:page_num>/size/<int:page_size>', views.paging_tickets),
    path('list', views.ticket_list),
    path('unresolved-list', views.ticket_unresolved_list),
    path('resolved-list', views.ticket_resolved_list),
    path('frozen-list', views.ticket_frozen_list),
    path('my-tickets', views.my_tickets),
    path('<int:id>', views.ticket_detail),
    path('<int:id>/delete', views.ticket_delete),
    path('<int:id>/upload_ticket_photo', views.upload_ticket_photo),
    path('<int:id>/upload_ticket_photo_from_url', views.upload_ticket_photo_from_url),
]


from django.urls import path
from . import views

app_name = 'events'
urlpatterns = [
    # events_list views
    path('', views.events_list, name='events_list'),
    path('search', views.search_result, name='search_result'),
    path('<int:event_id>', views.event_detail, name='event_detail'),
    path('add', views.add_event, name='add_event'),
    path('feed', views.feed_page, name='feed_page'),
    path('<int:event_id>/edit', views.edit_event, name='edit_event'),
    path('event/interation', views.event_button_interaction, name='event_interaction'),
    path('event/register', views.event_register_interaction, name='event_register'),
    path('sort/<str:option>', views.sort_list, name='sort_events'),
    path('delete', views.delete_event, name='delete_event'),
]

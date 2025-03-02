from django.urls import path
from events.views import event_home, event_dashboard, event_detail, create_events,search_events, update_events, delete_event

urlpatterns = [

    path('event-home/', event_home, name = "event-home"),
    path('event-dashboard/', event_dashboard, name ="event-dashboard"),
    path('create-event/', create_events, name="create-event"),
    path('event-detail/<int:pk>/', event_detail, name ="event-detail"),
    path('search-events/', search_events, name="search-events"),
    path('update-events/<int:id>/', update_events, name="update-events" ),
    path('delete-event/<int:id>/', delete_event, name="delete-event" ),

   
]
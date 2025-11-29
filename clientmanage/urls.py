from django.urls import path
from . import views

app_name = 'clientmanage'

urlpatterns = [
    path('', views.ClientListView.as_view(), name='client_list'),  # List view URL
    path('client/update/<int:pk>/', views.ClientUpdateView.as_view(), name='client_update'),  # Update view URL
    path('create/', views.ClientCreateView.as_view(), name='client_create'), 

    path('upload/', views.upload_csv, name='upload_csv'),

    path('confirm_email_send/<int:pk>/', views.confirm_email_send, name='confirm-email-send'),
    path('email_send/<int:pk>/<int:pg>', views.email_send, name='email-send'),
    path('email_send_e/<int:pk>/', views.email_send_e, name='email-send-e'),

]

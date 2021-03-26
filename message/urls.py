from django.urls import path
from . import views

app_name = 'Message'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('write-new-message/', views.write_new_message, name='write-new-message'),
    path('message-detail/<int:msg_id>', views.message_detail, name='message-detail'),
    path('delete-message/<int:msg_id>', views.delete_message, name='delete-message'),
    path('send-message/<int:user_id>', views.send_message, name='send-message'),
    path('message-reply/<int:msg_id>/<int:user_id>', views.message_reply, name='message-reply'),
    path('all-sent-msgs/', views.all_sent_msgs, name='all-sent-msgs'),
    path('view-sent-msg-detail/<int:msg_id>', views.view_sent_message_detail, name='view-sent-msg-detail'),
    path('trash-msg/<int:msg_id>', views.trash_message, name='trash-msg'),
    path('message-draft/', views.message_draft, name='message-draft'),
    path('send-draft-message/<int:msg_id>', views.send_draft_message, name='send-draft-message'),
    path('trash_msgs/', views.view_trash_msgs, name='trash_msgs'),
    path('delete-trash-msg/<int:msg_id>', views.delete_trash_msg, name='delete-trash-msg'),
]
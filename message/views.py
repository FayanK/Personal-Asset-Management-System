from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, reverse
from .models import *
from accounts.models import CustomUser
from .forms import WriteNewMessage, DraftMessageSendForm, SendMessageForm, ReplyMessageForm


@login_required
def write_new_message(request):
    url = request.META.get('HTTP_REFERER')
    form = WriteNewMessage()
    if request.method == 'POST':
        form = WriteNewMessage(request.POST)
        receiver = request.POST.get('receiver')
        if form.is_valid():
            instance = form.save(commit=False)
            instance.sender = request.user

            if instance.msg_status == 'Draft':
                instance.receiver = None
                instance.save()
                messages.success(request, 'Message saved to draft !')
                return HttpResponseRedirect(url)
            if receiver:
                instance.save()
                messages.success(request, f'Message sent to {instance.receiver}')
                return HttpResponseRedirect(url)
            else:
                messages.warning(request, 'Please select the receiver ')
                return HttpResponseRedirect(url)
    context = {'form': form}
    return render(request, 'message/write_new_message.html', context)


@login_required
def send_message(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
    except Exception as e:
        messages.warning(request, 'Query does not exists !!')
        return HttpResponseRedirect(reverse('Message:inbox'))
    form = SendMessageForm()
    if request.method == 'POST':
        form = SendMessageForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.receiver_id = user.pk
            instance.sender = request.user
            instance.save()
            inbox_msg = InboxMessage(sender=request.user, receiver_id=user.pk, message=instance.message)
            inbox_msg.save()
            messages.success(request, f'Message sent to {instance.receiver} !')
            return HttpResponseRedirect(reverse('Message:inbox'))
    context = {'form': form, 'user': user}
    return render(request, 'message/send_message.html', context)


@login_required
def inbox(request):
    user = request.user
    msgs = InboxMessage.objects.filter(receiver_id=user, delete_status=True).order_by('-sent_at')
    total_draft_msgs = NewMessage.objects.filter(sender=user, msg_status='Draft', delete_status=True).count()
    context = {'msgs': msgs, 'total_draft_msgs': total_draft_msgs}

    return render(request, 'message/inbox.html', context)


@login_required
def message_detail(request, msg_id):
    form = ReplyMessageForm()
    try:
        msg = InboxMessage.objects.get(pk=msg_id)
        msg.new_msg_active = False
        msg.save()
    except Exception as e:
        messages.warning(request, 'Query does not exists !')
        return HttpResponseRedirect(reverse('Message:inbox'))

    context = {'msg': msg, 'form': form}
    return render(request, 'message/message_detail.html', context)




@login_required
def message_reply(request, msg_id, user_id):
    try:
        receiver = CustomUser.objects.get(pk=user_id)
    except Exception as e:
        messages.warning(request, 'Query does not exists !!')
        return HttpResponseRedirect(reverse('Message:inbox'))
    try:
        msg = InboxMessage.objects.get(pk=msg_id)
    except Exception as e:
        messages.warning(request, 'Query does not exists !')
        return HttpResponseRedirect(reverse('Message:inbox'))
    form = ReplyMessageForm()
    if request.method == 'POST':
        form = ReplyMessageForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.msg_id = msg.pk
            instance.receiver = receiver
            instance.sender = request.user
            instance.save()
            inbox_msg = InboxMessage(sender=request.user, receiver_id=receiver.pk, message=instance.message)
            inbox_msg.save()

            messages.success(request, f'Replied to {instance.receiver} ')
            return HttpResponseRedirect(reverse('Message:inbox'))
    context = {'form': form}
    return render(request, 'message/message_reply.html', context)





@login_required
def message_draft(request):
    user = request.user
    draft_msgs = NewMessage.objects.filter(sender_id=user.pk, msg_status='Draft', delete_status=True, new_msg_active=True)
    context = {'draft_msgs': draft_msgs}
    return render(request, 'message/message_draft.html', context)


@login_required
def send_draft_message(request, msg_id):
    try:
        msg = NewMessage.objects.get(pk=msg_id)
    except Exception as e:
        messages.warning(request, 'Message query does not exists !')
        return HttpResponseRedirect(reverse('Message:message-draft'))
    form = DraftMessageSendForm(instance=msg)
    if request.method == 'POST':
        form = DraftMessageSendForm(request.POST, instance=msg)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.msg_status = 'Send'
            instance.save()
            messages.success(request, f'Message sent to {instance.receiver} !')
            return HttpResponseRedirect(reverse('Message:message-draft'))
    context = {'form': form}
    return render(request, 'message/send_draft_message.html', context)




@login_required
def delete_message(request, msg_id):
    try:
        msg = InboxMessage.objects.get(pk=msg_id, receiver_id=request.user)
    except Exception as e:
        messages.warning(request, 'Message query does not exists !')
        return HttpResponseRedirect(reverse('Message:inbox'))
    msg.delete()
    messages.warning(request, 'Message deleted successfully !')
    return HttpResponseRedirect(reverse('Message:inbox'))


@login_required
def all_sent_msgs(request):
    msgs = NewMessage.objects.filter(sender=request.user, msg_status='Send', delete_status=True)
    context = {'msgs': msgs}
    return render(request, 'message/all_sent_msgs.html', context)


@login_required
def view_sent_message_detail(request, msg_id):
    try:
        msg = NewMessage.objects.get(pk=msg_id, sender=request.user)
    except Exception as e:
        return HttpResponseRedirect(reverse('Message:inbox'))

    context = {'msg': msg}
    return render(request, 'message/view_sent_message_detail.html', context)




@login_required
def trash_message(request, msg_id):
    url = request.META.get('HTTP_REFERER')
    try:
        msg = NewMessage.objects.get(pk=msg_id, sender=request.user)
    except Exception as e:
        return HttpResponseRedirect(reverse('Message:inbox'))
    msg.delete_status = False
    msg.save()
    messages.warning(request, 'Message deleted !')
    return HttpResponseRedirect(url)



@login_required
def view_trash_msgs(request):
    msgs = NewMessage.objects.filter(sender_id=request.user, delete_status=False)
    context = {'msgs': msgs}
    return render(request, 'message/view_trash_msgs.html', context)


@login_required
def delete_trash_msg(request, msg_id):
    url = request.META.get('HTTP_REFERER')
    try:
        msg = NewMessage.objects.get(pk=msg_id, sender_id=request.user, delete_status=False)
    except Exception as e:
        messages.warning(request, 'Query does not exists !')
        return HttpResponseRedirect(url)
    msg.delete()
    messages.warning(request, 'Message deleted from database !')
    return HttpResponseRedirect(url)
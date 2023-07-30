from .models import Message  # Replace 'your_app' with the name of your Django app

def unread_message_count(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        messageRequests = profile.messages.all()
        unread = messageRequests.filter(is_read=False).count() 
        return {'unread_message_count': unread}
    else:
        return {'unread_message_count': None}
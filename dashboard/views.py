# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from dashboard.models import Message, ChatUser
from serializers import MessageSerializer, ChatUserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from dashboard.utils import getFirstLastName, getUserId, getuser
from django.db.models import Q

class Home(View):
    template_name = 'index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return render(request, self.template_name)


# view for getting the user friends list
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def getFriendsList(request):
    print("getting chat users...........")
    myid = getUserId(request)
    chatusers = ChatUser.objects.all().exclude(id=myid)
    try:
        serializer = ChatUserSerializer(chatusers, many=True)
    except Exception as e:
        print("Got exception while getting chat user list : %s" % e)
    return Response(serializer.data)


# view for getting the messages for the User and
# Friend name given
@api_view(['GET', 'POST'])
@renderer_classes((JSONRenderer,))
def getMessages(request, friend_name):
    NotExist = {'error': 'friend does not exist'}
    m_success = {'success': 'message sent successfully.....'}
    messagesData = []
    messUsersDetails = {}

    first, last = getFirstLastName(friend_name)
    myId = getUserId(request)
    messUsersDetails['myId'] = myId
    messUsersDetails['fname'] = friend_name
    messUsersDetails['me'] = getuser(request)
    try:
        friend = ChatUser.objects.get(first_name=first, last_name=last)
        fid = friend.getUserId()
        messUsersDetails['fid'] = fid
    except Exception as e:
        print(e)
        return Response(NotExist)

    if request.method == 'GET':
        try:
            messagesData.append(messUsersDetails)
            my_messages = Message.objects.filter(Q(chatuser_id=myId) & Q(frienduser_id=fid) | Q(chatuser_id=fid) & Q(frienduser_id=myId))
        except Exception as e:
            print(e)
            return Response(NotExist)

        try:
            serializer = MessageSerializer(my_messages, many=True)
            data = serializer.data
            messagesData.append(data)
        except Exception as e:
            print("Got exception while getting json: %s" % e)

        return Response(messagesData)

    if request.method == 'POST':
        print("saving messages..........")
        message = Message()
        message.chatuser_id = messUsersDetails['myId']
        message.frienduser_id = messUsersDetails['fid']
        message.message = request.POST.get('message')
        message.save()
        return Response(m_success)
##########################################################
##                                                      ##
##      Serializer class for for messages               ##
##                                                      ##
##########################################################

from rest_framework import serializers
from models import Message, ChatUser

class ChatUserSerializer(serializers.ModelSerializer):
    """
    Chatuser serializer for user list
    """
    class Meta:
        model = ChatUser
        fields = ('id', 'first_name', 'last_name')


class MessageSerializer(serializers.ModelSerializer):
    """
    Message serializer for displaying user `s messages
    """
    chatuser_id = serializers.PrimaryKeyRelatedField(source='chatuser.id', read_only=True)
    fuser_id = serializers.PrimaryKeyRelatedField(source='frienduser.id', read_only=True)

    class Meta:
        model = Message
        fields = ('message', 'messdate', 'chatuser_id', 'fuser_id')
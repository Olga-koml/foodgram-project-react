
from djoser.serializers import UserSerializer, UserCreateSerializer
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from .models import User
from .models import Subscription


class SubscribedFlag(serializers.Serializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        # return (user.is_authenticated
        #         and Subscription.objects.filter(fanatic=user, idol=obj).exists())
        return (user.is_authenticated and 
                user.fanatic.filter(idol=obj).exists())
    

class CustomCreateUserSerializer(UserCreateSerializer, SubscribedFlag):
 
    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 
            'last_name', 'password', 'is_subscribed'
        )
        
        extra_kwargs = {'email': {'required': True},
                        'first_name': {'required': True},
                        'last_name': {'required': True}
        }
        
    # def get_is_subscribed(self, obj):
    #     user = self.context.get('request').user
    #     # return (user.is_authenticated
    #     #         and Subscription.objects.filter(fanatic=user, idol=obj).exists())
    #     return (user.is_authenticated and 
    #             user.fanatic.filter(idol=obj).exists())
       
  
        # # fields = tuple(User.REQUIRED_FIELDS) + (
        #     'id', 'username', 'first_name', 'last_name', 'password'
        # )
    
    

   # password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    # username = serializers.CharField(#unique=True, 
    #     max_length=150, 
    #     #validators=[UnicodeUsernameValidator(),]
    # )
    # first_name = serializers.CharField(max_length=150) #style={"input_type": "first_name"},
    # last_name = serializers.CharField(max_length=150)
    #required=True, 
    # class Meta:
    #     model = User
    #     fields = ('email', 'username', 'first_name', 'last_name', 'password') 
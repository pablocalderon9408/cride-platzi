"""Users serializers"""
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.models import UserManager
from django.core.validators import RegexValidator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings



from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.utils import field_mapping
from rest_framework.validators import UniqueValidator

from cride.users.models import User, Profile
from cride.users.serializers.profiles import ProfileModelSerializer


from datetime import timedelta

import jwt

class UserModelSerializer(serializers.ModelSerializer):

    profile = ProfileModelSerializer(read_only=True)   
    class Meta:
        
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile'
        )

class UserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        
        user = authenticate(
            username=data['email'], 
            password = data['password']
            )
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet :(')

        self.context['user'] = user
        return data

    def create(self, data):

        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key

class UserSignUpSerializer(serializers.Serializer):
    """User signup serializer
    
    Handle sign up data validation and user/profile creation"""

    email = serializers.EmailField(
        max_length=140,
        validators = [
            UniqueValidator(queryset = User.objects.all())
        ])

    username = serializers.CharField(
        max_length=20,
        min_length=4,
        validators = [
            UniqueValidator(queryset = User.objects.all())
        ])
    
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='Phone number must be entered in the format: +999999999. Up to 15 digits allowed.'
    )
    phone_number = serializers.CharField(validators=[phone_regex])

    password = serializers.CharField(min_length=8,max_length = 64)
    password_confirmation = serializers.CharField(min_length=8,max_length = 64)

    first_name = serializers.CharField(min_length=2,max_length = 30)
    last_name = serializers.CharField(min_length=2,max_length = 30)
    

    def validate(self,data):
        """Validates specific fields.        
        data argument comes from serializer (data=request.data) """
        passwd = data['password']
        passwd_confirmation = data['password_confirmation']

        if passwd != passwd_confirmation:
            raise serializers.ValidationError('Passwords dont match')

        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Create a new user and its profile"""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_verified = False, is_client = True)
        Profile.objects.create(user=user)
        self.send_confirmation_email(user)
        return user

    def send_confirmation_email(self,user):
        """Send account verification link to given user"""
        verification_token = self.gen_verification_token(user)
        
        subject = 'Welcome @{}! Verify your account!'.format(user.username)
        from_email = 'Comparte Ride <noreply@comparteride.com>'
        content = render_to_string(
            'emails/users/account_verification.html',
            {'token':verification_token,'user': user}
            )

        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()

    def gen_verification_token(self,user):
        """Generate the verification token for the user"""
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user':user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation',
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token.decode()


class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer"""

    token = serializers.CharField()

    def validate_token(self, data):        

        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithm = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired')

        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')

        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')

        """The context is always there. If nothing is sent, it is an empty dictionary.
        You can always add to it more information"""
        self.context['payload'] = payload

        return data

    def save(self):
        payload = self.context['payload']
        user = User.objects.get(username = payload['user'])
        user.is_verified = True
        # import ipdb; ipdb.set_trace()
        user.save()








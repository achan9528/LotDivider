from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model, authenticate
from allauth.account.adapter import get_adapter
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from LotDividerAPI import models as apiModels
from rest_auth.serializers import UserDetailsSerializer

# get_user_model() must be used instead of regular
# User model because the custom User model in models.py
# is being used instead of default Django one. This is
# shown in AUTH_USER_MODEL in settings.py
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'alias',
        ]

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:

        model = User
        # these fields are a part of models.User (custom User)
        # model
        fields = [
            'name',
            'alias',
            'email',
            'password',
        ]

    # defining validation function for name
    def validate_name(self, value):
        # check if the name is less than 3 characters
        if len(value) < 3:
            raise serializers.ValidationError(
                "Name must be at least 3 characters!"
            )
        return value
    
    # defining custom validation function on object level. This is
    # to check for the password and password confirmation being the
    # same value
    def validate(self, data):
        # check if the password matches the password confirmation
        if data['password'] != self.initial_data['passwordConfirm']:
            raise serializers.ValidationError(
                "Passwords must match!"
            )
        return data

    # overriding ModelSerializer function
    def get_cleaned_data(self):
        # validated_data represents a dictionary of the data
        # which has been deemed valid by the serializer. The 
        # get function retrieves the value at the requested key, 
        # returning the second argument if the key is not found in
        # the validated_data dictionary
        return {
            'username': self.validated_data.get('username', ''),
            'password': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'alias': self.validated_data.get('alias', '')
        }

    # per django-rest-auth, save function which uses request as 
    # second parameter must be provided. It must also return user
    # object upon completion. Because this is a registration
    # serializer, and because the view only provides the data
    # instead of additional instances to check for already
    # existing objects, the save function will simply create
    # a new record in the database
    def save(self, request):
        user = User.objects.create(
            name=self.validated_data.get('name'),
            alias=self.validated_data.get('alias'),
            email=self.validated_data.get('email'),
            password=make_password(self.validated_data.get('password')),
        )
        return user

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'password'
        ]
    
    # this is taken from the authAll documentation. I only
    # wanted to change the fields

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_email(self, email, password):
        user = None

        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username(self, username, password):
        user = None

        if username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username_email(self, username, email, password):
        user = None

        if email and password:
            user = self.authenticate(email=email, password=password)
        elif username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include either "username" or "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        user = None

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            # Authentication through email
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                user = self._validate_email(email, password)

            # Authentication through username
            elif app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
                user = self._validate_username(username, password)

            # Authentication through either username or email
            else:
                user = self._validate_username_email(username, email, password)

        else:
            # Authentication without using allauth
            if email:
                try:
                    username = UserModel.objects.get(email__iexact=email).get_username()
                except UserModel.DoesNotExist:
                    pass

            if username:
                user = self._validate_username_email(username, '', password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError(_('E-mail is not verified.'))

        attrs['user'] = user
        return attrs

class CreateProjectSerializer(serializers.ModelSerializer):
    owners = UserSerializer(many=True)
    class Meta:
        model = apiModels.Project
        fields = [
            'name',
            'owners',
        ]

    def create(self, validated_data):
        owners = validated_data.pop('owners')
        project = apiModels.Project.objects.create(**validated_data)
        for owner in owners:
            project.owners.add(
                get_user_model().objects.get(
                    email=owner['email']))
        project.save()
        return project

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = apiModels.ProductType
        fields = [
            'name',
            'fractionalLotsAllowed'
        ]

    # def create(self, validated_data):

class SecuritySerializer(serializers.ModelSerializer):
    productType = serializers.PrimaryKeyRelatedField(
        queryset=apiModels.ProductType.objects.all(),
        )
    class Meta:
        model = apiModels.Security
        fields = [
            'name',
            'ticker',
            'cusip',
            'productType',
        ]

    def create(self, validated_data):
        security = apiModels.Security.objects.create(**validated_data)
        return security

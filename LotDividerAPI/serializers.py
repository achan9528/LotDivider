from rest_framework import serializers
from LotDividerAPI.models import User
import bcrypt

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'name',
            'alias',
            'email',
            'password',
        ]

    def create(self, validated_data):
        password = validated_data['password']
        pwHash = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()
            ).decode()
        user = User.objects.create(
            name=validated_data['name'],
            alias=validated_data['alias'],
            email=validated_data['email'],
            password=pwHash
        )
        return user

    def validate_name(self, value):
        # check if the name is less than 3 characters
        if len(value) < 3:
            raise serializers.ValidationError(
                "Name must be at least 3 characters!"
            )
        return value
    
    def validate(self, data):
        # check if the password matches the password confirmation
        if data['password'] != self.initial_data['passwordConfirm']:
            raise serializers.ValidationError(
                "Passwords must match!"
            )
        return data
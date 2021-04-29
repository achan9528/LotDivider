from rest_framework import serializers
from LotDividerAPI.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
        'name',
        'alias',
        'email',
        'password',
        'number',
        'createdAt',
        'updatedAt'
        ]


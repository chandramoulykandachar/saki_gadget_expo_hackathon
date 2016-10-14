from pyparsing import empty

from rest_framework import serializers
from saki.models import User, App


class UserSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    user = serializers.CharField(required=True, allow_blank=True, max_length=100)
    api_key = serializers.CharField(required=True, max_length=100)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """

        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.user = validated_data.get('user', instance.user)
        instance.api_key = validated_data.get('api_key', instance.api_key)
        instance.save()
        return instance


class AppSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    app_name = serializers.CharField(required=True, allow_blank=True, max_length=100)

    def __init__(self, user, instance=None, data=empty, **kwargs):
        super(AppSerializer, self).__init__(instance=None, data=data, **kwargs)
        self.user = user

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        validated_data['user'] = self.user
        return App.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.user = validated_data.get('user', instance.user)
        instance.api_key = validated_data.get('api_key', instance.api_key)
        instance.save()
        return instance


class PredictionSerializer(serializers.Serializer):
    app_name = serializers.CharField(required=True, allow_blank=False, max_length=100)
    current_activity = serializers.CharField(required=True, max_length=100)
    message = serializers.CharField(required=True)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return validated_data

    def update(self, instance, validated_data):
        pass


class TrainSerializer(serializers.Serializer):
    app_name = serializers.CharField(required=True, allow_blank=False, max_length=100)

    def create(self, validated_data, action_list):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return validated_data

    def update(self, instance, validated_data):
        pass
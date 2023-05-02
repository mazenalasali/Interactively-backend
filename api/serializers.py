from rest_framework import serializers
from .models import CustomUser, Question, UserHistory, Activity, PreExam, PostExam, Contact
from django.contrib.auth import authenticate

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'firstName', 'lastName', 'group', 'password', 'confirmPassword']
        extra_kwargs = {
            'password': {'write_only': True},
            'confirmPassword': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        confirmPassword = validated_data.pop('confirmPassword')
        if password != confirmPassword:
            raise serializers.ValidationError("Passwords don't match.")
        user = CustomUser.objects.create_user(password=password, confirmPassword=confirmPassword, **validated_data)
        return user

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                msg = 'Unable to authenticate with provided credentials'
                raise serializers.ValidationError(msg, code='authentication')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'subject', 'message']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question', 'answers', 'correctAnswer')

class PreExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreExam
        fields = ['id', 'user', 'question', 'answer']

class PostExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostExam
        fields = ['id', 'user', 'question', 'answer']

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'user', 'activity_name', 'file']

class UserHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserHistory
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'
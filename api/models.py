from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, firstName, lastName, password, confirmPassword, group, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        if not firstName:
            raise ValueError('The FirstName field must be set')
        if not lastName:
            raise ValueError('The LastName field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        if not confirmPassword:
            raise ValueError('The confirmPassword field must be set')
        if not group:
            raise ValueError('The Group field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, firstName=firstName, lastName=lastName, group=group, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, firstName, lastName, password, confirmPassword, group, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, firstName, lastName, password, confirmPassword, group, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_GROUP_CHOICES = (
        ('group1', 'Group 1'),
        ('group2', 'Group 2'),
        ('group3', 'Group 3'),
        ('group4', 'Group 4')
    )

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=30, unique=True)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    confirmPassword = models.CharField(max_length=30)
    group = models.CharField(max_length=20, choices=USER_GROUP_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'firstName', 'lastName', 'password', 'confirmPassword', 'group']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Question(models.Model):
    question = models.CharField(max_length=200)
    answers = models.JSONField()
    correctAnswer = models.CharField(max_length=200)

    def __str__(self):
        return self.question

class PreExam(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

class PostExam(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

class UserHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    is_pre_exam_taken = models.BooleanField(default=False,  null=True, blank=True)
    pre_exam_taken_spent_time = models.CharField(default='0', null=True, blank=True, max_length=1)
    is_post_exam_taken = models.BooleanField(default=False,  null=True, blank=True)
    post_exam_taken_spent_time = models.CharField(default='0', null=True, blank=True, max_length=1)
    is_chat_bot_used = models.BooleanField(default=False,  null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Activity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    activity_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='activity_files/')

class Contact(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.CharField(max_length=255)




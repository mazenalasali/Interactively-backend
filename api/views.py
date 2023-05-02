from django.contrib.auth import  login, logout
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PreExam, PostExam, CustomUser, Question, UserHistory, Activity, Contact
from .serializers import CustomUserSerializer, AuthTokenSerializer, QuestionSerializer, UserHistorySerializer, \
    PreExamSerializer, PostExamSerializer, ActivitySerializer, ContactSerializer


class RegisterView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = CustomUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key,
                             'user_id': user.pk,
                             'user_email': user.email,
                             'user_firstName': user.firstName,
                             'user_group': user.group
                             })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,
                         'user_id': user.pk,
                         'user_email': user.email,
                         'user_firstName': user.firstName,
                         'user_group': user.group
                         })

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully.'})

class ContactView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessagesListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        messages = Contact.objects.all()
        serializer = ContactSerializer(messages, many=True)
        return Response(serializer.data)


class AddQuestionsAPIView(APIView):
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateQuestionView(APIView):
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)

    def patch(self, request, id):
        try:
            question = Question.objects.get(id=id)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetQuestionsAPIView(APIView):
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)

    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

class PreExamAPIView(APIView):
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)

    def post(self, request):
        user_email = request.data['userEmail']
        data = request.data['data']
        user = CustomUser.objects.get(email=user_email)

        for answer_data in data:
            question = answer_data['questionText']
            selected_answer = answer_data['selectedAnswer']
            answer = PreExam(user=user, question=question, answer=selected_answer)
            answer.save()

        return Response({'message': 'PreExam answers submitted successfully'})

class PreExamList(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        preexams = PreExam.objects.filter(user=user)
        serializer = PreExamSerializer(preexams, many=True)
        return Response(serializer.data)

class PostExamAPIView(APIView):
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)

    def post(self, request):
        user_email = request.data['userEmail']
        data = request.data['data']
        user = CustomUser.objects.get(email=user_email)

        for answer_data in data:
            question = answer_data['questionText']
            selected_answer = answer_data['selectedAnswer']
            answer = PostExam(user=user, question=question, answer=selected_answer)
            answer.save()

        return Response({'message': 'PostExam answers submitted successfully'})

class PostExamList(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        postexams = PostExam.objects.filter(user=user)
        serializer = PostExamSerializer(postexams, many=True)
        return Response(serializer.data)

class ActivityCreateView(APIView):
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)

    def post(self, request):
        user_email = request.data['user_email']
        activity_name=request.data['activity_name']
        file = request.data['activity_name']
        user = CustomUser.objects.get(email=user_email)
        activity = Activity(activity_name=activity_name,
                                user=user,
                                file=file)
        try:
            activity.save()
            return Response({'message': 'activity submitted successfully'}, status=status.HTTP_200_OK)
        except:

            return Response({'message': 'Error in submitting the activity'}, status=status.HTTP_400_BAD_REQUEST)

class ActivityList(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        activities = Activity.objects.filter(user=user)
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class IsPreExamTakenView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        user_email = request.data['userEmail']
        try:
            user = CustomUser.objects.get(email=user_email)
            try:
                user_history = UserHistory.objects.get(user=user)
                is_pre_exam_taken = user_history.is_pre_exam_taken
                return Response(is_pre_exam_taken, status=status.HTTP_200_OK)
            except UserHistory.DoesNotExist:
                return Response(False, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            is_pre_exam_taken = False
            return Response(is_pre_exam_taken, status=status.HTTP_200_OK)

class UpdatePreExamTakenView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        user_email = request.data['userEmail']
        is_pre_exam_taken = request.data['isPreExamTaken']

        is_pre_exam_taken = True if is_pre_exam_taken == 'true' or 'True' else False

        if user_email is None:
            return JsonResponse({'error': 'User email is required.'}, status=400)

        if is_pre_exam_taken is None:
            return JsonResponse({'error': 'is_pre_exam_taken value is required.'}, status=400)

        try:
            user = CustomUser.objects.get(email=user_email)

            try:

                user_history, created = UserHistory.objects.get_or_create(user=user)
                user_history.is_pre_exam_taken = is_pre_exam_taken
                user_history.save()
                return JsonResponse({'success': 'User history updated.'}, status=200)
            except UserHistory.DoesNotExist:
                return JsonResponse({'error': 'User history not updated.'}, status=404)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User history not updated'}, status=404)


class IsPostExamTakenView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        user_email = request.data['userEmail']
        try:
            user = CustomUser.objects.get(email=user_email)
            try:
                user_history = UserHistory.objects.get(user=user)
                is_post_exam_taken = user_history.is_post_exam_taken
                return Response(is_post_exam_taken, status=status.HTTP_200_OK)
            except UserHistory.DoesNotExist:
                return Response(False, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            is_post_exam_taken = False
            return Response(is_post_exam_taken, status=status.HTTP_200_OK)

class UpdatePostExamTakenView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        user_email = request.data['userEmail']
        is_post_exam_taken = request.data['isPostExamTaken']
        is_post_exam_taken = True if is_post_exam_taken == 'true' or 'True' else False
        if user_email is None:
            return JsonResponse({'error': 'User email is required.'}, status=400)
        if is_post_exam_taken is None:
            return JsonResponse({'error': 'is_post_exam_taken value is required.'}, status=400)
        try:
            user = CustomUser.objects.get(email=user_email)
            try:
                user_history, created = UserHistory.objects.get_or_create(user=user)
                user_history.is_post_exam_taken = is_post_exam_taken
                user_history.save()
                return JsonResponse({'success': 'User history updated.'}, status=200)
            except UserHistory.DoesNotExist:
                return JsonResponse({'error': 'User history not updated.'}, status=404)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User history not updated'}, status=404)

class IsChatBotUsedView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        user_email = request.data['userEmail']
        try:
            user = CustomUser.objects.get(email=user_email)
            try:
                user_history = UserHistory.objects.get(user=user)
                is_chat_bot_used = user_history.is_chat_bot_used
                return Response(is_chat_bot_used, status=status.HTTP_200_OK)
            except UserHistory.DoesNotExist:
                return Response(False, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            is_chat_bot_used = False
            return Response(is_chat_bot_used, status=status.HTTP_200_OK)

class UpdateChatBotUsedView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        user_email = request.data['userEmail']
        is_chat_bot_used = request.data['isChatBotUsed']
        is_chat_bot_used = True if is_chat_bot_used == 'true' or 'True' else False
        if user_email is None:
            return JsonResponse({'error': 'User email is required.'}, status=400)
        if is_chat_bot_used is None:
            return JsonResponse({'error': 'is_chat_bot_used value is required.'}, status=400)
        try:
            user = CustomUser.objects.get(email=user_email)
            try:
                user_history, created = UserHistory.objects.get_or_create(user=user)
                user_history.is_chat_bot_used = is_chat_bot_used
                user_history.save()
                return JsonResponse({'success': 'User history updated.'}, status=200)
            except UserHistory.DoesNotExist:
                return JsonResponse({'error': 'User history not updated.'}, status=404)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User history not updated'}, status=404)

class UserListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

class UserDetailView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            data = {
                'id': user.id,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'email': user.email,
                'group': user.group
            }
            return JsonResponse(data)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

class UserHistoryView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        user_history = UserHistory.objects.filter(user=user)
        serializer = UserHistorySerializer(user_history, many=True)
        return Response(serializer.data)
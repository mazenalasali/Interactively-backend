from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView, LoginView, LogoutView, PreExamAPIView, PostExamAPIView, GetQuestionsAPIView, \
    AddQuestionsAPIView, UpdateQuestionView, ActivityCreateView, IsPreExamTakenView, UpdatePreExamTakenView, \
    IsPostExamTakenView, UpdatePostExamTakenView, IsChatBotUsedView, UpdateChatBotUsedView, UserListView, \
    UserHistoryView, UserDetailView, PreExamList, PostExamList, ActivityList, ContactView, MessagesListView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('api-token-auth', obtain_auth_token),
    path('contact', ContactView.as_view()),
    path('add-questions', AddQuestionsAPIView.as_view()),
    path('update-question/<int:id>', UpdateQuestionView.as_view()),
    path('get-questions', GetQuestionsAPIView.as_view()),
    path('pre-exam', PreExamAPIView.as_view()),
    path('post-exam', PostExamAPIView.as_view()),
    path('activities', ActivityCreateView.as_view()),
    path('is-pre-exam-taken', IsPreExamTakenView.as_view()),
    path('update-pre-exam-taken', UpdatePreExamTakenView.as_view()),
    path('is-post-exam-taken', IsPostExamTakenView.as_view()),
    path('update-post-exam-taken', UpdatePostExamTakenView.as_view()),
    path('is-chat-bot-used', IsChatBotUsedView.as_view()),
    path('update-chat-bot-used', UpdateChatBotUsedView.as_view()),
    path('users', UserListView.as_view()),
    path('users/<int:user_id>', UserDetailView.as_view()),
    path('users/<int:user_id>/history', UserHistoryView.as_view()),
    path('users/<int:user_id>/history/pre-exam', PreExamList.as_view()),
    path('users/<int:user_id>/history/post-exam', PostExamList.as_view()),
    path('users/<int:user_id>/history/activity', ActivityList.as_view()),
    path('users/history/messages', MessagesListView.as_view()),
]

from django.urls import path

from signup.views import ConfirmationView, SignUpView

urlpatterns = [
    path('', SignUpView.as_view(), name='signup'),
    path('confirm/<uidb64>/<token>', ConfirmationView.as_view(), name='confirm')
]
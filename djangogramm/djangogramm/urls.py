from django.urls import path

from .views import ConfirmationView, SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('confirm/<uidb64>/<token>', ConfirmationView.as_view(), name='confirm')
]
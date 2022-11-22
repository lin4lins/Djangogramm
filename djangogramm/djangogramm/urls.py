from django.urls import path

from .views import PostConfirmationView, SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('confirm/<uidb64>/<token>', PostConfirmationView.as_view(), name='confirm')
]
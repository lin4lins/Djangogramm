from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import (DjangoUnicodeDecodeError, force_bytes, force_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from mysite.settings import EMAIL_HOST_USER

from .forms import SignUpForm
from .models import User
from .utils import confirmation_token

# Create your views here


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            self.__send_confirmation_email(request, user)
            return HttpResponse("Check your email")

        return render(request, 'signup/signup.html', {'form': form})

    @staticmethod
    def __send_confirmation_email(request, user) -> None:
        message = render_to_string("signup/confirmation_email.html",
                                   {'domain': get_current_site(request),
                                    'user_id': urlsafe_base64_encode(force_bytes(user.pk)),
                                    'token': confirmation_token.make_token(user)})
        send_mail(
            subject='Confirm your email to sign in Djangogramm!',
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )


class ConfirmationView(View):
    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not user.is_active and confirmation_token.check_token(user, token):
                user.is_active = True
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return render(request, "signup/confirmed.html")

            return render(request, "signup/confirmed_earlier.html")

        except (DjangoUnicodeDecodeError, User.DoesNotExist, ValueError):
            return render(request, "errors.html", {'error_messages': ["Invalid confirmation link"]})

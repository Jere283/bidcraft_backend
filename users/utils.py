import random

from django.conf import settings
from django.core.mail import EmailMessage

from users.models import User, Otps


def send_generated_otp_to_email(email, request):
    subject = "Verifica tu correo electronico"
    otp = random.randint(1000, 9999)
    current_site = "test"
    user = User.objects.get(email=email)
    email_body=f"Hi {user.first_name} thanks for signing up on {current_site} please verify your email with the \n one time passcode {otp}"
    from_email = settings.EMAIL_HOST

    otp_obj = Otps.objects.create(user=user, code=otp)
    #send the email
    d_email = EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[user.email])
    d_email.send()

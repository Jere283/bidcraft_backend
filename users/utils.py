import random

from django.conf import settings
from django.core.mail import EmailMessage

from users.models import User, OneTimePassword


def generate_otp():
    otp=""
    for i in range(6):
        otp += str(random.randint(1,9))
    return otp

def send_code_to_user(email):
    subject = "Verifica tu correo electronico"
    otp_code = generate_otp()
    print(otp_code)

    user = User.objects.get(email=email)
    current_site = "myAuth.com"
    email_body = f"Hola {user.first_name} gracias por registrate en {current_site} porfavor verifica tu correo electronico" \
                 f"con tu \n codigo unico {otp_code}"
    from_email = settings.DEFAULT_FROM_EMAIL

    OneTimePassword.objects.create(user=user, code=otp_code)

    d_email = EmailMessage(subject=subject,body=email_body,from_email=from_email,to=email)
    d_email.send(fail_silently=True)
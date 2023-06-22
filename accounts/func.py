from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator

def send_custom_email(request:object, email_subject:str, template_path:str, user:object, email:str, order:object=None):
    currentSite = get_current_site(request)
    mail_subject = email_subject
    message = render_to_string(template_path, {
        "user": user,
        "domain": currentSite,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": default_token_generator.make_token(user),
        "order": order
    })

    emailReceiver = email
    send_email= EmailMessage(mail_subject, 
                             message, 
                             to=[emailReceiver])
    send_email.send()
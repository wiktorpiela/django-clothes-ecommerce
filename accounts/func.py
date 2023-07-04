from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator

from io import BytesIO
from orders.models import Order, OrderProduct
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.conf import settings

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

def fetch_resources(uri, rel):
    path = os.path.join(uri.replace(settings.STATIC_URL, ""))
    return path

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None
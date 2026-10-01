import random
from .models import NewUser
from django.conf import settings
import logging
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .models import NewUser


logger = logging.getLogger(__name__)


def envoie_email(subjet:str, receivers:list, template:str, context:dict):
    try:
        message = render_to_string(template, context)
        send_mail(
            subjet,
            message,
            settings.EMAIL_HOST_USER,
            receivers,
            fail_silently=True,
            html_message=message
        )
        return True


    except Exception as e:
        logger.error(e)
    return False


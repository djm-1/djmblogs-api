from django.contrib.auth.models import User
from django.shortcuts import render,HttpResponseRedirect
from django.http import JsonResponse
import googleanalytics as ga
from .models import *
from django.core.serializers import serialize
from django.contrib import messages
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .serializers import SubscriberSerializer
from rest_framework import status
from rest_framework.response import Response


def index(request): 
    newsletters=newsletter.objects.all()
    return render(request,'newsletter_table.html',{'newsletters':newsletters})


from django.core.mail import get_connection, EmailMultiAlternatives

def send_mass_html_mail(datatuple, fail_silently=False, user=None, password=None, 
                        connection=None):
    """
    Given a datatuple of (subject, text_content, html_content, from_email,
    recipient_list), sends each message to each recipient list. Returns the
    number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    """
    connection = connection or get_connection(
        username=user, password=password, fail_silently=fail_silently)
    messages = []
    for subject, text, html, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, text, from_email, recipient)
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    return connection.send_messages(messages)


def send_newsletter(request,id):

    nlt=newsletter.objects.get(id=id)
    subs=subscriber.objects.all()
    subs_list=[]
    for sub in subs:
        subs_list.append(str(sub.email))

    subject = nlt.title
    html_message = render_to_string('newsletter.html', {'content': nlt.content})
    plain_message = strip_tags(html_message)
    from_email = 'dibyajyoti.djmblogs@gmail.com'

    datatuple=[]
    for sub in subs_list:
        message = (subject, plain_message, html_message, from_email, [sub])
        datatuple.append(message)
    tuple(datatuple)
    #print(datatuple)
    send_mass_html_mail(datatuple, fail_silently=False)  
    messages.success(request,'Newsletter delivered')
    newsletter.objects.filter(id=id).update(published=True)  
    return HttpResponseRedirect('/admin/')

def commentdata(request,id):
    comm=comment.objects.filter(post__id=id)
    parent_comm=comm.filter(parent_comment=None)
    return JsonResponse(list(parent_comm.values()),safe=False)



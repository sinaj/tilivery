import re
from email.utils import parseaddr

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from web.models import Customer

from twilio.twiml.messaging_response import MessagingResponse


def homepage_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "")
        postal_code = request.POST.get("postal_code", "")
        request.context['email'] = email
        request.context['postal_code'] = postal_code
        if _validate_email(request, email) and _validate_postal_code(request, postal_code, True):
            Customer.objects.create(
                email=email,
                postal_code=postal_code.replace(" ", "").upper(),
                creation_time=timezone.now()
            )
            return HttpResponseRedirect(reverse("thank_you"))
    return render(request, "homepage.html", request.context)


def _validate_email(request, email):
    _, real_email = parseaddr(email)
    if not email or real_email is "":
        request.context['email_error'] = "Please enter a valid email."
        return False
    return True


def _validate_postal_code(request, postal_code, set_context):
    cleaned_postal_code = postal_code.replace(" ", "").upper()
    postal_code_regex = '[ABCEGHJKLMNPRSTVXY][0-9][ABCEGHJKLMNPRSTVWXYZ][0-9][ABCEGHJKLMNPRSTVWXYZ][0-9]'
    if not re.search(postal_code_regex, cleaned_postal_code):
        if set_context:
            request.context['postal_code_error'] = "Please enter a valid postal code"
        return False
    return True


def thank_you_view(request):
    return render(request, "thank_you.html", request.context)


def privacy_view(request):
    return HttpResponseRedirect("https://www.privacypolicygenerator.info/live.php?token=omWgU7pTEWEqM8Bv7upmaV0JjlXmDkmH")


@csrf_exempt
def sms_received_handler(request):
    resp = MessagingResponse()
    from_number = request.GET.get('From', None)
    sms_body = request.GET.get('Body', None)
    if _validate_postal_code(request, sms_body, False):
        cleaned_postal_code = sms_body.replace(" ", "").upper()
        Customer.objects.create(
            phone=from_number,
            postal_code=cleaned_postal_code,
            creation_time=timezone.now()
        )
        resp.message("Thank you! We have recorded your vote.\n" +
                     "Please share this with your friends, so they can also take advantage.")
        return HttpResponse(resp, content_type="text/xml")
    else:
        resp.message("If you are voting, please send us just your postal code.\n" +
                     "Otherwise, please leaves a message for us")
        return HttpResponse(resp, content_type="text/xml")

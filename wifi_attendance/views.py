#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
import qrcode
from cStringIO import StringIO
import uuid
from users.models import VerificationToken
import datetime


__author__ = "Elvin Zeng"


class HomeView(View):
    """
    home page view
    """

    def get(self, request):
        if request.user.is_authenticated():
            return render(request, "index.html")
        else:
            verification_token = str(uuid.uuid4())
            request.session["verification_token"] = verification_token
            return render(request, "authentication.html", locals())


class QRView(View):
    """
    QR Code View
    """

    def get(self, request):
        host = request.META['HTTP_HOST']
        token = request.session.get("verification_token", str(uuid.uuid4()))

        verification_token = VerificationToken()
        verification_token.token = token
        verification_token.expire_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
        verification_token.save()

        data = "http://" + host + "/authorize?token=" + token
        img = qrcode.make(data)
        buf = StringIO()
        img.save(buf)
        image_stream = buf.getvalue()
        response = HttpResponse(image_stream, content_type="image/png")
        return response

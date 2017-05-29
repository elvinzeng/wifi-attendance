#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
import qrcode
from cStringIO import StringIO


__author__ = "Elvin Zeng"


class HomeView(View):
    """
    home page view
    """

    def get(self, request):
        if request.user.is_authenticated():
            return render(request, "index.html")
        else:
            return render(request, "login.html")


class QRView(View):
    """
    QR Code View
    """

    def get(self, request):
        host = request.META['HTTP_HOST']
        data = "http://" + host + "/login"
        img = qrcode.make(data)
        buf = StringIO()
        img.save(buf)
        image_stream = buf.getvalue()
        response = HttpResponse(image_stream, content_type="image/png")
        return response

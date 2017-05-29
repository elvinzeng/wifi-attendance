#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic import View


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

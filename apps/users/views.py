#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.views.generic import View


__author__ = "Elvin Zeng"


class JoinView(View):
    """
    join view
    """

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        else:
            return render(request, "join.html")

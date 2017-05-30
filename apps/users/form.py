#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms

__author__ = "Elvin Zeng"


class JoinForm(forms.Form):
    """
    手机登记
    """

    first_name = forms.CharField(min_length=1, max_length=15, required=True)
    last_name = forms.CharField(min_length=1, max_length=15, required=True)
    email = forms.EmailField(required=True, label='email')

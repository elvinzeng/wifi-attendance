#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging

from django.contrib.auth.models import Group

from users.models import UserProfile

__author__ = "Elvin Zeng"


logger = logging.getLogger(__name__)
logger.info("Start to initialize the user system")


_hr_group_list = Group.objects.filter(name="hr")
if len(_hr_group_list) > 0:
    logger.info("User group 'hr' already exists.")
else:
    logger.info("User group 'hr' not already exists. creating...")
    _hr_group = Group()
    _hr_group.name = "hr"
    _hr_group.save()

_staff_group_list = Group.objects.filter(name="staff")
if len(_staff_group_list) > 0:
    logger.info("User group 'staff' already exists.")
else:
    logger.info("User group 'staff' not already exists. creating...")
    _staff_group = Group()
    _staff_group.name = "staff"
    _staff_group.save()


def is_hr_account_created():
    """
    :rtype: bool
    :return: hr帐号是否已经存在
    """

    hr_user_list = UserProfile.objects.filter(groups__name='hr')
    if len(hr_user_list) > 0:
        return True
    else:
        return False


def hr_group():
    hr_group_list = Group.objects.filter(name="hr")
    if len(hr_group_list) > 0:
        return hr_group_list[0]
    else:
        raise Exception("User group 'hr' not found.")


def staff_group():
    staff_group_list = Group.objects.filter(name="staff")
    if len(staff_group_list) > 0:
        return staff_group_list[0]
    else:
        raise Exception("User group 'staff' not found.")

logger.info("The user system is initialized")

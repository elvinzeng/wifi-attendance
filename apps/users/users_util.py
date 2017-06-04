#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from mobile_scanner.models import OnlineHistory
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


_staff_history_view_permission_list = Permission.objects.filter(codename='view_staffonlinehistory')
if len(_staff_history_view_permission_list) > 0:
    logger.info("Permission 'view_staffonlinehistory' already exists.")
else:
    logger.info("Permission 'view_staffonlinehistory' not already exists. creating...")
    _permission = Permission()
    _permission.name = "查看员工在线历史"
    _permission.codename = "view_staffonlinehistory"
    _onlinehistory_content_type = ContentType.objects.get(app_label='mobile_scanner', model='OnlineHistory')
    _permission.content_type = _onlinehistory_content_type
    _permission.save()
    hr_group().permissions.add(_permission)


logger.info("The user system is initialized")

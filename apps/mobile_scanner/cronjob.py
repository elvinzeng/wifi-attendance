#!/usr/bin/env python
# -*- coding:utf-8 -*-
from wifi_attendance.settings import WIFI_NET_ADDR
import logging
import os

__author__ = "Elvin Zeng"


def scan_mobile():
    # os.system('cd $(cd $(dirname $0) && pwd -P)')
    logger = logging.getLogger(__name__)
    logger.info("mobile scaner is running...")
    logger.info(WIFI_NET_ADDR)

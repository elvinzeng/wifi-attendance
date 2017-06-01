#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import threading

from mobile_scanner.models import OnlineHistory
from users.models import UserProfile
from wifi_attendance.settings import WIFI_NET_ADDR
import logging
import os
import re

__author__ = "Elvin Zeng"


def scan_mobile():
    # os.system('cd $(cd $(dirname $0) && pwd -P)')
    logger = logging.getLogger(__name__)
    logger.info("mobile scanner is running...")
    logger.info("network pattern: " + WIFI_NET_ADDR)
    batch_list = []
    for i in xrange(253):
        ip = WIFI_NET_ADDR.format(i + 1)
        batch_index = i / 10
        if len(batch_list) <= batch_index:
            batch_list.append([])
        batch_list[batch_index].append(ip)

    threads = []
    for batch in batch_list:
        thread = threading.Thread(target=scan_batch, args=(batch,))
        thread.setDaemon(True)
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()

    logger.info("mobile scan completed.")


def scan_batch(ip_list):
    logger = logging.getLogger(__name__)
    logger.info("scanning a batch: " + str(ip_list))
    for ip in ip_list:
        scan_ip(ip)


def scan_ip(ip):
    logger = logging.getLogger(__name__)
    logger.info("scanning: " + ip)
    ping_cmd = "ping {0} -c 1".format(ip)
    ping_output = os.popen(ping_cmd).readlines()
    match = re.search(r"64\sbytes\sfrom\s{0}:".format(ip.replace(".", "\.")),
                      "".join(ping_output))
    if match:
        #  matched. host is online.
        logger.info("host {0} is online.".format(ip))
        is_arp_ok = False
        arp_cmd = "cat /proc/net/arp | grep -w '" + ip + "' | awk '{print $4}'"
        arp_output = os.popen(arp_cmd).readlines()
        arp_output = "".join(arp_output)
        arp_output_matched_list = re.findall(r"([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})", arp_output)
        if len(arp_output_matched_list) > 0:
            arp_output_matched_tuple = arp_output_matched_list[0]
            if len(arp_output_matched_tuple) > 0:
                mac = arp_output_matched_tuple[0]
                is_arp_ok = True
                record_online_history(ip, mac)
        if not is_arp_ok:
            logger.error("host {0} is online, but failed to get mac address.".format(ip))
    else:
        #  logger.info("host {0} is not online".format(ip))
        pass


def record_online_history(ip, mac):
    logger = logging.getLogger(__name__)
    user_list = UserProfile.objects.filter(username=mac)
    if len(user_list) > 0:
        user = user_list[0]
        online_history = OnlineHistory()
        online_history.mac = mac
        online_history.ip = ip
        online_history.user = user
        online_history.date = datetime.datetime.now()
        online_history.time = datetime.datetime.now()
        online_history.save()
    else:
        #  logger.info("host {0} {1} is online, but not had registered.".format(ip, mac))
        pass



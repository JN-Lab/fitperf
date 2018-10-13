#! /usr/bin/env python3
# coding: utf-8
from datetime import time

class Tools:

    def convert_km_into_meters(self, km):
        """
        Convert kilometers into meters
        """
        return int(km * 1000)

    def convert_seconds_into_time(self, all_seconds):
        days = all_seconds//86400
        hours = (all_seconds - (days * 86400)) // 3600
        minutes = (all_seconds - (days * 86400 + hours * 3600)) // 60
        seconds = all_seconds - (days * 86400 + hours * 3600 + minutes * 60)

        return time(hour=hours, minute=minutes, second=seconds)
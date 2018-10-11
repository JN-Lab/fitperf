#! /usr/bin/env python3
# coding: utf-8

class Tools:

    def convert_seconds_into_time_string(self, all_seconds):
        """
        The objective to this private is to convert seconds into this format:
        HH:MM:SS
        """
        hours = all_seconds // 60 // 60
        minutes = all_seconds // 60
        seconds = all_seconds % 60

        return "{}:{}:{}".format(hours, minutes, seconds)

    def convert_time_into_seconds(self, hours, minutes, seconds):
        """
        The objective is to convert a time splitted in hours, minutes and seconds
        into seconds
        """    
        return hours * 60 * 60 + minutes * 60 + seconds 

    def convert_km_into_meters(self, km):
        """
        Convert kilometers into meters
        """
        return int(km * 1000)
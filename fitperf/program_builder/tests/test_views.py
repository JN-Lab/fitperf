#! /usr/bin/env python3
# coding: utf-8
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..utils.db_interactions import DBMovement


class IndexPageTestCase(TestCase):
    """
    This class tests the index view
    """

    @classmethod
    def setUpTestData(cls):
        username = 'user'
        user = User.objects.create_user(username=username)
        user.set_password('test-view')
        user.save()

    def test_index_when_logged(self):
        self.client.login(username='user', password='test-view')      
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/app/dashboard/')

    def test_index_when_not_logged(self):      
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/authentification/login/')

class HomePageTestCase(TestCase):
    """
    This class tests the homepage view
    """

    @classmethod
    def setUpTestData(cls):
        username = 'user'
        user = User.objects.create_user(username=username)
        user.set_password('test-view')
        user.save()

    def test_homepage_get_when_logged(self):
        self.client.login(username='user', password='test-view')      
        response = self.client.get(reverse('program_builder:homepage'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_get_when_not_logged(self):
        response = self.client.get(reverse('program_builder:homepage'))
        self.assertEqual(response.status_code, 302)
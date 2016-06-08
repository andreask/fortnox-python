# coding=utf-8
import json
import unittest
import responses
from fortnox.exceptions import ObjectNotFound
from fortnox.requests import Request
from fortnox.config import fortnox_config


class RequestTest(unittest.TestCase):
    def setUp(self):
        fortnox_config.access_token = 'access-token'
        fortnox_config.client_secret = 'client-secret'

    def test_get_with_relative_url(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, 'https://api.fortnox.se/3/instance/1',
                     json={"Instance": {"Id": 1}}, status=200,
                     content_type='application/json')

            response = Request.get('/instance/1')
            response_json = response.json()
            self.assertTrue("Instance" in response_json.keys())
            self.assertTrue("Id" in response_json['Instance'].keys())
            self.assertEqual(1, response_json['Instance']['Id'])

            self.assertEqual(1, len(rsps.calls))
            self.assertEqual("https://api.fortnox.se/3/instance/1", rsps.calls[0].request.url)
            self.assertEqual("application/json", rsps.calls[0].request.headers['Accept'])
            self.assertEqual("application/json", rsps.calls[0].request.headers['Content-Type'])
            self.assertEqual("access-token", rsps.calls[0].request.headers['Access-Token'])
            self.assertEqual("client-secret", rsps.calls[0].request.headers['Client-Secret'])

    def test_get(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, 'https://api.fortnox.se/3/instance',
                     json={"Instances": [{"Id": 1}, {"Id": 2}]}, status=200,
                     content_type='application/json')

            response = Request.get('https://api.fortnox.se/3/instance')
            response_json = response.json()
            self.assertTrue("Instances" in response_json.keys())
            for item in response_json['Instances']:
                self.assertTrue("Id" in item.keys())

            self.assertEqual(1, len(rsps.calls))
            self.assertEqual("https://api.fortnox.se/3/instance", rsps.calls[0].request.url)
            self.assertEqual("application/json", rsps.calls[0].request.headers['Accept'])
            self.assertEqual("application/json", rsps.calls[0].request.headers['Content-Type'])
            self.assertEqual("access-token", rsps.calls[0].request.headers['Access-Token'])
            self.assertEqual("client-secret", rsps.calls[0].request.headers['Client-Secret'])

            rsps.add(responses.GET, 'https://api.fortnox.se/3/instance/1',
                     json={"Instance": {"Id": 1}}, status=200,
                     content_type='application/json')

            response = Request.get('https://api.fortnox.se/3/instance/1')
            response_json = response.json()
            self.assertTrue("Instance" in response_json.keys())
            self.assertTrue("Id" in response_json['Instance'].keys())
            self.assertEqual(1, response_json['Instance']['Id'])

            self.assertEqual(2, len(rsps.calls))
            self.assertEqual("https://api.fortnox.se/3/instance/1", rsps.calls[1].request.url)
            self.assertEqual("application/json", rsps.calls[1].request.headers['Accept'])
            self.assertEqual("application/json", rsps.calls[1].request.headers['Content-Type'])
            self.assertEqual("access-token", rsps.calls[1].request.headers['Access-Token'])
            self.assertEqual("client-secret", rsps.calls[1].request.headers['Client-Secret'])

    def test_get_404(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, 'https://api.fortnox.se/3/instance/4',
                     json={}, status=404, content_type='application/json')

            with self.assertRaises(ObjectNotFound):
                Request.get('https://api.fortnox.se/3/instance/4')

    def test_post(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, 'https://api.fortnox.se/3/instance',
                     json={"Instance": {"Id": 1}}, status=200,
                     content_type='application/json')

            response = Request.post('https://api.fortnox.se/3/instance', {"Id": 1})
            response_json = response.json()
            self.assertTrue("Instance" in response_json.keys())
            self.assertTrue("Id" in response_json['Instance'].keys())
            self.assertEqual(1, response_json['Instance']['Id'])

            self.assertEqual(1, len(rsps.calls))
            self.assertEqual("https://api.fortnox.se/3/instance", rsps.calls[0].request.url)
            self.assertEqual(json.dumps({"Id": 1}), rsps.calls[0].request.body)
            self.assertEqual("application/json", rsps.calls[0].request.headers['Accept'])
            self.assertEqual("application/json", rsps.calls[0].request.headers['Content-Type'])
            self.assertEqual("access-token", rsps.calls[0].request.headers['Access-Token'])
            self.assertEqual("client-secret", rsps.calls[0].request.headers['Client-Secret'])

    def test_post_with_relative_url(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, 'https://api.fortnox.se/3/instance',
                     json={"Instance": {"Id": 1}}, status=200,
                     content_type='application/json')

            response = Request.post('/instance', {"Id": 1})
            response_json = response.json()
            self.assertTrue("Instance" in response_json.keys())
            self.assertTrue("Id" in response_json['Instance'].keys())
            self.assertEqual(1, response_json['Instance']['Id'])

            self.assertEqual(1, len(rsps.calls))
            self.assertEqual("https://api.fortnox.se/3/instance", rsps.calls[0].request.url)
            self.assertEqual("application/json", rsps.calls[0].request.headers['Accept'])
            self.assertEqual("application/json", rsps.calls[0].request.headers['Content-Type'])
            self.assertEqual("access-token", rsps.calls[0].request.headers['Access-Token'])
            self.assertEqual("client-secret", rsps.calls[0].request.headers['Client-Secret'])

    def test_put(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.PUT, 'https://api.fortnox.se/3/instance/1',
                     json={"Instance": {"Id": 1, "Name": "Test name"}}, status=200,
                     content_type='application/json')

            response = Request.put('https://api.fortnox.se/3/instance/1', {"Id": 1, "Name": "Test name"})
            response_json = response.json()
            self.assertTrue("Instance" in response_json.keys())
            self.assertTrue("Id" in response_json['Instance'].keys())
            self.assertEqual(1, response_json['Instance']['Id'])
            self.assertTrue("Name" in response_json['Instance'].keys())
            self.assertEqual("Test name", response_json['Instance']['Name'])

            self.assertEqual(1, len(rsps.calls))
            self.assertEqual("https://api.fortnox.se/3/instance/1", rsps.calls[0].request.url)
            self.assertEqual(json.dumps({"Id": 1, "Name": "Test name"}), rsps.calls[0].request.body)
            self.assertEqual("application/json", rsps.calls[0].request.headers['Accept'])
            self.assertEqual("application/json", rsps.calls[0].request.headers['Content-Type'])
            self.assertEqual("access-token", rsps.calls[0].request.headers['Access-Token'])
            self.assertEqual("client-secret", rsps.calls[0].request.headers['Client-Secret'])

    def test_put_with_relative_url(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.PUT, 'https://api.fortnox.se/3/instance/1',
                     json={"Instance": {"Id": 1, "Name": "Test name"}}, status=200,
                     content_type='application/json')

            response = Request.put('/instance/1', {"Id": 1, "Name": "Test name"})
            response_json = response.json()
            self.assertTrue("Instance" in response_json.keys())
            self.assertTrue("Id" in response_json['Instance'].keys())
            self.assertEqual(1, response_json['Instance']['Id'])
            self.assertTrue("Name" in response_json['Instance'].keys())
            self.assertEqual("Test name", response_json['Instance']['Name'])

            self.assertEqual(1, len(rsps.calls))
            self.assertEqual("https://api.fortnox.se/3/instance/1", rsps.calls[0].request.url)
            self.assertEqual(json.dumps({"Id": 1, "Name": "Test name"}), rsps.calls[0].request.body)
            self.assertEqual("application/json", rsps.calls[0].request.headers['Accept'])
            self.assertEqual("application/json", rsps.calls[0].request.headers['Content-Type'])
            self.assertEqual("access-token", rsps.calls[0].request.headers['Access-Token'])
            self.assertEqual("client-secret", rsps.calls[0].request.headers['Client-Secret'])

#!/usr/bin/python3.5

import random
import unittest
import requests
from bs4 import BeautifulSoup

class tests(unittest.TestCase):
    server = "http://localhost:8080/"

    def create_user(self, user, passwd='12345678'):
        x = requests.get("%sregister"%self.server)
        id = x.cookies
        x = BeautifulSoup(x.text, 'html.parser')
        x = x.find_all("input")
        payload={"username":user, "password":passwd, "passwordConfirm":passwd}
        for y in x:
            if y["name"] == "_csrf":
                payload[y["name"]] = y["value"]
        return requests.post("%sregister"%self.server, payload, cookies=id)

    def test_create_user(self):
        user="test_%s"%''.join(random.sample('0123456789',5))
        response = self.create_user(user=user)
        y = BeautifulSoup(response.text, 'html.parser').find_all("form")
        y2 = BeautifulSoup(response.text, 'html.parser').find_all("span")

        for z in y:
            if z['id'] == 'logoutForm':
                self.assertTrue(True, "Logged in successfully")
                return
        self.assertTrue(False)

    def test_create_user_short_pw(self):
        user="test_%s"%''.join(random.sample('0123456789',5))
        response = self.create_user(user=user, passwd='1234567')
        y = BeautifulSoup(response.text, 'html.parser').find_all("form")
        y2 = BeautifulSoup(response.text, 'html.parser').find_all("span")

        for z in y:
            if z['id'] == 'logoutForm':
                self.assertTrue(False, "Should not have been able to login.")
                return

        for z in y2:
            if z['id'] == 'passeord.errors':
                self.assertTrue(True)
                return
            if z['id'] == 'username.errors':
                self.assertTrue(False, "Should not have username errors:")


    def test_create_user_short_un(self):
        user="test_"
        response = self.create_user(user=user, passwd='12345678')
        y = BeautifulSoup(response.text, 'html.parser').find_all("form")
        y2 = BeautifulSoup(response.text, 'html.parser').find_all("span")

        for z in y:
            if z['id'] == 'logoutForm':
                self.assertTrue(False, "Should not have been able to login.")
                return

        for z in y2:
            if z['id'] == 'passeord.errors':
                self.assertTrue(False, "Password should be long enough.")
                return
            if z['id'] == 'username.errors':
                if z.next == "Please use between 6 and 32 characters.":
                    self.assertTrue(True, "Should not have username errors:")
                else:
                    self.assertTrue(False, "UN should be unique")

    def test_login(self):
        user = "test_%s" % ''.join(random.sample('0123456789', 5))
        passwd = "123456789"
        self.create_user(user, passwd=passwd)
        x = requests.get("%slogin"%self.server)
        id = x.cookies
        x = BeautifulSoup(x.text, 'html.parser')
        x = x.find_all("input")
        payload={"username":user, "password":passwd}
        for y in x:
            if y["name"] == "_csrf":
                payload[y["name"]] = y["value"]

        response = requests.post("%slogin"%self.server, payload, cookies=id)
        response = BeautifulSoup(response.text, 'html.parser')
        y = BeautifulSoup(response.text, 'html.parser').find_all("form")

        for z in y:
            if z['id'] == 'logoutForm':
                self.assertTrue(True, "Logged in successfully")
                return
            self.assertTrue(False)


    def test_login_false(self):
        user = "test_%s" % ''.join(random.sample('0123456789', 5))
        passwd = "123456789"
        self.create_user(user, passwd=passwd)
        x = requests.get("%slogin"%self.server)
        id = x.cookies
        x = BeautifulSoup(x.text, 'html.parser')
        x = x.find_all("input")
        payload={"username":user, "password":passwd+"x"}
        for y in x:
            if y["name"] == "_csrf":
                payload[y["name"]] = y["value"]

        response = requests.post("%slogin"%self.server, payload, cookies=id)
        response = BeautifulSoup(response.text, 'html.parser')
        y = BeautifulSoup(response.text, 'html.parser').find_all("form")

        for z in y:
            if z['id'] == 'logoutForm':
                self.assertTrue(False, "Used Wrong PW, should not have logged in")
                return
            self.assertTrue(True)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(tests)
    unittest.TextTestRunner(verbosity=2).run(suite)
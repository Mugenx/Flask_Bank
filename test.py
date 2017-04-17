"""
Created on March 24th, 2016

@author: Guobin Wu
version: 2.0
professor: Stanley Pieda
file name: test.py

description: testing database connection
"""

from unittest.mock import MagicMock
import unittest
import sqlite3


class MyTest(unittest.TestCase):
    def test_sqlite3_connect_success(self):
        sqlite3.connect = MagicMock(return_value='connection succeeded')

        dbc = DataBaseClass()
        sqlite3.connect.assert_called_with('db/sample.db')
        self.assertEqual(dbc.connection, 'connection succeeded')


class DataBaseClass():
    def __init__(self, connection_string='db/sample.db'):
        self.connection = sqlite3.connect(connection_string)


if __name__ == '__main__':
    unittest.main()

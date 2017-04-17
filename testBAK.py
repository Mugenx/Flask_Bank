import unittest

from flask import Flask
from flask_testing import TestCase


class TestRenderTemplates(TestCase):
    render_templates = True

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def test_assert_template_used(self):
        try:
            self.client.get("/template/")
            self.assert_template_used("welcome.html")
        except RuntimeError:
            pass


if __name__ == '__main__':
    unittest.main()

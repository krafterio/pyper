# Copyright Krafter SAS <hey@krafter.io>
# Odoo Proprietary License (see LICENSE file).

from odoo.addons.base.tests.common import HttpCaseWithUserDemo
from odoo.tests.common import tagged

@tagged("-at_install", "post_install")
class WebManifestTest(HttpCaseWithUserDemo):
    """
    This test suite is used to request the routes used by the PWA backend implementation.
    """

    def test_webmanifest_format_user_logged(self):
        """
        Test if the webmanifest is well formated when a user is logged in.
        """

        # Login as our test consist to be logged in.
        self.authenticate(
            'demo',
            'demo'
        )
        self.check_webmanifest_format()
    
    def test_offline_route_user_logged(self):
        """
        Test if the offline route is here when a user is logged in.
        """

        # Login as our test consist to be logged in.
        self.authenticate(
            'demo',
            'demo'
        )
        self.check_offline_route()


    def test_webmanifest_format_user_unauthenticated(self):
        """
        Test if the webmanifest is well formated when a user is not logged in.
        """
        self.check_webmanifest_format()

    def test_offline_route_user_unauthenticated(self):
        """
        Test if the offline route is here when a user is not logged in.
        """
        self.check_offline_route()


    def check_webmanifest_format(self):
        """
        Check if the webmanifest is well formated.
        """
        response = self.url_open("/web/manifest.webmanifest")

        # Check if the page exists.
        self.assertEqual(response.status_code, 200)

        # As we edited manifest, we can't rely on value. Only check their existence and type.
        self.assertGreater(len(response.headers["Content-Type"]), 0)
        self.assertIsInstance(response.headers["Content-Type"], str)

        data = response.json()
        self.assertGreater(len(data["name"]), 0)
        self.assertIsInstance(data["name"], str)

        self.assertGreater(len(data["scope"]), 0)
        self.assertIsInstance(data["scope"], str)

        self.assertGreater(len(data["start_url"]), 0)
        self.assertIsInstance(data["start_url"], str)

        self.assertGreater(len(data["display"]), 0)
        self.assertIsInstance(data["display"], str)

        self.assertGreater(len(data["background_color"]), 0)
        self.assertIsInstance(data["background_color"], str)

        self.assertGreater(len(data["theme_color"]), 0)
        self.assertIsInstance(data["theme_color"], str)

        self.assertIsInstance(data["prefer_related_applications"], bool)

        self.assertGreaterEqual(len(data["icons"]), 0)
        for icon in data["icons"]:
            self.assertGreater(len(icon["src"]), 0)
            self.assertGreater(len(icon["sizes"]), 0)
            self.assertGreater(len(icon["type"]), 0)

        self.assertGreaterEqual(len(data["shortcuts"]), 0)
        for shortcut in data["shortcuts"]:
            self.assertGreater(len(shortcut["name"]), 0)
            self.assertGreater(len(shortcut["description"]), 0)
            self.assertGreater(len(shortcut["icons"]), 0)

    def check_offline_route(self):
        """
        Check if the offline route exists.
        """
        response = self.url_open("/web/offline")

        # Check if the page exists.
        self.assertEqual(response.status_code, 200)

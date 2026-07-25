import unittest

from workstation import ModelRouter, Node


class RouterTests(unittest.TestCase):
    def setUp(self):
        self.router = ModelRouter(
            [Node("a", "http://192.0.2.10:8080", 8), Node("b", "http://192.0.2.20:8080", 4)]
        )

    def test_routes_to_healthy_capacity(self):
        self.assertEqual(self.router.route(6).name, "a")

    def test_fails_over(self):
        self.router.mark_unhealthy("a")
        self.assertEqual(self.router.route(2).name, "b")

    def test_rejects_when_capacity_is_insufficient(self):
        self.assertIsNone(self.router.route(20))

    def test_balances_active_requests(self):
        self.assertEqual(self.router.route().name, "a")
        self.assertEqual(self.router.route().name, "b")

    def test_recovery_resets_node(self):
        self.router.mark_unhealthy("a")
        self.router.recover("a")
        self.assertTrue(self.router.nodes[0].healthy)


if __name__ == "__main__":
    unittest.main()


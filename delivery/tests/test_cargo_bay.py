import unittest
from delivery.agents.uav.components.CargoBay import CargoBay
from delivery.agents.Item import Item


class CargoBayTest(unittest.TestCase):

    def setUp(self):
        self.cargo_bay = CargoBay(item=None)
        self.item = Item(destination=(0, 0),priority=1, iid=0)

    def test_init(self):
        self.assertIsNone(self.cargo_bay.item)

        self.cargo_bay = CargoBay(item=self.item)

        self.assertIs(self.cargo_bay.item, self.item)

    def test_is_empty(self):
        # 1st Test: No item, result: True
        self.assertTrue(self.cargo_bay.is_empty())

        # 2nd Test: Add item, result: False
        self.cargo_bay.item = self.item
        self.assertFalse(self.cargo_bay.is_empty())

    def test_store_item(self):
        # Test: Add item, result: cargo_bay.item = self.item
        self.cargo_bay.store_item(self.item)
        self.assertEqual(self.cargo_bay.item, self.item)

    def test_remove_item(self):
        # Test: Add item and check if Item is None after and delivered is set to True in item
        self.cargo_bay.item = self.item

        self.cargo_bay.remove_item()
        self.assertIsNone(self.cargo_bay.item)
        self.assertTrue(self.item.delivered)

    def test_get_destination(self):
        # 1st Test: No item, result: None
        self.assertIsNone(self.cargo_bay.get_destination())

        # 2nd Test: Add item, result: (0,0)
        self.cargo_bay.item = self.item
        self.assertEqual(self.cargo_bay.get_destination(), (0, 0))

    def test_get_item(self):
        # 1st Test: No item, result: None
        self.assertIsNone(self.cargo_bay.get_item())

        # 2nd Test: Set item, result: item
        self.cargo_bay.item = self.item
        self.assertIs(self.cargo_bay.get_item(), self.item)

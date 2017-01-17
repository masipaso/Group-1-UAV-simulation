import unittest
from delivery.agents.uav.components.CargoBay import CargoBay
from delivery.agents.Item import Item

class cargoBay_Test(unittest.TestCase):

    def setUp(self):
        self.cargobay = CargoBay(item= None)
        self.item = Item(destination=(0,0),priority=1,iid=0)

    def test_init(self):
        self.assertIsNone(self.cargobay.item)

        self.cargobay = CargoBay(item=self.item)

        self.assertIs(self.cargobay.item, self.item)

    def test_is_empty(self):
        # 1st Test: No item, result: True
        self.assertTrue(self.cargobay.is_empty())

        # 2nd Test: Add item, result: False
        self.cargobay.item = self.item
        self.assertFalse(self.cargobay.is_empty())

    def test_store_item(self):
        # Test: Add item, result: cargobay.item = self.item
        self.cargobay.store_item(self.item)
        self.assertEqual(self.cargobay.item,self.item)

    def test_remove_item(self):
        # Test: Add item and check if Item is None after and delivered is set to True in item
        self.cargobay.item = self.item

        self.cargobay.remove_item()
        self.assertIsNone(self.cargobay.item)
        self.assertTrue(self.item.delivered)

    def test_get_destination(self):
        # 1st Test: No item, result: None
        self.assertIsNone(self.cargobay.get_destination())

        # 2nd Test: Add item, result: (0,0)
        self.cargobay.item = self.item
        self.assertEqual(self.cargobay.get_destination(),(0,0))

    def test_get_item(self):
        # 1st Test: No item, result: None
        self.assertIsNone(self.cargobay.get_item())

        # 2nd Test: Set item, result: item
        self.cargobay.item = self.item
        self.assertIs(self.cargobay.get_item(), self.item)

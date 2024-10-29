import unittest
from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def setUp(self):
        """Create a library of items used across tests"""
        self.items = {
            # Regular items at different states
            'regular': {
                'standard': Item("Regular Item", sell_in=5, quality=10),
                'expired': Item("Regular Item", sell_in=0, quality=10),
                'zero_quality': Item("Regular Item", sell_in=5, quality=0),
            },
        }

    def test_normal_item_before_sell_date(self):
        item = self._create_item_copy(self.items['regular']['standard'])
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(4, item.sell_in)
        self.assertEqual(9, item.quality)

    def test_normal_item_after_sell_date(self):
        item = self._create_item_copy(self.items['regular']['expired'])
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(8, item.quality)

    def test_normal_item_quality_never_negative(self):
        item = self._create_item_copy(self.items['regular']['zero_quality'])
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(4, item.sell_in)
        self.assertEqual(0, item.quality)


    def _create_item_copy(self, item):
        """Create a copy of an item to ensure test isolation"""
        return Item(item.name, item.sell_in, item.quality)


if __name__ == '__main__':
    unittest.main()
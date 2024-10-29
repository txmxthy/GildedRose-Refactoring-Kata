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
            # Aged Brie at different states
            'aged_brie': {
                'standard': Item("Aged Brie", sell_in=5, quality=10),
                'expired': Item("Aged Brie", sell_in=0, quality=10),
                'max_quality': Item("Aged Brie", sell_in=5, quality=50),
            },

            # Sulfuras is always the same
            'sulfuras': {
                'standard': Item("Sulfuras, Hand of Ragnaros", sell_in=5, quality=80),
            },

            # Backstage passes at different states
            'backstage': {
                'far_future': Item("Backstage passes to a TAFKAL80ETC concert", sell_in=11, quality=10),
                'medium_close': Item("Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=10),
                'very_close': Item("Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=10),
                'expired': Item("Backstage passes to a TAFKAL80ETC concert", sell_in=0, quality=10),
                'near_max_quality': Item("Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49),
            },
            # Conjured items at different states
            'conjured': {
                'standard': Item("Conjured Mana Cake", sell_in=5, quality=10),
                'expired': Item("Conjured Mana Cake", sell_in=0, quality=10),
                'low_quality': Item("Conjured Mana Cake", sell_in=5, quality=1),
                'zero_quality': Item("Conjured Mana Cake", sell_in=5, quality=0),
            }
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

    def test_aged_brie_before_sell_date(self):
        item = self._create_item_copy(self.items['aged_brie']['standard'])
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(4, item.sell_in)
        self.assertEqual(11, item.quality)

    def test_aged_brie_after_sell_date(self):
        item = self._create_item_copy(self.items['aged_brie']['expired'])
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(12, item.quality)

    def test_aged_brie_quality_max_50(self):
        item = self._create_item_copy(self.items['aged_brie']['max_quality'])
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(4, item.sell_in)
        self.assertEqual(50, item.quality)

    def test_sulfuras_never_changes(self):
        item = self._create_item_copy(self.items['sulfuras']['standard'])
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(5, item.sell_in)
        self.assertEqual(80, item.quality)

    def test_backstage_pass_long_before_concert(self):
        item = self._create_item_copy(self.items['backstage']['far_future'])
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(10, item.sell_in)
        self.assertEqual(11, item.quality)

    def test_backstage_pass_medium_close_to_concert(self):
        item = self._create_item_copy(self.items['backstage']['medium_close'])
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(9, item.sell_in)
        self.assertEqual(12, item.quality)

    def test_backstage_pass_very_close_to_concert(self):
        item = self._create_item_copy(self.items['backstage']['very_close'])
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(4, item.sell_in)
        self.assertEqual(13, item.quality)

    def test_backstage_pass_after_concert(self):
        item = self._create_item_copy(self.items['backstage']['expired'])
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(0, item.quality)

    def test_backstage_pass_quality_max_50(self):
        item = self._create_item_copy(self.items['backstage']['near_max_quality'])
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(4, item.sell_in)
        self.assertEqual(50, item.quality)

    def test_conjured_item_before_sell_date(self):
        item = self._create_item_copy(self.items['conjured']['standard'])
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(4, item.sell_in)
        self.assertEqual(8, item.quality)  # Degrades by 2

    def test_conjured_item_after_sell_date(self):
        item = self._create_item_copy(self.items['conjured']['expired'])
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(6, item.quality)  # Degrades by 4

    def test_conjured_item_near_zero_quality(self):
        item = self._create_item_copy(self.items['conjured']['low_quality'])
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(4, item.sell_in)
        self.assertEqual(0, item.quality)  # Would degrade by 2 but hits 0

    def test_conjured_item_zero_quality(self):
        item = self._create_item_copy(self.items['conjured']['zero_quality'])
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(4, item.sell_in)
        self.assertEqual(0, item.quality)  # Stays at 0

    def test_multiple_items(self):
        items = [
            self._create_item_copy(self.items['regular']['standard']),
            self._create_item_copy(self.items['aged_brie']['standard'])
        ]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(9, items[0].quality)
        self.assertEqual(4, items[1].sell_in)
        self.assertEqual(11, items[1].quality)

    def _create_item_copy(self, item):
        """Create a copy of an item to ensure test isolation"""
        return Item(item.name, item.sell_in, item.quality)

    if __name__ == '__main__':
        unittest.main()

# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class ItemStrategy(ABC):
    """Abstract base class for item update strategies"""

    @abstractmethod
    def update_quality(self, item):
        pass

    def _decrease_sell_in(self, item):
        item.sell_in -= 1

    def _decrease_quality(self, item):
        if item.quality > 0:
            item.quality -= 1

    def _increase_quality(self, item):
        if item.quality < 50:
            item.quality += 1


class RegularItemStrategy(ItemStrategy):
    """Strategy for regular items"""

    def update_quality(self, item):
        self._decrease_quality(item)
        self._decrease_sell_in(item)

        if item.sell_in < 0:
            self._decrease_quality(item)


class AgedBrieStrategy(ItemStrategy):
    """Strategy for Aged Brie"""

    def update_quality(self, item):
        self._increase_quality(item)
        self._decrease_sell_in(item)

        if item.sell_in < 0:
            self._increase_quality(item)


class BackstagePassStrategy(ItemStrategy):
    """Strategy for Backstage passes"""

    def update_quality(self, item):
        self._increase_quality(item)

        if item.sell_in <= 10:
            self._increase_quality(item)
        if item.sell_in <= 5:
            self._increase_quality(item)

        self._decrease_sell_in(item)

        if item.sell_in < 0:
            item.quality = 0


class SulfurasStrategy(ItemStrategy):
    """Strategy for Sulfuras - legendary item that never changes"""

    def update_quality(self, item):
        pass  # Sulfuras never changes


class GildedRose:
    def __init__(self, items):
        self.items = items
        self.regular_strategy = RegularItemStrategy()
        self.brie_strategy = AgedBrieStrategy()
        self.backstage_strategy = BackstagePassStrategy()
        self.sulfuras_strategy = SulfurasStrategy()

    def update_quality(self):
        for item in self.items:
            if item.name == "Aged Brie":
                self.brie_strategy.update_quality(item)
            elif item.name == "Backstage passes to a TAFKAL80ETC concert":
                self.backstage_strategy.update_quality(item)
            elif item.name == "Sulfuras, Hand of Ragnaros":
                self.sulfuras_strategy.update_quality(item)
            else:
                self.regular_strategy.update_quality(item)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
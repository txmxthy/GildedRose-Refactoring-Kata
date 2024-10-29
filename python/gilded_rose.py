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


class GildedRose:
    def __init__(self, items):
        self.items = items
        self.regular_strategy = RegularItemStrategy()
        self.brie_strategy = AgedBrieStrategy()

    def update_quality(self):
        for item in self.items:
            if item.name == "Aged Brie":
                self.brie_strategy.update_quality(item)
                continue

            if (item.name != "Backstage passes to a TAFKAL80ETC concert"
                    and item.name != "Sulfuras, Hand of Ragnaros"):
                self.regular_strategy.update_quality(item)
                continue

            # Original logic for remaining special items
            if item.name != "Backstage passes to a TAFKAL80ETC concert":
                if item.quality > 0:
                    if item.name != "Sulfuras, Hand of Ragnaros":
                        item.quality = item.quality - 1
            else:
                if item.quality < 50:
                    item.quality = item.quality + 1
                    if item.name == "Backstage passes to a TAFKAL80ETC concert":
                        if item.sell_in < 11:
                            if item.quality < 50:
                                item.quality = item.quality + 1
                        if item.sell_in < 6:
                            if item.quality < 50:
                                item.quality = item.quality + 1
            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in = item.sell_in - 1
            if item.sell_in < 0:
                if item.name != "Backstage passes to a TAFKAL80ETC concert":
                    if item.quality > 0:
                        if item.name != "Sulfuras, Hand of Ragnaros":
                            item.quality = item.quality - 1
                else:
                    item.quality = item.quality - item.quality


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
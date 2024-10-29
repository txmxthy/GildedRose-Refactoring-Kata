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
    def update_quality(self, item):
        self._decrease_quality(item)
        self._decrease_sell_in(item)

        if item.sell_in < 0:
            self._decrease_quality(item)


class ConjuredItemStrategy(ItemStrategy):
    def update_quality(self, item):
        # Degrades twice as fast as normal items
        # Hacky, will do another implementation to show another wayde
        self._decrease_quality(item)
        self._decrease_quality(item)
        self._decrease_sell_in(item)

        if item.sell_in < 0:
            self._decrease_quality(item)
            self._decrease_quality(item)


class AgedBrieStrategy(ItemStrategy):
    def update_quality(self, item):
        self._increase_quality(item)
        self._decrease_sell_in(item)

        if item.sell_in < 0:
            self._increase_quality(item)


class BackstagePassStrategy(ItemStrategy):
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
    def update_quality(self, item):
        pass


class ItemStrategyFactory:
    """Factory for creating item strategies"""

    _strategies = {
        "Aged Brie": AgedBrieStrategy(),
        "Backstage passes to a TAFKAL80ETC concert": BackstagePassStrategy(),
        "Sulfuras, Hand of Ragnaros": SulfurasStrategy(),
        "Conjured Mana Cake": ConjuredItemStrategy()
    }

    _default_strategy = RegularItemStrategy()

    @classmethod
    def create_strategy(cls, item):
        return cls._strategies.get(item.name, cls._default_strategy)


class GildedRose:
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            strategy = ItemStrategyFactory.create_strategy(item)
            strategy.update_quality(item)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
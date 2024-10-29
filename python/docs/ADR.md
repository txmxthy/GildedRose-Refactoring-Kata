# Gilded Rose Refactoring Notes

## Progress
- [x] Set up test suite with item library
- [x] First strategy implementation (Regular items)
- [ ] Aged Brie strategy
- [ ] Backstage passes strategy
- [ ] Sulfuras strategy
- [ ] Factory implementation
- [ ] Conjured items strategy

## Architecture Decision Record (ADR)

### Context
Legacy codebase with mixed item logic needs extension for new "Conjured" items.

### Approach

#### Strategy Pattern
- Using the strategy pattern to define a family of algorithms that can be used interchangeably. 
- Each item type (Regular, Aged Brie, etc.) gets its own strategy class that handles its specific quality update rules. 
- The base strategy defines the common interface and shared behaviors.

#### Factory Pattern
- Creates objects (in our case, strategies) without directly exposing the creation logic. 
- The factory will examine an item and return the appropriate strategy to handle it. 
- This keeps the main code clean and makes adding new item types easier.
Implementation Approach

1. Create one strategy at a time
2. Keep old code working for other items
3. Add factory once all strategies are done
4. Finally clean up the main class

This incremental approach lets us refactor safely while keeping the system working at all times.

### Benefits
- Lower risk of breaking changes
- Easier code review
- Each step independently valuable

### Drawbacks
- Temporary dual implementation styles
- Extra care needed during transition

## Implementation Notes
- Started with regular items as foundation
- Moving special cases one at a time
- Running full test suite after each change
- Will add factory once patterns emerge

# Implementation Log

Tests
* Made test suite with library of item cases to make referencing them easier.
* Setup tests for each item case

Regular Item Strategy
* Added base ItemStrategy class with common quality operations
* Implemented RegularItemStrategy for basic items
* Modified GildedRose to use strategy for regular items only
* All tests passing

Aged Brie Strategy

* Added AgedBrieStrategy with quality increase logic
* Added increase_quality helper to base strategy
* All tests passing

Backstage Passes Strategy
* Added BackstagePassStrategy with concert approach rules
* Simplified remaining legacy code
* All tests passing

Sulfuras Strategy
* Added SulfurasStrategy (no-op implementation)
* Removed last of legacy code
* All tests passing
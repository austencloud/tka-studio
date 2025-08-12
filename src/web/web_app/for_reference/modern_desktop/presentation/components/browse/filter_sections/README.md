"""
Filter Sections - DEPRECATED

This directory contained overengineered filter components that have been
simplified and inlined into the main FilterSelectionPanel.

OLD APPROACH (removed):

- FilterCategorySection: Separate QFrame with glassmorphism
- QuickAccessSection: Separate QFrame with glassmorphism
- Multiple levels of container hierarchy

NEW APPROACH (in FilterSelectionPanel):

- Inline category and quick access creation
- Single glassmorphism layer on main panel
- Flat hierarchy with unified styling
- Everything fits on one screen

The old components created visual noise with:

- 3 levels of glassmorphism containers
- Competing visual elements
- Complex responsive logic
- Inconsistent styling approaches

The new design achieves 10/10 UX with:

- Clean, flat visual hierarchy
- Unified button styling
- Compact, single-page layout
- Consistent design system usage
  """

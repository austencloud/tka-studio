"""
Option Pool Service - Pure Pool Management Logic

Manages pool item availability and lifecycle without Qt dependencies.
Extracted from option_factory.py to maintain clean architecture.
"""

from typing import Dict, Optional, Set


class OptionPoolService:
    """
    Pure service for managing option pool availability.

    No Qt dependencies - manages pool identifiers only.
    """

    def __init__(self, max_items: int = 100):
        """Initialize pool with specified maximum items."""
        self._max_items = max_items
        self._available_ids: Set[int] = set(range(max_items))
        self._in_use_ids: Set[int] = set()

    def checkout_item(self) -> Optional[int]:
        """
        Get available pool item ID.

        Returns pool ID (int) - presentation layer maps to actual Qt widgets.
        """
        # PAGINATION DEBUG: Log pool state before checkout
        available_count = len(self._available_ids)
        in_use_count = len(self._in_use_ids)

        if self._available_ids:
            item_id = self._available_ids.pop()
            self._in_use_ids.add(item_id)

            # PAGINATION DEBUG: Log successful checkout
            print(f"🔍 [PAGINATION_DEBUG] OptionPoolService.checkout_item:")
            print(f"   Checked out item {item_id}")
            print(
                f"   Pool state: {available_count-1} available, {in_use_count+1} in use"
            )

            return item_id

        # If no available items, we should not reuse items that are still in use
        # This prevents the "disappearing first pictograph" bug
        # Instead, return None to indicate pool exhaustion
        print(f"🔍 [PAGINATION_DEBUG] OptionPoolService.checkout_item:")
        print(f"   ⚠️ POOL EXHAUSTED - all {self._max_items} items in use")
        print(f"   Available: {available_count}, In use: {in_use_count}")
        return None

    def checkin_item(self, item_id: int) -> None:
        """
        Return item ID to pool.

        Pure pool management - no Qt widget handling.
        """
        # PAGINATION DEBUG: Log checkin process
        was_in_use = item_id in self._in_use_ids
        available_before = len(self._available_ids)
        in_use_before = len(self._in_use_ids)

        if item_id in self._in_use_ids:
            self._in_use_ids.remove(item_id)
            self._available_ids.add(item_id)

            print(f"🔍 [PAGINATION_DEBUG] OptionPoolService.checkin_item:")
            print(f"   Checked in item {item_id}")
            print(
                f"   Pool state: {available_before+1} available, {in_use_before-1} in use"
            )
        else:
            print(f"🔍 [PAGINATION_DEBUG] OptionPoolService.checkin_item:")
            print(f"   ⚠️ Attempted to check in item {item_id} that was not in use")
            print(
                f"   Pool state unchanged: {available_before} available, {in_use_before} in use"
            )

    def reset_pool(self) -> None:
        """Reset entire pool to available state."""
        self._available_ids = set(range(self._max_items))
        self._in_use_ids.clear()

    def get_usage_stats(self) -> Dict[str, int]:
        """Get pool usage statistics."""
        return {
            "available": len(self._available_ids),
            "in_use": len(self._in_use_ids),
            "total": self._max_items,
            "utilization_percent": int((len(self._in_use_ids) / self._max_items) * 100),
        }

    def is_item_available(self, item_id: int) -> bool:
        """Check if specific item ID is available."""
        return item_id in self._available_ids

    def is_item_in_use(self, item_id: int) -> bool:
        """Check if specific item ID is in use."""
        return item_id in self._in_use_ids

    def get_available_count(self) -> int:
        """Get count of available items."""
        return len(self._available_ids)

    def get_in_use_count(self) -> int:
        """Get count of items in use."""
        return len(self._in_use_ids)

    def force_checkin_all(self) -> None:
        """Force all items back to available state (emergency reset)."""
        self.reset_pool()

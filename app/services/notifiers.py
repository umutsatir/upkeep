# OWNER: MEMBER-4
# Decorator Pattern — Low-Stock Alert Channels
#
# LowStockNotifier (abstract base)
#   └── LogNotifier (concrete base — writes to Python logger)
#   └── NotifierDecorator (abstract decorator base)
#       ├── EmailAlertDecorator — simulates email delivery
#       └── SlackAlertDecorator — simulates Slack webhook delivery
#
# Usage:
#   notifier = SlackAlertDecorator(EmailAlertDecorator(LogNotifier()))
#   notifier.notify(item)  # logs + "emails" + "slacks"

from __future__ import annotations

import logging
from abc import ABC, abstractmethod

from app.models.inventory import InventoryItem

logger = logging.getLogger("upkeep.notifications")


class LowStockNotifier(ABC):
    """Base class for the low-stock notification chain (Decorator pattern)."""

    @abstractmethod
    def notify(self, item: InventoryItem) -> list[str]:
        """Send a low-stock alert for *item*.

        Returns a list of channel names that were notified, useful for
        logging and testing.
        """
        ...


class LogNotifier(LowStockNotifier):
    """Concrete base notifier — writes to the Python logger."""

    def notify(self, item: InventoryItem) -> list[str]:
        logger.warning(
            "LOW STOCK ALERT: '%s' (SKU: %s) has %d %s remaining "
            "(threshold: %d)",
            item.name,
            item.sku,
            item.quantity_on_hand,
            item.unit,
            item.low_stock_threshold,
        )
        return ["log"]


class NotifierDecorator(LowStockNotifier, ABC):
    """Abstract decorator — wraps another LowStockNotifier."""

    def __init__(self, wrapped: LowStockNotifier) -> None:
        self._wrapped = wrapped


class EmailAlertDecorator(NotifierDecorator):
    """Adds email delivery to the notification chain.

    In a production system this would call an SMTP service or a
    transactional-email API.  Here we simulate by logging.
    """

    def notify(self, item: InventoryItem) -> list[str]:
        channels = self._wrapped.notify(item)
        logger.info(
            "EMAIL SENT: Low stock alert for '%s' (SKU: %s) — %d %s left",
            item.name,
            item.sku,
            item.quantity_on_hand,
            item.unit,
        )
        channels.append("email")
        return channels


class SlackAlertDecorator(NotifierDecorator):
    """Adds Slack webhook delivery to the notification chain.

    In production this would POST to a Slack Incoming Webhook URL.
    Here we simulate by logging.
    """

    def notify(self, item: InventoryItem) -> list[str]:
        channels = self._wrapped.notify(item)
        logger.info(
            "SLACK SENT: :warning: Low stock — *%s* (SKU: %s) has %d %s remaining",
            item.name,
            item.sku,
            item.quantity_on_hand,
            item.unit,
        )
        channels.append("slack")
        return channels


def build_default_notifier() -> LowStockNotifier:
    """Factory that builds the default notification chain.

    Chain: Log → Email → Slack
    Each call to notify() will trigger all three channels.
    """
    return SlackAlertDecorator(EmailAlertDecorator(LogNotifier()))

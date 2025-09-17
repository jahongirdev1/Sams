import logging
from typing import Any

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None

from django.conf import settings

logger = logging.getLogger(__name__)


def send_telegram_message(text: str) -> None:
    """Send a message to the configured Telegram chat."""
    token = '8281238479:AAFpptxxRGeOUs3YO3hQRdqF5cGzdpimQpM'
    chat_id = '758761122'

    if not token or not chat_id:
        logger.warning("Telegram credentials are not configured; message not sent.")
        return

    if requests is None:
        logger.warning("Requests library is unavailable; Telegram message not sent.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload: dict[str, Any] = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }

    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        logger.exception("Failed to send Telegram message.")
    except Exception:
        logger.exception("Unexpected error while sending Telegram message.")

# -*- coding: utf-8 -*-
import logging
import threading
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger("client_utils")

GLOBAL_QUEUE = "global_queue"

_on_send_message_req: Optional[Callable] = None

def set_send_message_handler(handler: Callable):
    global _on_send_message_req
    _on_send_message_req = handler

def run_on_queue(func: Callable, queue: Any = None):
    """Executes task in background thread / queue."""
    t = threading.Thread(target=func, daemon=True)
    t.start()
    return t

def get_current_account() -> int:
    return 0

def send_message(peer_id: int, text: str, reply_to: Optional[int] = None, account: int = 0) -> bool:
    """Sends a message via Telegram Desktop client."""
    logger.info(f"[SendMessage] account={account} peer={peer_id} text={text[:50]}")
    if _on_send_message_req:
        return _on_send_message_req(account, peer_id, text, reply_to)
    return True

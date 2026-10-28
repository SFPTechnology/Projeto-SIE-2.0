"""B07: local development-only bounded sliding-window rate control.

This is an extra local safety limit, NOT a distributed production limiter.
No Authorization token, PII, or user identifiers are stored in the counters.
"""
from __future__ import annotations
from collections import deque
import threading
import time


_LOCK=threading.Lock()
_REQUESTS: dict[str, deque[float]]={}


def consume(peer: str,limit: int,now: float|None=None) -> bool:
    if limit < 1 or limit > 10000:
        raise ValueError("invalid local rate limit")
    moment=time.monotonic() if now is None else now
    with _LOCK:
        # Prune stale clients to bound local process memory.
        if len(_REQUESTS)>1000:
            for key in list(_REQUESTS):
                q=_REQUESTS[key]
                while q and moment-q[0]>=60: q.popleft()
                if not q: del _REQUESTS[key]
        q=_REQUESTS.setdefault(peer,deque())
        while q and moment-q[0]>=60: q.popleft()
        if len(q)>=limit: return False
        q.append(moment)
        return True


def reset_dev_test_only():
    with _LOCK: _REQUESTS.clear()

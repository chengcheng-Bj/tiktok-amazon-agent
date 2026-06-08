import os
import requests
import time
import 

# --------------------
# Scoring configuration (derived from Manus.txt)
# --------------------
# These weights can be tuned for different markets.
W_SHARES = 0.3
W_SAVES = 0.4
W_ENGAGEMENT = 0.1
W_FRESHNESS = 0.15
W_AUTHOR = 0.05
DECAY_RATE = 0.1  # daily decay for freshness

def _log_score(value: int) -> float:
    """Utility to convert raw count to a diminishing return score.

    Using ``log(value + 1)`` ensures that extremely large numbers do not
    dominate the final total while still rewarding higher counts.
    """
    return math.log(value + 1)

def _freshness_score(publish_timestamp: float, now_timestamp: float) -> float:
    """Score based on how recent a video is.

    ``publish_timestamp`` and ``now_timestamp`` are Unix epoch seconds.
    The score decays exponentially with the number of days since publish.
    """
    days = (now_timestamp - publish_timestamp) / 86400.0
    return math.exp(-DECAY_RATE * days)

def compute_total_score(video: dict) -> float:
    """Calculate the overall potential score for a TikTok video.

    The *video* dictionary is expected to contain the following keys:

    - ``shares_count`` (int)
    - ``saves_count`` (int)
    - ``likes_count`` (int)
    - ``comments_count`` (int)
    - ``author_followers`` (int)
    - ``publish_date`` (ISO‑8601 string, e.g. ``"2026-04-18 10:30:00"``)

    The function returns a normalized score in the range ``[0, 1]``.
    """
    now = time.time()
    try:
        pub_struct = time.strptime(video.get("publish_date", ""), "%Y-%m-%d %H:%M:%S")
        pub_ts = time.mktime(pub_struct)
    except Exception:
        pub_ts = now

    shares_score = _log_score(video.get("shares_count", 0))
    saves_score = _log_score(video.get("saves_count", 0))
    engagement_score = _log_score(video.get("likes_count", 0) + video.get("comments_count", 0))
    freshness_score = _freshness_score(pub_ts, now)
    author_score = _log_score(video.get("author_followers", 0))

    total = (
        shares_score * W_SHARES
        + saves_score * W_SAVES
        + engagement_score * W_ENGAGEMENT
        + freshness_score * W_FRESHNESS
        + author_score * W_AUTHOR
    )

max_possible = (
 _log_score(1_000_000) * W_SHARES
+ _log_score(1_000_000) * W_SAVES
+ _log_score(2_000_000) * W_ENGAGEMENT
+ 1.0 * W_FRESHNESS
+ _log_score(10_000_000) * W_AUTHOR
)
return min(total / max_possible, 1.0)

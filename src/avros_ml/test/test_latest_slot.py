# test/test_latest_slot.py
# Checks the "mailbox for one letter": the newest value wins, old ones are dropped and
# counted, and an empty mailbox times out instead of blocking forever.

from avros_ml.utils.latest_slot import LatestSlot


def test_newest_wins_and_drops_counted():
    s = LatestSlot()
    s.put(1)
    s.put(2)
    assert s.get(0.01) == 2
    assert s.dropped == 1


def test_empty_times_out():
    assert LatestSlot().get(0.01) is None

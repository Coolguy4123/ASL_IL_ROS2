# test/test_launch_dummy_graph.py
# Integration test (to be implemented): start the whole graph with dummy models and check
#   * /cmd_vel is published at ~20 Hz even with no ML input (arbiter heartbeat),
#   * killing il_node drives /cmd_vel to zero within the watchdog time,
#   * the model nodes report ready before autonomy can be enabled.
# Uses launch_testing so it can run in CI without a GPU or any hardware.

import pytest


@pytest.mark.skip(reason="TODO: implement with launch_testing once nodes are filled in")
def test_graph_with_dummy_models():
    ...

import pytest
from tests.conftest import prepare
from gcleaner.constants import Constants
from gcleaner.plugins.trash import TrashPlugin


@pytest.fixture
def setup():
    """Fixture to setup each unit test"""
    plugin = TrashPlugin()
    trash_path = f"{Constants.USERHOMEDIR}/.local/share/Trash/files/"
    prepare(trash_path)

    yield {
        "plugin": plugin
    }


def test_trash_plugin_scan(setup):
    # This test tries to validate that the trash plugin scan the
    # Trash and finds files in it.
    plugin = setup["plugin"]
    files, _ = plugin.scan()
    assert files > 0


def test_trash_plugin_clean(setup):
    # This test validates that the clean function of the trash plugin
    # deletes all files in the Trash.
    plugin = setup["plugin"]
    plugin.clean()
    import os
    for path in plugin.inventory.paths:
        assert not os.path.exists(path)

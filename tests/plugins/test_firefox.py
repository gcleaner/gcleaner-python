import pytest
from tests.conftest import prepare
from gcleaner.plugins.firefox import FirefoxPlugin


@pytest.fixture
def setup():
    """Fixture to setup each unit test"""
    plugin = FirefoxPlugin()
    profiles = plugin.get_profiles()
    cache_path = next((item for item in profiles if "release" in item), None)
    prepare(cache_path)

    yield {
        "plugin": plugin
    }


def test_firefox_plugin_scan(setup):
    # This test tries to validate that the firefox plugin scan the
    # cache directory and finds files in it.
    plugin = setup["plugin"]
    files, _ = plugin.scan()
    assert files > 0


def test_firefox_plugin_clean(setup):
    # This test validates that the clean function of the firefox plugin
    # deletes all files in the cache.
    plugin = setup["plugin"]
    plugin.clean()
    import os
    for path in plugin.inventory.paths:
        assert not os.path.exists(path)

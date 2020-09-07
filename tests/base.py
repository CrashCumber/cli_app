import pytest


class Base:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, config):
        self.client = config


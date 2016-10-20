from pytest import fixture
from test.python.shared.conftest import *
import os


@fixture(scope="module")
def proto_bundle_path():
    yield os.path.abspath("test/support/build/types-proto3.build")

from pytest import fixture
from test.python.memoize import clear_memoized_cache
from test.python.memoize import memoize
from test.python.navigator import Navigator


@fixture(params=[
    ("file-comment"),
    ("Enums (1)"),
    ("Services (1)"),
    ("Messages (2)"),
])
def file_proto_comment(request):
    yield request.param


@fixture(params=[
    ("message-comment"),
    ("message-field-comment"),
    ("message-oneof[0]-comment"),
    ("message-oneof[0]-field[0]-comment"),
    ("message-oneof[0]-field[1]-comment"),
    ("message-oneof[1]-comment"),
    ("message-oneof[1]-field[0]-comment"),
    ("message-oneof[1]-field[1]-comment"),
])
def message_proto_comment(request):
    yield request.param


@fixture(params=[
    ("nested-message-comment"),
    ("nested-message-field[0]-comment"),
    ("nested-message-oneof-comment"),
    ("nested-message-oneof-field[0]-comment"),
    ("nested-message-oneof-field[1]-comment"),
    ("nested-message-field[1]-comment"),
])
def nested_message_proto_comment(request):
    yield request.param


@fixture(params=[
    ("recursive-message-comment"),
    ("recursive-message-field-comment"),
    ("recursive-message-oneof-comment"),
    ("recursive-message-oneof-field[0]-comment"),
    ("recursive-message-oneof-field[1]-comment"),
])
def recursive_message_proto_comment(request):
    yield request.param


@fixture(params=[
    ('enum-comment'),
    ('enum-val[0]-comment'),
    ('enum-val[1]-comment'),
])
def enum_proto_comment(request):
    yield request.param


@fixture(params=[
    ('nested-enum-comment'),
    ('nested-enum-val[0]-comment'),
    ('nested-enum-val[1]-comment'),
])
def nested_enum_proto_comment(request):
    yield request.param


@fixture(params=[
    ('recursive-enum-comment'),
    ('recursive-enum-val[0]-comment'),
    ('recursive-enum-val[1]-comment'),
])
def recursive_enum_proto_comment(request):
    yield request.param


@fixture(params=[
    ("service-comment"),
    ("action-comment"),
])
def service_proto_comment(request):
    yield request.param


## Fixtures
@fixture
def navigator(server_did_boot, driver, test_host, timeout, print_debug_func):
    if server_did_boot:
        yield Navigator(driver, test_host, timeout, print_debug_func)
    else:
        print_debug_func()
        assert server_did_boot, "server did not start up"


@fixture
def types_file_url():
    yield '/#/files/example/types.proto'


@fixture
def example_message_url():
    yield '/#/messages/.example.ExampleMessage'


@fixture
def example_nested_message_url():
    yield '/#/messages/.example.ExampleNestingScope.ExampleNestedMessage'


@fixture
def example_recursive_message_url():
    yield '/#/messages/.example.ExampleNestingScope.RecursiveProvingScope.ExampleRecursiveMessage'


@fixture
def example_enum_url():
    yield '#/enums/.example.ExampleEnum'


@fixture
def example_nested_enum_url():
    yield '/#/enums/.example.ExampleNestingScope.ExampleNestedEnum'


@fixture
def example_recursive_enum_url():
    yield '/#/enums/.example.ExampleNestingScope.RecursiveProvingScope.ExampleRecursiveEnum'


@fixture
def example_service_url():
    yield '#/services/.example.ExampleService'


@fixture
@memoize
def file_proto_page(navigator, types_file_url):
    yield navigator.get_page(types_file_url)


@fixture
@memoize
def message_proto_page(navigator, example_message_url):
    yield navigator.get_page(example_message_url)


@fixture
@memoize
def nested_message_proto_page(navigator, example_nested_message_url):
    yield navigator.get_page(example_nested_message_url)


@fixture
@memoize
def recursive_message_proto_page(navigator, example_recursive_message_url):
    yield navigator.get_page(example_recursive_message_url)


@fixture
@memoize
def service_proto_page(navigator, example_service_url):
    yield navigator.get_page(example_service_url)


@fixture
@memoize
def enum_proto_page(navigator, example_enum_url):
    yield navigator.get_page(example_enum_url)


@fixture
@memoize
def nested_enum_proto_page(navigator, example_nested_enum_url):
    yield navigator.get_page(example_nested_enum_url)


@fixture
@memoize
def recursive_enum_proto_page(navigator, example_recursive_enum_url):
    yield navigator.get_page(example_recursive_enum_url)


@fixture(autouse=True, scope="module")
def clear_cache():
    clear_memoized_cache()

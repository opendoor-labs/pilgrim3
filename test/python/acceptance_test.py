from navigator import Navigator
from pytest import fixture
from pytest import mark

# Debugging Helpers
# logs = self.driver.get_log("har")
# logs = self.driver.get_log("browser")
# screenshot_loc = "log/%f.png" % time.time()
# print('error ocured while using selenium, see ' + screenshot_loc)
# self.driver.save_screenshot(screenshot_loc)


## Fixtures

@fixture
def navigator(server_did_boot, driver, test_host, timeout, print_debug_func):
    if server_did_boot:
        yield Navigator(driver, test_host, timeout, print_debug_func)
    else:
        print_debug_func()
        assert server_did_boot, "server did not start up"


memoization = {}


@fixture
def types_file_url():
    yield '/#/files/example/types.proto'


@fixture
def example_message_url():
    yield '/#/messages/example.ExampleMessage'


@fixture
def example_nested_message_url():
    yield '/#/messages/example.ExampleNestingScope.ExampleNestedMessage'


@fixture
def example_enum_url():
    yield '#/enums/example.ExampleEnum'


@fixture
def example_enum_url():
    yield '#/services/example.ExampleService'


@fixture()
def file_proto_page(navigator, types_file_url):
    if 'file_proto' not in memoization:
        memoization['file_proto'] = navigator.get_page(types_file_url)
    yield memoization['file_proto']


@fixture
def message_proto_page(navigator, example_message_url):
    if 'message_proto' not in memoization:
        memoization['message_proto'] = navigator.get_page(example_message_url)
    yield memoization['message_proto']


@fixture
def nested_message_proto_page(navigator, example_nested_message_url):
    if 'message_proto' not in memoization:
        memoization['nested_message_proto'] = navigator.get_page(example_nested_message_url)
    yield memoization['nested_message_proto']


## Tests

def test_file_comment(file_proto_page):
    assert 'file-comment' in file_proto_page


@mark.parametrize("token_type", [
    ("Enums (1)"),
    ("Services (1)"),
    ("Messages (3)"),
    ("message-oneof-field[0]-comment"),
    ("message-oneof-field[1]-comment"),
])
def test_file_links(token_type, file_proto_page):
    assert token_type in file_proto_page


@mark.parametrize("comment_string", [
    ("message-comment"),
    ("message-field-comment"),
    ("message-oneof-comment"),
    ("message-oneof-field[0]-comment"),
    ("message-oneof-field[1]-comment"),
])
def test_message_comment(comment_string, message_proto_page):
    assert comment_string in message_proto_page

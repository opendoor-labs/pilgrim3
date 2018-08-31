# Debugging Helpers
# logs = self.driver.get_log("har")
# logs = self.driver.get_log("browser")
# screenshot_loc = "log/%f.png" % time.time()
# print('error ocured while using selenium, see ' + screenshot_loc)
# self.driver.save_screenshot(screenshot_loc)

# params come from global conftest.py

def test_file_comment(file_proto_comment, file_proto_page):
    assert file_proto_comment in file_proto_page


def test_message_comment(message_proto_comment, message_proto_page):
    assert message_proto_comment in message_proto_page


def test_nested_message_comment(nested_message_proto_comment, nested_message_proto_page):
    assert nested_message_proto_comment in nested_message_proto_page


def test_recursive_message_comment(recursive_message_proto_comment, recursive_message_proto_page):
    assert recursive_message_proto_comment in recursive_message_proto_page


def test_enum_comment(enum_proto_comment, enum_proto_page):
    assert enum_proto_comment in enum_proto_page


def test_nested_enum_comment(nested_enum_proto_comment, nested_enum_proto_page):
    assert nested_enum_proto_comment in nested_enum_proto_page


def test_recursive_enum_comment(recursive_enum_proto_comment, recursive_enum_proto_page):
    assert recursive_enum_proto_comment in recursive_enum_proto_page


def test_line_comment(line_comment, line_comment_page):
    assert line_comment in line_comment_page


def test_multiline_comment(multiline_comment, multiline_comment_page):
    assert multiline_comment in multiline_comment_page


def test_service_comment(service_proto_comment, service_proto_page):
    assert service_proto_comment in service_proto_page

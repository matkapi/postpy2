"""Test core.py."""
import os
import re
import logging
import json
import pprint
import pytest
from unittest.mock import Mock, call, patch

from parameterized import parameterized

from postpy2.core import PostRequest, PostPython

logger = logging.getLogger(__name__)
nested_datafile_name = os.path.join(
    os.path.dirname(__file__),
    "testdata",
    "collections",
    "nested.postman_collection.json",
)


@parameterized.expand(
    [
        (
            "graphql_and_empty_variables",
            {
                "name": "name",
                "url": {"raw": "raw_url"},
                "body": {
                    "mode": "graphql",
                    "graphql": {
                        "query": "{\n  countries {\n    code \n    name\n  }\n}\n",
                        "variables": "",
                    },
                },
                "header": [{"key": "key", "value": "value"}],
                "method": "POST",
            },
            [
                call(
                    url="http://raw_url",
                    json={
                        "query": "{\n  countries {\n    code \n    name\n  }\n}\n",
                        "variables": "{}",
                    },
                    headers={"key": "value"},
                    method="POST",
                )
            ],
        ),
        (
            "graphql_and_empty_variables_object",
            {
                "name": "name",
                "url": {"raw": "raw_url"},
                "body": {
                    "mode": "graphql",
                    "graphql": {
                        "query": "{\n  countries {\n    code \n    name\n  }\n}\n",
                        "variables": "{}",
                    },
                },
                "header": [{"key": "key", "value": "value"}],
                "method": "POST",
            },
            [
                call(
                    url="http://raw_url",
                    json={
                        "query": "{\n  countries {\n    code \n    name\n  }\n}\n",
                        "variables": "{}",
                    },
                    headers={"key": "value"},
                    method="POST",
                )
            ],
        ),
        (
            "graphql_with_variables",
            {
                "name": "name",
                "url": {"raw": "raw_url"},
                "body": {
                    "mode": "graphql",
                    "graphql": {
                        "query": "{\n  countries {\n    code \n    name\n  }\n}\n",
                        "variables": '{ "myvar": "value" }',
                    },
                },
                "header": [{"key": "key", "value": "value"}],
                "method": "POST",
            },
            [
                call(
                    url="http://raw_url",
                    json={
                        "query": "{\n  countries {\n    code \n    name\n  }\n}\n",
                        "variables": '{ "myvar": "value" }',
                    },
                    headers={"key": "value"},
                    method="POST",
                )
            ],
        ),
    ]
)
@patch("postpy2.core.requests.request")
def test_post_request(name, data, expected_request_call, request_mock: Mock):
    """Post Request."""
    logger.info(name)
    mock_post_python = Mock()
    mock_post_python.environments = {}
    mock_post_python.request_overrides = None
    post_request = PostRequest(mock_post_python, data)
    post_request()
    for idx, expected_call in enumerate(expected_request_call):
        _, _, x_call = expected_call
        request_call = request_mock.call_args_list[idx]
        _, r_call = request_call
        if "json" in x_call:
            if "query" in x_call["json"]:
                # \t\n are removed
                x_call["json"]["query"] = re.sub(r"\s+", " ", x_call["json"]["query"])
                x_call["json"]["variables"] = json.loads(x_call["json"]["variables"])

        assert x_call == r_call


@parameterized.expand(
    [
        (
            "with_request_override",
            {"headers": {"RUNTIMEHEADER": "RUNTIMEVALUE"}},
            [
                call(
                    headers={
                        "myCollectionHeader": "MyCollectionHeaderValue",
                        "RUNTIMEHEADER": "RUNTIMEVALUE",
                    },
                    method="POST",
                    url="http://raw_url",
                )
            ],
        ),
        (
            "no_request_override",
            None,
            [
                call(
                    headers={"myCollectionHeader": "MyCollectionHeaderValue"},
                    method="POST",
                    url="http://raw_url",
                )
            ],
        ),
        (
            "with_existing_keys",
            {"headers": {"myCollectionHeader": "RUNTIMEVALUE"}},
            [
                call(
                    headers={"myCollectionHeader": "RUNTIMEVALUE"},
                    method="POST",
                    url="http://raw_url",
                )
            ],
        ),
    ]
)
@patch("postpy2.core.requests.request")
def test_request_overrides(name: str, request_overrides, expected_request, mock_requests: Mock):
    """Verify request overrides."""
    mock_post_python = Mock()
    mock_post_python.request_overrides = request_overrides
    mock_post_python.environments = {}

    data = {
        "name": name,
        "url": {"raw": "raw_url"},
        "method": "POST",
        "header": [{"key": "myCollectionHeader", "value": "MyCollectionHeaderValue"}],
    }
    post_request = PostRequest(mock_post_python, data)
    post_request()

    assert mock_requests.call_args_list == expected_request


def test_walk_folders():
    """Verify that we find all the requests by folder."""
    expected = {
        "Root": ["root_test"],
        "Folder": ["test1", "test2", "test_file", "graphql"],
        "Folder2": ["test_file_3"],
        "Folder3": ["test_file_5"],
        "SubFolder1": ["test_file_2"],
        "SubFolder2": ["test_file_4"],
        "SubSubFolder1": ["test_file_6"],
    }
    found = {}
    # requests = []
    things = PostPython(nested_datafile_name)
    for folder in things.walk():
        logger.info("Folder: %s (%s)", folder.name, type(folder))
        for request_item in folder.walk():
            logger.info("%s/%s", folder.name, request_item.name)
            if folder.name not in found:
                found[folder.name] = []
            found[folder.name].append(request_item.name)
    for key, value in expected.items():
        assert value == found[key]
    logger.info(pprint.pformat(found))
    assert len(found) == 7
    assert expected == found


def test_help(capfd):
    """test help."""
    expected = """Possible methods:
post_python.Root.root_test()
post_python.Folder.test1()
post_python.Folder.test2()
post_python.Folder.test_file()
post_python.Folder.graphql()
post_python.Folder2.test_file_3()
post_python.SubFolder1.test_file_2()
post_python.Folder3.test_file_5()
post_python.SubFolder2.test_file_4()
post_python.SubSubFolder1.test_file_6()
"""
    things = PostPython(nested_datafile_name)
    things.help()
    out, _ = capfd.readouterr()
    assert out == expected


def test_attr_error_no_folder():
    """verify that when we call an invalid request, we get an exception."""
    with pytest.raises(AttributeError) as err:
        things = PostPython(nested_datafile_name)
        things.always_gunna_break()
        assert "folder does not exist in Postman collection" in err.message


def test_attr_error_no_folder_match():
    """verify that when we call an invalid request, we get an exception."""
    with pytest.raises(AttributeError) as err:
        things = PostPython(nested_datafile_name)
        things.SubFold()
        assert "folder does not exist in Postman collection" in err.message
        assert "Did you mean" in err.message


def test_attr_error_no_request():
    """verify that when we call an invalid request, we get an exception."""
    with pytest.raises(AttributeError) as err:
        things = PostPython(nested_datafile_name)
        things.Folder.always_gunna_break_1232345()
        assert "request does not exist in Postman collection" in err.message


def test_attr_error_no_request_match():
    """verify that when we call an invalid request, we get an exception."""
    with pytest.raises(AttributeError) as err:
        things = PostPython(nested_datafile_name)
        things.Folder.test()
        assert "request does not exist in Postman collection" in err.message
        assert "Did you mean" in err.message


def test_handle_auth_bearer():
    """Verify that we can handle a bearer auth."""
    things = PostPython(nested_datafile_name)
    for folder in things.walk():
        for request_item in folder.walk():
            formatted_kwargs = {
                "url": "https://testy_url.co",
                "json": {
                    "query": "{\n  countries {\n    code \n    name\n  }\n}\n",
                    "variables": {"keyword": "test"},
                },
                "headers": {},
                "method": "POST",
            }
            new_env = {"bearer_token": "testing123"}
            ret = request_item._handle_auth(formatted_kwargs, new_env)  # pylint: disable=W0212
            assert ret
            assert "Authorization" in ret["headers"]
            assert ret["headers"]["Authorization"] == f"Bearer {new_env['bearer_token']}"
            break
        break

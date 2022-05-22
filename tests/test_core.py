from unittest.mock import Mock, call, patch

from parameterized import parameterized

from postpy2.core import PostRequest


@parameterized.expand([
    (
        'graphql_and_empty_variables',
        {
            'name': 'name',
            'url': {'raw': 'raw_url'},
            'body': {
                'mode': 'graphql',
                'graphql': {
                    'query': "{\n  countries {\n    code \n    name\n  }\n}\n",
                    'variables': ""
                },
            },
            'header': [{'key': 'key', 'value': 'value'}],
            'method': 'POST'
        },
        [call(
            url='raw_url',
            json={
                'query': '{\n  countries {\n    code \n    name\n  }\n}\n', 'variables': '{}'
            },
            headers={'key': 'value'},
            method='POST')]
    ),
    (
        'graphql_and_empty_variables_object',
        {
            'name': 'name',
            'url': {'raw': 'raw_url'},
            'body': {
                'mode': 'graphql',
                'graphql': {
                    'query': "{\n  countries {\n    code \n    name\n  }\n}\n",
                    'variables': "{}"
                },
            },
            'header': [{'key': 'key', 'value': 'value'}],
            'method': 'POST'
        },
        [call(
            url='raw_url',
            json={
                'query': '{\n  countries {\n    code \n    name\n  }\n}\n', 'variables': '{}'
            },
            headers={'key': 'value'},
            method='POST')]
    ),
    (
        'graphql_with_variables',
        {
            'name': 'name',
            'url': {'raw': 'raw_url'},
            'body': {
                'mode': 'graphql',
                'graphql': {
                    'query': "{\n  countries {\n    code \n    name\n  }\n}\n",
                    'variables': "{ 'myvar': 'value' }"
                },
            },
            'header': [{'key': 'key', 'value': 'value'}],
            'method': 'POST'
        },
        [call(
            url='raw_url',
            json={
                'query': "{\n  countries {\n    code \n    name\n  }\n}\n", 'variables': "{ 'myvar': 'value' }"
            },
            headers={'key': 'value'},
            method='POST')]
    ),
])
@patch('postpy2.core.requests.request')
def test_PostRequest(name, data, expected_request_call, request_mock: Mock):

    mock_post_python = Mock()
    mock_post_python.environments = {}
    post_request = PostRequest(mock_post_python, data)
    post_request()

    assert expected_request_call == request_mock.call_args_list

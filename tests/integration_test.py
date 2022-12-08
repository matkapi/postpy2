import logging
import os
import sys
from typing import Dict

# Integration Tests are invoked from the Root of the Repository
sys.path.append(os.path.abspath("."))
print(sys.path)

from postpy2.core import PostPython  # noqa

logging.basicConfig(format=logging.BASIC_FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

cases: Dict[str, Dict[str, str]] = {
    "test1": {
        "func": lambda pp: pp.Folder.test1,
        "collection": "tests/testdata/collections/tests.postman_collection.json",
        "environment": "tests/testdata/environments/test.postman_environment.json",
        "environment_overrides": {"server_url": "https://httpbin.org"},
        "request_overrides": {},
    },
    "test2": {
        "func": lambda pp: pp.Folder.test2,
        "collection": "tests/testdata/collections/tests.postman_collection.json",
        "environment": "tests/testdata/environments/test.postman_environment.json",
        "environment_overrides": {"server_url": "https://httpbin.org"},
        "request_overrides": {},
    },
    "test_file": {
        "func": lambda pp: pp.Folder.test_file,
        "collection": "tests/testdata/collections/tests.postman_collection.json",
        "environment": "tests/testdata/environments/test.postman_environment.json",
        "environment_overrides": {"server_url": "https://httpbin.org"},
        "request_overrides": {},
        "data": [{"key": "title", "value": "bar"}, {"key": "body", "value": "foo"}],
        "files": [{"key": "two", "src": "tests/testdata/assets/2.png"}],
    },
    "test2_json": {
        "func": lambda pp: pp.Folder.test2,
        "collection": "tests/testdata/collections/tests.postman_collection.json",
        "environment": "tests/testdata/environments/test.postman_environment.json",
        "environment_overrides": {"server_url": "https://httpbin.org"},
        "request_overrides": {},
        "json": {"title": "bar", "body": "foo", "userId": 1},
    },
    "graphql": {
        "func": lambda pp: pp.Folder.graphql,
        "collection": "tests/testdata/collections/tests.postman_collection.json",
        "environment": "tests/testdata/environments/test.postman_environment.json",
        "environment_overrides": {"server_url": "https://httpbin.org"},
        "request_overrides": {},
    },
}

for name in cases.keys():
    logger.info("Running Test: " + name)
    current_case = cases[name]
    logger.debug(current_case)

    pp = PostPython(current_case["collection"], current_case["request_overrides"])
    pp.environments.load(current_case["environment"])
    pp.environments.update(current_case["environment_overrides"])

    if "data" in current_case:
        current_case["func"](pp).set_data(current_case["data"])

    if "files" in current_case:
        current_case["func"](pp).set_files(current_case["files"])

    if "json" in current_case:
        current_case["func"](pp).set_json(current_case["json"])

    response = current_case["func"](pp)()
    assert response.status_code == 200
    logger.info("OK")

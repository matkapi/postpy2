"""Extractor tests."""
import pytest
from postpy2 import extractors


def test_format_object_missing_variable_does_not_throw():
    """verify that we do not throw an exception when the variable is missing from the string."""
    assert extractors.format_object(obj="{{thiswillerr}}", key_values={"tmp": 1}, is_graphql=False)


def test_format_object_int_variable_does_not_throw():
    """verify that we throw an exception when the variable is missing."""
    assert extractors.format_object(obj="thiswillnoterr", key_values={"tmp": 1}, is_graphql=False)


def test_format_object_with_list():
    """verify that we handle a list object."""
    ret = extractors.format_object(
        obj=["thiswillnoterr", "neitherwillthis"],
        key_values={"tmp": 1},
        is_graphql=False,
    )
    assert ret == ["thiswillnoterr", "neitherwillthis"]


def test_format_object_unknown_throws():
    """verify that we throw an exception when the variable is missing."""
    with pytest.raises(Exception):
        assert extractors.format_object(obj=tuple(), key_values={"tmp": 1}, is_graphql=False)

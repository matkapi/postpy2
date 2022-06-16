"""postpy2 extractors."""
import logging
import json
import ntpath
import os
from io import BytesIO

import magic

logger = logging.getLogger(__name__)


def extract_dict_from_raw_mode_data(raw):
    """extract json to dictionay

    :param raw: jsondata
    :return: :extracted dict
    """
    try:
        return json.loads(raw)
    except json.decoder.JSONDecodeError:
        return {}


def exctact_dict_from_files(data):
    """extract files from dict data.

    :param data: [{"key":"filename", "src":"relative/absolute path to file"}]
    :return: :tuple of file metadata for requests library
    """
    if not os.path.isfile(data["src"]):
        raise Exception("File " + data["src"] + " does not exists")
    mime = magic.Magic(mime=True)
    file_mime = mime.from_file(data["src"])
    file_name = ntpath.basename(data["src"])
    with open(data["src"], "rb") as file_source:
        bytes_source = BytesIO(file_source.read())  # read bytes from file into memory
    return (
        file_name,
        bytes_source,
        file_mime,
        {
            "Content-Disposition": 'form-data; name="' + data["key"] + '"; filename="' + file_name + '"',
            "Content-Type": file_mime,
        },
    )


def extract_dict_from_formdata_mode_data(formdata):
    """Extract dict from formdata mode data."""
    data = {}
    files = {}
    try:
        for row in formdata:
            if row["type"] == "text":
                data[row["key"]] = row["value"]
            if row["type"] == "file":
                files[row["key"]] = exctact_dict_from_files(row)
        return data, files
    except Exception as err:  # pylint: disable=W0703
        logger.info("extact from formdata_mode_data error occurred: %s", err)
        return data, files


def extract_dict_from_headers(data):
    """Extract dict from headers."""
    ret_data = {}
    for header in data:
        try:
            if "disabled" in header and header["disabled"] is True:
                continue
            ret_data[header["key"]] = header["value"]
        except ValueError:
            continue

    return ret_data


def format_object(obj, key_values, is_graphql=False):
    """Format object with variables."""
    logger.debug(
        "format_object (%s) %s - is_graphql: %s\nvariables: %s",
        type(obj),
        obj,
        is_graphql,
        key_values.keys(),
    )
    if isinstance(obj, str):
        if is_graphql:
            return obj
        # fixes 'JSON body parsing issue with environment variable replacement #9'
        for key, value in key_values.items():
            logger.debug(key)
            obj = obj.replace(f"{{{{{key}}}}}", str(value))
        logger.debug("formatted object: %s", obj)
        return obj

    if isinstance(obj, dict):
        return format_dict(obj, key_values, is_graphql)

    if isinstance(obj, list):
        return [format_object(oobj, key_values, is_graphql) for oobj in obj]

    logger.warning("Unhandled object of type %s", type(obj))
    return obj


def format_dict(data, key_values, is_graphql):
    """Format dict with variables."""
    kwargs = {}
    for key, value in data.items():
        logger.debug("format '%s' - is_graphql: %s", key, is_graphql)
        kwargs[key] = format_object(
            value,
            key_values,
            is_graphql=(is_graphql and key in ["body", "json", "query", "data"]),
        )
    return kwargs

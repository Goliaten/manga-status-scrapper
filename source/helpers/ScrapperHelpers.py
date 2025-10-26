from typing import Any, Literal, Tuple
import requests
from http import HTTPStatus


def get_html_from_url(
    url: str,
) -> Tuple[bytes | Any, Literal[True], str] | Tuple[bytes | Any, Literal[False], None]:
    """
    Retrieve the raw response content for a given URL.

    Parameters
    ----------
    url : str
        URL to request.

    Returns
    -------
    tuple
        A 3-tuple (data, is_error, error_msg):
        - data (bytes | Any): Response content on success; empty string on HTTP error.
        - is_error (bool): True if an HTTP error occurred (status code >= 400), False otherwise.
        - error_msg (str | None): Error message when is_error is True (e.g. "Error: 404"); None on success.

    Notes
    -----
    - The function prints HTTP errors and returns an empty data value with an error message instead of raising.
    - Network-related exceptions raised by requests (e.g. ConnectionError, Timeout) are not caught and will propagate.
    """
    req_data = requests.get(url)

    if int(req_data.status_code / 100) >= 4:
        error = f"Error: {req_data.status_code}"
        print(error)
        return ("", True, error)
        # raise Exception

    return (req_data.content, False, None)

from enum import Enum
from typing import Optional, List, Dict, Any, Union

import requests

from .exceptions import NoResponseException, ThrottledResponseException
from .headers import RequestHeaders

_CLIENT_THROTTLED_RESPONSE: str = 'You are making requests too quickly.'


def _follow_pagination(url: Optional[str], items_left: Optional[int]) -> List[Dict[str, Any]]:
	if url is None or items_left is not None and items_left <= 0:
		return list()

	response: requests.Response = requests.get(url, headers=RequestHeaders.get_headers())
	parsed_response: Dict[str, Any] = response.json()

	return _complete_pagination(parsed_response, items_left)


def _complete_pagination(response: Dict[str, Any], result_limit: Optional[int]) -> List[Dict[str, Any]]:
	try:
		results: List[Dict[str, Any]] = response['results']
	except KeyError:
		message: Optional[str] = response.get('message')
		if message is None:
			raise NoResponseException("Complete server response was ({})".format(response))

		if message == _CLIENT_THROTTLED_RESPONSE:
			raise ThrottledResponseException()
		raise NoResponseException("Server message was: {}".format(message))

	if result_limit is not None:
		result_limit -= len(results)

	maybe_next: Optional[str] = response.get('pagination').get('urls', {}).get('next')
	return results + _follow_pagination(maybe_next, result_limit)




from typing import Optional, List, Dict, Any

import requests

from api.headers import RequestHeaders


def _follow_pagination(url: Optional[str], items_left: Optional[int]) -> List[Dict[str, Any]]:
	if url is None or items_left is not None and items_left <= 0:
		return list()

	response: requests.Response = requests.get(url, headers=RequestHeaders.get_headers())
	parsed_response: Dict[str, Any] = response.json()

	return _complete_pagination(parsed_response, items_left)


def _complete_pagination(response: Dict[str, Any], result_limit: Optional[int]) -> List[Dict[str, Any]]:
	results: List[Dict[str, Any]] = response['results']
	if result_limit is not None:
		result_limit -= len(results)

	maybe_next: Optional[str] = response.get('pagination').get('urls', {}).get('next')
	return results + _follow_pagination(maybe_next, result_limit)

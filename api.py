from typing import Dict, Any, List, Optional
from urllib.parse import urljoin

import requests


class RequestHeaders:
	_USER_AGENT_HEADER_FIELD: str = 'User-Agent'
	_APP_NAME: str = 'discogs_renamer'
	_APP_VERSION: str = '0.1'
	_USER_AGENT_VALUE: str = '{}/{}'.format(_APP_NAME, _APP_VERSION)

	_AUTHORIZATION_HEADER_FIELD: str = 'Authorization'
	_AUTH_KEY: str = 'xNnMbGxMhgafZvWPYUfM'
	_AUTH_SECRET: str = 'hkTIktzVZqjNgDOQYeUpNLGCiiTWiGuX'
	_AUTHORIZATION_VALUE: str = 'Discogs key={}, secret={}'.format(_AUTH_KEY, _AUTH_SECRET)

	_BASE_HEADERS: Dict[str, str] = {
		_USER_AGENT_HEADER_FIELD: _USER_AGENT_VALUE,
		_AUTHORIZATION_HEADER_FIELD: _AUTHORIZATION_VALUE
	}

	@classmethod
	def get_headers(cls) -> Dict[str, str]:
		return cls._BASE_HEADERS


_BASE_API_URL: str = 'https://api.discogs.com/'

_ENDPOINT_SEARCH_DB: str = 'database/search'

_SEARCH_QUERY: str = 'q'


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


def search_db(search_term: str, result_limit: Optional[int] = None) -> List[Dict[str, Any]]:
	full_url: str = urljoin(_BASE_API_URL, _ENDPOINT_SEARCH_DB)

	params: Dict[str, Any] = {
		_SEARCH_QUERY: search_term
	}
	response: requests.Response = requests.get(
		full_url,
		headers=RequestHeaders.get_headers(),
		params=params
	)

	parsed_response: Dict[str, Any] = response.json()

	return _complete_pagination(parsed_response, result_limit)


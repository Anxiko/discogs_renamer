from typing import Optional, List, Dict, Any
from urllib.parse import urljoin

import requests

from .headers import RequestHeaders
from .tools import _complete_pagination


class Api:
	_BASE_API_URL: str = 'https://api.discogs.com/'
	_ENDPOINT_SEARCH_DB: str = 'database/search'
	_SEARCH_QUERY_FIELD: str = 'q'

	@classmethod
	def search_db(cls, search_term: str, result_limit: Optional[int] = None) -> List[Dict[str, Any]]:
		full_url: str = urljoin(cls._BASE_API_URL, cls._ENDPOINT_SEARCH_DB)

		params: Dict[str, Any] = {
			cls._SEARCH_QUERY_FIELD: search_term
		}
		response: requests.Response = requests.get(
			full_url,
			headers=RequestHeaders.get_headers(),
			params=params
		)

		parsed_response: Dict[str, Any] = response.json()

		return _complete_pagination(parsed_response, result_limit)

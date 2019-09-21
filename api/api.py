import sys
from enum import Enum
from time import sleep
from typing import Optional, List, Dict, Any, Union
from urllib.parse import urljoin

import requests

from .cleaner import Cleaner
from .exceptions import ThrottledResponseException
from .headers import RequestHeaders
from .tools import _complete_pagination


class SearchType(Enum):
	RELEASE: str = 'release'
	MASTER: str = 'master'
	ARTIST: str = 'artist'
	LABEL: str = 'label'


class EntryField(Enum):
	TITLE: str = 'title'


class Api:
	_BASE_API_URL: str = 'https://api.discogs.com/'
	_ENDPOINT_SEARCH_DB: str = 'database/search'
	_SEARCH_TERM_FIELD: str = 'q'
	_SEARCH_TYPE_FIELD: str = 'type'

	@classmethod
	def search_db(
			cls,
			search_term: str, search_type: Optional[SearchType] = None,

			result_limit: Optional[int] = None, retries: int = 2, wait_seconds_before_retry: int = 10
	) -> List[Dict[str, Any]]:
		full_url: str = urljoin(cls._BASE_API_URL, cls._ENDPOINT_SEARCH_DB)

		params: Dict[str, Any] = {
			cls._SEARCH_TERM_FIELD: search_term
		}

		if search_type is not None:
			params[cls._SEARCH_TYPE_FIELD] = search_type.value

		total_attempts: int = 0

		while True:
			try:
				response: requests.Response = requests.get(
					full_url,
					headers=RequestHeaders.get_headers(),
					params=params
				)

				parsed_response: Dict[str, Any] = response.json()

				return _complete_pagination(parsed_response, result_limit)
			except ThrottledResponseException as e:
				print("Attempt {} out of {} failed".format(total_attempts + 1, retries + 1), file=sys.stderr)
				if total_attempts < retries:
					print("Waiting {} seconds before next attempt...".format(wait_seconds_before_retry))
					sleep(wait_seconds_before_retry)

					total_attempts += 1
					print("Retrying, attempt {}...".format(total_attempts + 1))
				else:
					print("Out of attempts, aborting", file=sys.stderr)
					raise e

	@staticmethod
	def filter_results_by(
			expected: str, results: List[Dict[str, Any]], field_name: Union[EntryField, str]
	) -> List[Dict[str, Any]]:
		if type(field_name) is EntryField:
			field_name: str = field_name.value

		normalized_expected: str = Cleaner.normalize_string(expected)
		return list(filter(
			lambda e: Cleaner.normalize_string(e.get(field_name, '')) == normalized_expected,
			results
		))

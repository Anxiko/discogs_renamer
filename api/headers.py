from typing import Dict


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

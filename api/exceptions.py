class NoResponseException(Exception):
	pass


class ThrottledResponseException(NoResponseException):
	def __init__(self):
		super().__init__("API rejected request because the client is making them too quickly")

import re
from typing import Pattern, Match


class Cleaner:
	_LABEL_CLEANER_PATTERN: Pattern = re.compile(r'(.+)\(.*\)\s*')

	@classmethod
	def label_cleaner(cls, raw_label: str) -> str:
		match: Match = cls._LABEL_CLEANER_PATTERN.match(raw_label)
		if match is None:
			return raw_label

		cleaned_label: str = match.group(1).strip()
		if len(cleaned_label) == 0:
			return raw_label
		return cleaned_label

	@staticmethod
	def normalize_string(raw_string: str) -> str:
		return raw_string.strip().lower()

import json
import os
import sys
from pathlib import Path
from typing import Dict, Union, List, Type, Any

from api import Api, SearchType, Cleaner, EntryField

StructureType: Type = Dict[str, Union[Dict, List]]


class StructureReplicator:
	_STRUCTURE_FILENAME: str = 'structure.json'

	@classmethod
	def _fill_folder(cls, path: str) -> StructureType:
		_, folders, files = next(os.walk(path), (path, [], []))
		rv: StructureType = {".": files}

		for folder in folders:
			rv[folder] = cls._fill_folder(os.path.join(path, folder))

		return rv

	@classmethod
	def extract_folder_structure(cls) -> StructureType:
		return cls._fill_folder('.')

	@classmethod
	def save_folder_structure(cls, d: StructureType, pretty: bool = False) -> None:
		with open(cls._STRUCTURE_FILENAME, mode='w', encoding='utf-8') as f:
			json.dump(d, f, indent=1 if pretty else None)

	@classmethod
	def _deflate_folder(cls, path: str, contents: StructureType) -> None:
		os.makedirs(path, exist_ok=True)

		files: List[str] = contents.get('.', [])
		for file in files:
			file_path: str = os.path.join(path, file)
			Path(file_path).touch(exist_ok=True)

		for folder, folder_contents in contents.items():
			if folder == '.':
				continue
			full_folder_path: str = os.path.join(path, folder)
			cls._deflate_folder(full_folder_path, folder_contents)

	@classmethod
	def expand_folder_structure(cls, structure: StructureType, target: str = None) -> None:
		if target is None:
			target = '.'

		cls._deflate_folder(target, structure)

	@classmethod
	def read_structure(cls) -> StructureType:
		with open(cls._STRUCTURE_FILENAME, encoding='utf-8') as f:
			structure: StructureType = json.load(f)

		return structure


def main() -> None:
	structure: StructureType = StructureReplicator.read_structure()

	labels: List[str] = list(filter(lambda lbl: lbl != '.', structure.keys()))

	for label in labels:
		print("{}...".format(label))
		cleaned_label: str = Cleaner.label_cleaner(label)
		unfiltered_results: List[Dict[str, Any]] = Api.search_db(
			search_term=cleaned_label, search_type=SearchType.LABEL, result_limit=50)

		results = Api.filter_results_by(cleaned_label, unfiltered_results, EntryField.TITLE)

		if len(results) == 1:
			continue
		print(
			"FILTERED:", "{} [{}]".format(cleaned_label, label), "=>", "[{}] ({})".format(len(results), results),
			file=sys.stderr)
		print(
			"UNFILTERED:", "{} [{}]".format(cleaned_label, label), "=>", "[{}] ({})".format(len(results), results),
			file=sys.stderr)


if __name__ == '__main__':
	main()

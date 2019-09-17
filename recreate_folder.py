import json
import os
from pathlib import Path
from typing import Dict, Union, List, Type

_STRUCTURE_FILENAME: str = 'structure.json'

StructureType: Type = Dict[str, Union[Dict, List]]


def _fill_folder(path: str) -> StructureType:
	_, folders, files = next(os.walk(path), (path, [], []))
	rv: StructureType = {".": files}

	for folder in folders:
		rv[folder] = _fill_folder(os.path.join(path, folder))

	return rv


def extract_folder_structure() -> StructureType:
	return _fill_folder('.')


def save_folder_structure(d: StructureType, pretty: bool = False) -> None:
	with open(_STRUCTURE_FILENAME, mode='w', encoding='utf-8') as f:
		json.dump(d, f, indent=1 if pretty else None)


def _deflate_folder(path: str, contents: StructureType) -> None:
	os.makedirs(path, exist_ok=True)

	files: List[str] = contents.get('.', [])
	for file in files:
		file_path: str = os.path.join(path, file)
		Path(file_path).touch(exist_ok=True)

	for folder, folder_contents in contents.items():
		if folder == '.':
			continue
		full_folder_path: str = os.path.join(path, folder)
		_deflate_folder(full_folder_path, folder_contents)


def expand_folder_structure(structure: StructureType, target: str = None) -> None:
	if target is None:
		target = '.'

	_deflate_folder(target, structure)


def read_structure() -> StructureType:
	with open(_STRUCTURE_FILENAME, encoding='utf-8') as f:
		structure: StructureType = json.load(f)

	return structure


if __name__ == '__main__':
	expand_folder_structure(read_structure(), target='./test')

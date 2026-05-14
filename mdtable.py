import logging
from pathlib import Path
from typing import NamedTuple

from settings import settings

logging.getLogger(__name__)


def _is_dict_ordered() -> bool:
	"""
	This function is implemented by checking current Python version.

	From Python 3.7, the built-in datatype `dict` will maintain the order of value.
	"""
	import sys

	return sys.version_info.major >= 3 and sys.version_info.minor >= 7


class MDTable:
	def __init__(self, md_table: str | list[str]):
		# Check whether the Python dict maintain order.
		# TODO: Add a OrderedDict version for lower Python version.
		if not _is_dict_ordered():
			logging.error('Current python version does not support maintain order in dict.')
			raise SystemError('Python version is too low for the current program')

		# Preprocess the source table.
		if not isinstance(md_table, list):
			md_table = md_table.split('\n')  # Split table into lines for iteration.

		def process_unit(unit: str) -> str:
			"""Process a single unit with the format specified by settings."""
			unit = unit.strip()
			if settings['extract_number_in_latex']:
				import re
				unit = re.sub(r'\$(-?[\d,]+\.?\d*)[^$]*\$', r'\1', unit)
			if settings['replace_comma_with_semicolon']:
				unit = unit.replace(',', ';')
			if settings['use_quote_for_each_unit']:
				unit = '"' + unit + '"'
			return unit

		# Process the title line and create table.
		self.header_row = tuple(process_unit(key) for key in md_table[0].split('|')[1:][:-1])
		self._column_number, self._row_number = len(self.header_row), len(md_table) - 2
		self.table: dict[str, list[str]] = {self.header_row[i]: list() for i in range(self._column_number)}

		# Process the entire part of table.
		for raw_row in md_table[2:]:
			row = tuple(process_unit(unit) for unit in raw_row.split('|')[1:][:-1])
			for i in range(self._column_number):
				self.table[self.header_row[i]].append(row[i])

	def __repr__(self) -> str:
		return f'<Markdown Table with {self._column_number} columns and {self._row_number} rows>'

	_MDTableSize = NamedTuple('_MDTableSize', [('column', int), ('row', int)])

	def size(self) -> NamedTuple:
		"""
		:return: A NamedTuple with attributes `column` and `row` to present the size of table.
		"""
		return self._MDTableSize(self._column_number, self._row_number)

	def export_to_csv(self, filepath: str | Path, /, overwrite: bool = False):
		"""
		Export the table to a CSV file.

		:param filepath: The file path to store CSV file.
		:param overwrite: If the file given already exist, overwrite it instead of adding appendix to filename.
		"""
		if not isinstance(filepath, Path):
			filepath = Path(filepath)

		with open(filepath, 'x' if not overwrite else 'w') as file:
			file.write(', '.join(self.header_row) + '\n')
			for row in range(self._row_number):
				file.write(', '.join(self.table[column][row] for column in self.header_row) + '\n')

		if not overwrite:
			logging.info(f'Stored table to CSV file: {filepath}.')
		else:
			logging.warning(f'Overwrite existed CSV file: {filepath}')

import logging

from mdtable import MDTable

logging.getLogger(__name__)


def set_log_config():
	log_format = '%(asctime)s : %(levelname)s : %(name)s' + '\n' + '%(message)s'
	logging.basicConfig(filename='logs.log', format=log_format, level=logging.INFO)


def parse_args():
	from argparse import ArgumentParser

	parser = ArgumentParser(prog='MDTableExtractor', description='Extract table in markdown format.')
	parser.add_argument('sourcefile', help='Origin markdown file which contains a table only.')
	parser.add_argument('-E', '--export', metavar='CSVFileName', help='Export table to the specific CSV file.')

	args = parser.parse_args()
	return args


def main():
	set_log_config()
	args = parse_args()

	from pathlib import Path

	if not Path(args.sourcefile).exists():
		logging.error(f'Source file does not exist: {Path(args.sourcefile)}.')
		raise FileNotFoundError(f'File not exists: {Path(args.sourcefile)}')

	with open(Path(args.sourcefile), 'r') as file:
		table = MDTable(file.readlines())
		logging.info(f'Read the table from file: {table}.')
	if args.export is not None:
		try:
			table.export_to_csv(Path(args.export))
		except FileExistsError:
			logging.warning(f'File {args.export} already exists. Ask user whether to overwrite.')
			overwrite = input(f"File {args.export} already exists. Enter 'y' to overwrite: ")
			logging.debug(f'Receive the answer from user: {overwrite}.')
			if overwrite.strip().lower() == 'y':
				table.export_to_csv(Path(args.export), overwrite=True)


if __name__ == '__main__':
	main()

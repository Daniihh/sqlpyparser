from . import SQLStatement
from .expressions import TableExpression
from .identifier import database_name_syntax, identifier_syntax
from .data_types import DataLiteral
from typing import Dict, List
from pyparsing import CaselessKeyword, Group, ParseResults, Suppress, \
	delimitedList

class InsertStatement(SQLStatement):
	statement_type = "INSERT"
	parse_expression = \
		CaselessKeyword("INSERT").setResultsName("statement_type") + \
		CaselessKeyword("INTO") + \
		database_name_syntax.setResultsName("database_name") + \
		identifier_syntax.setResultsName("table_name") + \
		Suppress("(") + \
		delimitedList(
			identifier_syntax
		).setResultsName("columns") + \
		Suppress(")") + \
		CaselessKeyword("VALUES") + \
		Suppress("(") + \
		Group(
			delimitedList(
				Group(DataLiteral.parse_expression)
			).setResultsName("values")
		).setResultsName("rows", listAllMatches=True) + \
		Suppress(")")

	def __init_from_args__(self):
		pass

	def __init_from_results__(self, results: ParseResults):
		rows = results.get("rows")
		columns = results.get("columns")
		columns_len = len(columns)

		if not all(len(row) == columns_len for row in rows):
			raise IndexError("All rows aren't same length as chosen columns.")

		self.parse_results = results
		self.table = TableExpression(results)
		self.rows: List[Dict[str, DataLiteral]] = [
			{key: DataLiteral(value) for key, value in zip(columns, row)}
				for row in rows
		]

	def __str__(self):
		return "INSERT INTO {} ({}) VALUES({})".format(
			self.table,
			", ".join(self.rows[0].keys()),
			", ".join(map(str, self.rows[0].values()))
		)

target = [InsertStatement]

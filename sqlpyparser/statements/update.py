from sqlpyparser.statements.expressions import TableExpression
from . import SQLExpression, SQLStatement
from .data_types import DataLiteral
from .identifier import identifier_syntax
from pyparsing import CaselessKeyword, CaselessLiteral, Group, \
	ParseExpression, delimitedList

class WhereCaluse(SQLExpression):
	parse_expression = \
		CaselessKeyword("WHERE") + \
		Group(
			delimitedList(
				identifier_syntax.setResultsName("name") +
				CaselessLiteral("=") +
				Group(DataLiteral.parse_expression).setResultsName("data")
			)
		).setResultsName("conditions", listAllMatches=True)

	def __init_from_args__(self):
		pass

	def __init_from_results__(self, results: ParseExpression):
		self.parse_results = results
		self.conditions = {
			condition.get("name"): DataLiteral(condition.get("data"))
				for condition in results.get("conditions")
		}

class UpdateStatement(SQLStatement):
	statement_type = "UPDATE"
	parse_expression = \
		CaselessKeyword("UPDATE").setResultsName("statement_type") + \
		TableExpression.parse_expression.setResultsName("table") + \
		CaselessKeyword("SET") + \
		Group(
			delimitedList(
				identifier_syntax.setResultsName("name") +
				CaselessLiteral("=") +
				Group(DataLiteral.parse_expression).setResultsName("data")
			)
		).setResultsName("updates", listAllMatches=True) + \
		Group(WhereCaluse.parse_expression).setResultsName("where")

	def __init_from_args__(self):
		pass

	def __init_from_results__(self, results: ParseExpression):
		self.parse_results = results
		self.table = TableExpression(results.get("table"))
		self.updates = {
			update.get("name"): DataLiteral(update.get("data"))
				for update in results.get("updates")
		}
		self.where = WhereCaluse(results.get("where"))

target = [UpdateStatement]

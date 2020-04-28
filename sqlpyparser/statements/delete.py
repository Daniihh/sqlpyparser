from . import SQLStatement
from .update import WhereCaluse
from .expressions import TableExpression
from pyparsing import CaselessKeyword, Group, ParseExpression

class DeleteStatement(SQLStatement):
	statement_type = "DELETE"
	parse_expression = \
		CaselessKeyword("DELETE").setResultsName("statement_type") + \
		CaselessKeyword("FROM") + \
		TableExpression.parse_expression.setResultsName("table") + \
		Group(WhereCaluse.parse_expression).setResultsName("where")

	def __init_from_args__(self):
		pass

	def __init_from_results__(self, results: ParseExpression):
		self.parse_results = results
		self.table = TableExpression(results.get("table"))
		self.where = WhereCaluse(results.get("where"))

target = [DeleteStatement]

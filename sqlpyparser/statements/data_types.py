from typing import Any
from pyparsing import CaselessKeyword, Or, ParseResults, QuotedString
from . import SQLExpression

def add_key_value(key: str, value: Any):
	def set_parse_action(toks: ParseResults):
		toks[key] = value
	return set_parse_action

class DataTypeName(str):
	def __new__(cls, value: str, argument: Any):
		return str.__new__(cls, value) # type: ignore

	def __init__(self, value: str, argument: Any):
		self._secondary_argument = None if argument is None else str(argument)

	def __getitem__(self, thing: int):
		value = {0: str(self), 1: self._secondary_argument}[thing]
		if value is None:
			raise AttributeError()
		return value

class DataType(SQLExpression):
	parse_expression = Or((
		CaselessKeyword("BOOL"), # For now this is fine.
		CaselessKeyword("TEXT"),
		CaselessKeyword("INT")
	)).setResultsName("type_name")

	def __init_from_args__(self):
		pass

	def __init_from_results__(self, results: ParseResults):
		self.parse_results = results
		self.type_name: str = results.get("type_name")

class DataLiteral(SQLExpression):
	parse_expression = (
		(
			CaselessKeyword("TRUE") ^
			CaselessKeyword("FALSE")
		).setParseAction(add_key_value("type", "boolean")) ^
		QuotedString('"')
			.setParseAction(add_key_value("type", "string"))
	).setResultsName("value")

	type: str
	value: Any

	def __init_from_args__(self, type: str, value: Any):
		self.type = type
		self.value = value

	def __init_from_results__(self, results: ParseResults):
		self.parse_results = results
		self.type = results.get("type")
		self.value = results.get("value")

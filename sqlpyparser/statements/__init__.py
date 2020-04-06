from typing import Any, List, Tuple, Type, Union
from pkgutil import walk_packages
from pyparsing import Group, Or, ParseExpression, ParseResults, ZeroOrMore
from abc import ABC

def tupleisinstance(value: Any, check: Tuple[Type[Any], ...]) -> bool:
	return isinstance(value, tuple) and len(check) == len(value) and \
		all((isinstance(value[ind], check[ind]) for ind in range(0, len(check))))

class SQLStatement(ABC):
	statement_type: str
	parse_expression: ParseExpression

	def __init__(self, results: ParseResults): ...

	def get(self, item: str) -> ParseExpression: ...

class FakeSQLClass():
	def __new__(cls, expression: ParseExpression, statement_type: str) -> \
			Type[SQLStatement]:
		return super().__new__(cls)

	def __init__(self, expression: ParseExpression, statement_type: str):
		self.statement_type = statement_type
		self.parse_expression = expression

	def __call__(self, results: ParseResults) -> SQLStatement:
		return results

	def parse(self, content: str):
		return self(self.parse_expression.parseString(content))

sub_modules = [
	finder.find_spec(f"sqlpyparser.statements.{module_name}").loader.load_module()
		for finder, module_name, _ in walk_packages(__path__)
]

sql_classes: List[Union[Type[SQLStatement], FakeSQLClass]] = [
	FakeSQLClass(sub_module.target[0], sub_module.target[1])
		if tupleisinstance(sub_module.target, (ParseExpression, str))
			else sub_module.target for sub_module in sub_modules
				if hasattr(sub_module, "target")
]

sql_syntax = ZeroOrMore(Group(Or(
	[sql_class.parse_expression for sql_class in sql_classes]
).setResultsName("statements", listAllMatches=True)))

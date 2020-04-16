from typing import Any, List, Optional, Type, Union
from pkgutil import walk_packages
from pyparsing import Group, Or, ParseExpression, ParseResults, ZeroOrMore
from abc import ABC, abstractmethod
from ..utilities import RawText, tupleisinstance

class SQLExpression(ABC):
	parse_results: ParseResults
	parse_expression: Optional[ParseExpression]

	@abstractmethod
	def __init__(self, results: ParseResults): ...

	def __getitem__(self, key: int) -> List[str]:
		return self.parse_results[key]

	def __getattr__(self, attribute: str) -> ParseResults:
		if not hasattr(self, "parse_results"):
			raise AttributeError()
		return self.parse_results.get(attribute)

	def __repr__(self, class_props_shown: int = 3, results_props_shown: int = 2):
		class_props = [
			key for key, val in vars(self).items() if not key.startswith("_")
		]
		class_props_short = class_props[:class_props_shown]
		class_props_not_shown = len(class_props) - class_props_shown
		results_props = {
			key: val if not isinstance(val, ParseResults) else RawText("...")
				for key, val in dict(self.parse_results).items()
		}
		results_props_short = dict([*results_props.items()][:results_props_shown])
		results_props_not_shown = len(results_props) - results_props_shown

		return "<{} {}{} {}{}>".format(
			type(self).__name__,
			class_props_short,
			f"; {class_props_not_shown} hidden" if class_props_not_shown > 0
				else "",
			results_props_short,
			f"; {results_props_not_shown} hidden" if results_props_not_shown > 0
				else ""
		)

	def get(self, item: str, defaultValue: Any = None) -> ParseResults:
		return self.parse_results.get(item, defaultValue)

class SQLStatement(SQLExpression):
	statement_type: str
	parse_expression: ParseExpression

class FakeSQLStatementClass():
	parse_expression: ParseExpression

	def __new__(cls, expression: ParseExpression, stmnt_type: str):
		class FakeSQLStatement(SQLStatement):
			statement_type = stmnt_type
			parse_expression = expression

			def __new__(cls, results: ParseResults) -> SQLStatement:
				return results

		sentinel = (None,)
		for attr in dir(cls):
			if getattr(FakeSQLStatement, attr, sentinel) is not sentinel:
				continue
			setattr(FakeSQLStatement, attr, getattr(cls, attr, sentinel))
		
		return FakeSQLStatement

	def __call__(self, results: ParseResults) -> SQLStatement:
		return results

	def parse(self, content: str):
		return self(self.parse_expression.parseString(content))

sub_modules = [
	finder.find_spec(f"sqlpyparser.statements.{module_name}").loader.load_module()
		for finder, module_name, _ in walk_packages(__path__)
]

sql_classes: List[Union[Type[SQLStatement], FakeSQLStatementClass]] = [
	clazz for sublist in
		([FakeSQLStatementClass(sub_module.target[0], sub_module.target[1])]
			if tupleisinstance(sub_module.target, (ParseExpression, str))
				else sub_module.target for sub_module in sub_modules
					if hasattr(sub_module, "target"))
						for clazz in sublist
]

sql_syntax = ZeroOrMore(Group(Or(
	[sql_class.parse_expression for sql_class in sql_classes]
).setResultsName("statements", listAllMatches=True)))

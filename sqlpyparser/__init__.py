from typing import IO, List, Literal, Union, overload
from pyparsing import ParseResults
from .statements import SQLStatement, sql_classes, sql_syntax

__author__ = 'Julius Seporaitis'
__email__ = 'julius@seporaitis.net'
__version__ = '0.1.6'

@overload
def parse(file_or_sql: Union[str, IO[Union[str, bytes]]],
		experimental: Literal[False]) -> ParseResults: ...
@overload
def parse(file_or_sql: Union[str, IO[Union[str, bytes]]],
		experimental: Literal[True]) -> List[SQLStatement]: ...
def parse(file_or_sql: Union[str, IO[Union[str, bytes]]],
		experimental: bool = False):
	sql_data = file_or_sql if isinstance(file_or_sql, str) else file_or_sql.read()
	sql_str = sql_data if isinstance(sql_data, str) else sql_data.decode("utf-8")

	parsed_sql = sql_syntax.parseString(sql_str, parseAll=True)

	if experimental:
		return [
			next(sql_class for sql_class in sql_classes if \
				sql_class.statement_type == sql_part.get("statement_type"))(
					sql_part) # type: ignore
						for sql_part in parsed_sql
		]
	else:
		return parsed_sql

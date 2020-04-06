# -*- encoding:utf-8 -*-
from pyparsing import CaselessKeyword, Group, Optional, Suppress, delimitedList
from mysqlparse.grammar.identifier import database_name_syntax, \
	identifier_syntax, ParseExpression

# TABLE REFERENCE
# Specifies a table from a database to use, and an optional alias given.
table_reference = Group(
	(
		database_name_syntax.setResultsName("database_name") +
		identifier_syntax.setResultsName("table_name") +
		Optional(
			(
				CaselessKeyword("AS") +
				identifier_syntax.setResultsName("alias_name")
			)
		)
	)
)

# COLUMN REFERENCE
column_reference = Group(
	(
		identifier_syntax.setResultsName("column_name") +
		Optional(
			(
				CaselessKeyword("AS") +
				identifier_syntax.setResultsName("alias_name")
			)
		)
	)
)

# SELECT SYNTAX
# The full implemented SELECT syntax.
# Source: https://dev.mysql.com/doc/refman/5.7/en/select.html
select_syntax = (
	CaselessKeyword("SELECT").setResultsName("statement_type") +
	(delimitedList(column_reference) ^ CaselessKeyword("*")).setResultsName("columns") +
	CaselessKeyword("FROM") +
	delimitedList(table_reference).setResultsName("tables") + 
	Suppress(Optional(";"))
)

from sqlpyparser.statements import SQLStatement

class SelectStatement(SQLStatement):
	statement_type = "SELECT"
	parse_expression = select_syntax

	def __init__(self, expression: ParseExpression):
		self.columns = expression.get("columns")

target = SelectStatement

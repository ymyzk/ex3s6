#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys

from ply import yacc

from tinyc import common
from tinyc.lexer import Lexer


class Parser(object):
    tokens = common.TOKENS

    def p_program_external_declaration(self, p):
        """program : external_declaration"""
        p[0] = p[1]

    def p_program_program_external_declaration(self, p):
        """program : program external_declaration"""
        p[0] = ('CONS', p[1], p[2],)

    def p_external_declaration(self, p):
        """external_declaration : declaration
                                | function_definition"""
        p[0] = p[1]

    def p_declaration(self, p):
        """declaration : INT declarator_list SEMICOLON"""
        p[0] = ('INT', p[2])

    def p_declarator_list_declarator(self, p):
        """declarator_list : declarator"""
        p[0] = p[1]

    def p_declarator_list_declarator_list(self, p):
        """declarator_list : declarator COMMA declarator_list"""
        p[0] = ('CONS', p[1], p[3])

    def p_declarator(self, p):
        """declarator : identifier"""
        p[0] = p[1]

    def p_function_definition(self, p):
        """function_definition : INT declarator LPAREN parameter_type_list_opt RPAREN compound_statement"""
        p[0] = ('FUNDEF', ('INT', p[2],), p[4], p[6])

    def p_parameter_type_list_opt(self, p):
        """parameter_type_list_opt : empty
                                   | parameter_type_list"""
        p[0] = p[1]

    def p_parameter_type_list_parameter_declaration(self, p):
        """parameter_type_list : parameter_declaration"""
        p[0] = p[1]

    def p_parameter_type_list_parameter_type_list(self, p):
        """parameter_type_list : parameter_type_list COMMA parameter_declaration"""
        p[0] = ('CONS', p[1], p[3],)

    def p_parameter_declaration(self, p):
        """parameter_declaration : INT declarator"""
        p[0] = ('INT', p[2],)

    def p_statement_semicolon(self, p):
        """statement : SEMICOLON"""
        pass

    def p_statement_expression(self, p):
        """statement : expression SEMICOLON"""
        p[0] = p[1]

    def p_statement_compound_statement(self, p):
        """statement : compound_statement"""
        p[0] = p[1]

    def p_statement_if(self, p):
        """statement : IF LPAREN expression RPAREN statement"""
        p[0] = ('IF', p[3], p[5],)

    def p_statement_if_else(self, p):
        """statement : IF LPAREN expression RPAREN statement ELSE statement"""
        p[0] = ('IF', p[3], p[5], p[7],)

    def p_statement_while(self, p):
        """statement : WHILE LPAREN expression RPAREN statement"""
        p[0] = ('WHILE', p[3], p[5],)

    def p_statement_return(self, p):
        """statement : RETURN expression SEMICOLON"""
        p[0] = ('RETURN', p[2],)

    def p_compound_statement(self, p):
        """compound_statement : LBRACE declaration_list_opt statement_list_opt RBRACE"""
        p[0] = ('CMPD_STM', p[2], p[3],)

    def p_declaration_list_opt(self, p):
        """declaration_list_opt : empty
                                | declaration_list"""
        p[0] = p[1]

    def p_declaration_list_declaration(self, p):
        """declaration_list : declaration"""
        p[0] = p[1]

    def p_declaration_list_declaration_list(self, p):
        """declaration_list : declaration_list declaration"""
        p[0] = ('CONS', p[1], p[2],)

    def p_statement_list_opt(self, p):
        """statement_list_opt : empty
                              | statement_list"""
        p[0] = p[1]

    def p_statement_list_statement(self, p):
        """statement_list : statement"""
        p[0] = p[1]

    def p_statement_list_statement_list(self, p):
        """statement_list : statement_list statement"""
        p[0] = ('CONS', p[1], p[2],)

    def p_expression_assign_expr(self, p):
        """expression : assign_expr"""
        p[0] = p[1]

    def p_expression_expression(self, p):
        """expression : expression COMMA assign_expr"""
        p[0] = ('CONS', p[1], p[3],)

    def p_assign_expr_or(self, p):
        """assign_expr : logical_OR_expr"""
        p[0] = p[1]

    def p_assign_expr_assign(self, p):
        """assign_expr : identifier EQUALS assign_expr"""
        p[0] = ('ASSIGN', p[1], p[3],)

    def p_logical_OR_expr_and_expr(self, p):
        """logical_OR_expr : logical_AND_expr"""
        p[0] = p[1]

    def p_logical_OR_expr_or(self, p):
        """logical_OR_expr : logical_OR_expr LOR logical_AND_expr"""
        p[0] = ('LOR', p[1], p[3],)

    def p_logical_AND_expr_equality_expr(self, p):
        """logical_AND_expr : equality_expr"""
        p[0] = p[1]

    def p_logical_AND_expr_and(self, p):
        """logical_AND_expr : logical_AND_expr LAND equality_expr"""
        p[0] = ('LAND', p[1], p[3],)

    def p_equality_expr_relational_expr(self, p):
        """equality_expr : relational_expr"""
        p[0] = p[1]

    def p_equality_expr_eq(self, p):
        """equality_expr :  equality_expr EQ relational_expr"""
        p[0] = ('EQ', p[1], p[3],)

    def p_equality_expr_neq(self, p):
        """equality_expr : equality_expr NEQ relational_expr"""
        p[0] = ('NEQ', p[1], p[3],)

    def p_relational_expr_add(self, p):
        """relational_expr : add_expr"""
        p[0] = p[1]

    def p_relational_expr_lt(self, p):
        """relational_expr : relational_expr LT add_expr"""
        p[0] = ('LT', p[1], p[3],)

    def p_relational_expr_lte(self, p):
        """relational_expr : relational_expr LTE add_expr"""
        p[0] = ('LTE', p[1], p[3],)

    def p_relational_expr_gt(self, p):
        """relational_expr : relational_expr GT add_expr"""
        p[0] = ('GT', p[1], p[3],)

    def p_relational_expr_gte(self, p):
        """relational_expr : relational_expr GTE add_expr"""
        p[0] = ('GTE', p[1], p[3],)

    def p_add_expr_mult_expr(self, p):
        """add_expr : mult_expr"""
        p[0] = p[1]

    def p_add_expr_plus(self, p):
        """add_expr : add_expr PLUS mult_expr"""
        p[0] = ('PLUS', p[1], p[3],)

    def p_add_expr_minus(self, p):
        """add_expr : add_expr MINUS mult_expr"""
        p[0] = ('MINUS', p[1], p[3],)

    def p_mult_expr_unary_expr(self, p):
        """mult_expr : unary_expr"""
        p[0] = p[1]

    def p_mult_expr_mult(self, p):
        """mult_expr : mult_expr MULT unary_expr"""
        p[0] = ('MULT', p[1], p[3],)

    def p_mult_expr_div(self, p):
        """mult_expr : mult_expr DIV unary_expr"""
        p[0] = ('DIV', p[1], p[3],)

    def p_unary_expr_postfix(self, p):
        """unary_expr : postfix_expr"""
        p[0] = p[1]

    def p_unary_expr_minus(self, p):
        """unary_expr : MINUS unary_expr"""
        p[0] = ('UMINUS', p[2],)

    def p_postfix_expr_primary_expr(self, p):
        """postfix_expr : primary_expr"""
        p[0] = p[1]

    def p_postfix_expr_fcall(self, p):
        """postfix_expr : identifier LPAREN argument_expression_list_opt RPAREN"""
        p[0] = ('FCALL', p[1], p[3],)

    def p_primary_expr(self, p):
        """primary_expr : identifier
                        | CONSTANT"""
        p[0] = p[1]

    def p_primary_expr_paren(self, p):
        """primary_expr : LPAREN expression RPAREN"""
        p[0] = (p[2],)

    def p_argument_expression_list_opt(self, p):
        """argument_expression_list_opt : empty
                                        | argument_expression_list"""
        p[0] = p[1]

    def p_argument_expression_list_assign_expr(self, p):
        """argument_expression_list : assign_expr"""
        p[0] = p[1]

    def p_argument_expression_list_argument_expression_list(self, p):
        """argument_expression_list : argument_expression_list COMMA assign_expr"""
        p[0] = (p[1], p[3],)

    def p_identifier(self, p):
        """identifier : ID"""
        p[0] = ('ID', p[1],)

    def p_empty(self, p):
        """empty : """
        pass

    def p_error(self, t):
        message = "Line {line}: Syntax error at '{value}'. "
        print(
            message.format(
                line=t.lineno,
                value=t.value),
            file=sys.stderr)

    precedence = (
        ('right', 'ELSE',),
    )

    def build(self, **kwargs):
        self.lexer = Lexer()
        self.lexer.build()
        kwargs['debug'] = True
        self.parser = yacc.yacc(module=self, **kwargs)

    def parse(self, data):
        return self.parser.parse(data)

#!/usr/bin/env python3
from utils import intersperse

class LSString:

    def __init__(self, string: str | None):
        if string is None: return None
        tokens = string.split(";")
        expressions = {}
        for expr in tokens:
            #ActionResource(BardicInspiration,3,0)
            #expr_type = ActionResource
            #arg = BardicInspiration,3,0
            expr_type, args = expr.split("(")    # ProficiencyBonus
            func = args.rstrip(")").split(",")[0]  # SavingThrow
            arg_params = args.rstrip(")").split(",")[1:]  # ['Charisma']
            if expr_type in expressions.keys():
                if func in expressions[expr_type].keys():
                    if arg_params not in expressions[expr_type][func] and len(arg_params) != 0:
                        expressions[expr_type][func].append(arg_params)
                elif len(arg_params) != 0:
                    expressions[expr_type][func] = [arg_params]
                else:
                    expressions[expr_type][func] = []
            elif len(arg_params) != 0:
                expressions[expr_type] = { func : [arg_params] }
            else:
                expressions[expr_type] = { func: [] }
        # print(expressions)
        self.expressions = expressions

    def __getitem__(self, item):
        return self.expressions[item]

    def __setitem__(self, item, value):
        self.expressions[item] = value

    def update(self, other):
        for expr_type, expr in other.expressions.items():
            # if we do not habe given expression type, just add it
            if expr_type not in self.expressions.keys():
                self.expressions[expr_type] = expr
            # if we do, merge sub-dicts
            else:
                self.expressions[expr_type].update(other.expressions[expr_type])


    def __str__(self):
        result = []
        for expr_type, expr_func in self.expressions.items():
            if type(expr_func) is not dict and type(expr_func) is not list:
                result.append(f"{expr_type}({expr_func})")
                continue
            for func, params in expr_func.items():
                # SavingThrow, [['Charisma'], ['Dexterity']
                if len(params) == 0:
                    expr_str = f"{expr_type}({func})"
                    result.append(expr_str)
                else:
                    for param_table in params:
                        # ['Charisma']
                        if len(param_table) >= 1:
                            param_str = "," + "".join(intersperse(param_table, ","))
                            func_expr = func + param_str
                        else:
                            func_expr = func + "," + param_table[0]
                        expr_str = expr_type + "(" + func_expr + ")"
                        result.append(expr_str)
        return "".join(intersperse(result, ";"))




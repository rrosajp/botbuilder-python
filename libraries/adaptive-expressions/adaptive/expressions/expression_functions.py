from .expression_type import ADD, SUBTRACT, MULTIPLY, DIVIDE, MOD
from .expression_type import (
    EQUAL,
    LESSTHAN,
    LESSTHANOREQUAL,
    GREATERTHAN,
    GREATERTHANOREQUAL,
    NOT,
    OR,
    AND,
    CONCAT,
)

# Math
from .builtin_functions.add import Add
from .builtin_functions.subtract import Subtract
from .builtin_functions.multiply import Multiply
from .builtin_functions.divide import Divide
from .builtin_functions.min import Min
from .builtin_functions.max import Max
from .builtin_functions.power import Power
from .builtin_functions.mod import Mod
from .builtin_functions.average import Average
from .builtin_functions.sum import Sum
from .builtin_functions.range import Range
from .builtin_functions.floor import Floor
from .builtin_functions.ceiling import Ceiling
from .builtin_functions.round import Round

# Comparisons
from .builtin_functions.equal import Equal
from .builtin_functions.less_than import LessThan
from .builtin_functions.less_than_or_equal import LessThanOrEqual
from .builtin_functions.greater_than import GreaterThan
from .builtin_functions.greater_than_or_equal import GreaterThanOrEqual
from .builtin_functions.not_equal import NotEqual
from .builtin_functions.exist import Exist

# Logic
from .builtin_functions.not_function import Not
from .builtin_functions.or_function import Or
from .builtin_functions.and_function import And

# String
from .builtin_functions.concat import Concat
from .builtin_functions.length import Length
from .builtin_functions.replace import Replace
from .builtin_functions.replace_ignore_case import ReplaceIgnoreCase
from .builtin_functions.split import Split
from .builtin_functions.to_lower import ToLower
from .builtin_functions.to_upper import ToUpper
from .builtin_functions.trim import Trim
from .builtin_functions.ends_with import EndsWith
from .builtin_functions.starts_with import StartsWith
from .builtin_functions.count_word import CountWord
from .builtin_functions.add_ordinal import AddOrdinal
from .builtin_functions.new_guid import NewGuid
from .builtin_functions.index_of import IndexOf
from .builtin_functions.last_index_of import LastIndexOf
from .builtin_functions.eol import Eol
from .builtin_functions.sentence_case import SentenceCase
from .builtin_functions.title_case import TitleCase

# Colleaction

# DataTime
from .builtin_functions.add_days import AddDays
from .builtin_functions.add_hours import AddHours
from .builtin_functions.add_minutes import AddMinutes
from .builtin_functions.add_seconds import AddSeconds

# Timex
# Conversions
# URI Parsing Functions

# Memory
from .builtin_functions.create_array import CreateArray

# Misc
# Object manipulation and construction functions
# Regular expression
# Type Checking

# pylint: disable=too-many-statements
def get_standard_functions() -> dict:
    functions = []

    # Math
    functions.append(Add())
    functions.append(Subtract())
    functions.append(Multiply())
    functions.append(Divide())
    functions.append(Min())
    functions.append(Max())
    functions.append(Power())
    functions.append(Mod())
    functions.append(Average())
    functions.append(Sum())
    functions.append(Range())
    functions.append(Floor())
    functions.append(Ceiling())
    functions.append(Round())

    # Comparisons
    functions.append(Equal())
    functions.append(LessThan())
    functions.append(LessThanOrEqual())
    functions.append(GreaterThan())
    functions.append(GreaterThanOrEqual())
    functions.append(NotEqual())
    functions.append(Exist())

    # Logic
    functions.append(Not())
    functions.append(Or())
    functions.append(And())

    # String
    functions.append(Concat())
    functions.append(Length())
    functions.append(Replace())
    functions.append(ReplaceIgnoreCase())
    functions.append(Split())
    # TODO: substring, skipped
    functions.append(ToLower())
    functions.append(ToUpper())
    functions.append(Trim())
    functions.append(EndsWith())
    functions.append(StartsWith())
    functions.append(CountWord())
    functions.append(AddOrdinal())
    functions.append(NewGuid())
    functions.append(IndexOf())
    functions.append(LastIndexOf())
    functions.append(Eol())
    functions.append(SentenceCase())
    functions.append(TitleCase())

    # Colleaction

    # DataTime
    functions.append(AddDays())
    functions.append(AddHours())
    functions.append(AddMinutes())
    functions.append(AddSeconds())

    # Timex
    # Conversions
    # URI Parsing Functions

    # Memory
    functions.append(CreateArray())

    # Misc
    # Object manipulation and construction functions
    # Regular expression
    # Type Checking

    lookup = dict()
    for function in functions:
        lookup[function.expr_type] = function

    # Math aliases
    lookup["add"] = lookup[ADD]
    lookup["sub"] = lookup[SUBTRACT]
    lookup["mul"] = lookup[MULTIPLY]
    lookup["div"] = lookup[DIVIDE]
    lookup["mod"] = lookup[MOD]

    # Comparison aliases
    lookup["equals"] = lookup[EQUAL]
    lookup["less"] = lookup[LESSTHAN]
    lookup["lessOrEuqals"] = lookup[LESSTHANOREQUAL]
    lookup["greater"] = lookup[GREATERTHAN]
    lookup["greaterOrEquals"] = lookup[GREATERTHANOREQUAL]

    # Logic aliases
    lookup["not"] = lookup[NOT]
    lookup["or"] = lookup[OR]
    lookup["and"] = lookup[AND]

    lookup["&"] = lookup[CONCAT]

    return lookup


class ExpressionFunctions:
    standard_functions = staticmethod(get_standard_functions())

from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import CONCAT
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Concat(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            CONCAT,
            Concat.evaluator(),
            ReturnType.Array | ReturnType.String,
            FunctionUtils.validate_at_least_one,
        )

    @staticmethod
    def evaluator():
        def anonymous_function(args: list):
            first_item = args[0]
            second_item = args[1]
            is_first_list = isinstance(first_item, list)
            is_second_list = isinstance(second_item, list)
            if first_item is None and second_item is None:
                return None
            elif first_item is None and is_second_list:
                return second_item
            elif second_item is None and is_first_list:
                return first_item
            elif is_first_list and is_second_list:
                return first_item + second_item
            else:
                return str(first_item) + str(second_item)

        return FunctionUtils.apply_sequence(anonymous_function)

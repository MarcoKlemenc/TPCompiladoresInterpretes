from llvmlite import ir


class StandardObject():
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value

    def eq(self, other):
        return type(self) == type(other) and self.get_value() == other.get_value()

    def ne(self, other):
        return not self.eq(other)

    def gt(self, other):
        if type(self) != type(other):
            raise Exception("Está tratando de comparar dos tipos de dato distintos")
        return self.get_value() > other.get_value()

    def lt(self, other):
        if type(self) != type(other):
            raise Exception("Está tratando de comparar dos tipos de dato distintos")
        return self.get_value() < other.get_value()

    def _eval(self, ir_type):
        return ir.Constant(ir_type, self.get_value())


class Number(StandardObject):
    def get_value(self):
        return float(self.value)

    def eval(self):
        return self._eval(ir.DoubleType())

    def get_decimal_places(self):
        number_components = self.value.split(".")
        return len(number_components[1]) if len(number_components) == 2 else 0

    def format(self):
        return "%.{}f".format(self.get_decimal_places())


class String(StandardObject):
    def get_value(self):
        return self.value

    def get_string_length(self):
        return len(self.value)

    def eval(self):
        return ir.Constant(ir.ArrayType(ir.IntType(8), len(self.value)), bytearray(self.value.encode("utf8")))

    def format(self):
        return "%c" * self.get_string_length()


class Boolean(StandardObject):
    def get_value(self):
        return int(self.value)

    def eval(self):
        return self._eval(ir.IntType(1))

    def format(self):
        return "VERDADERO" if self.value else "FALSO"


class OpBuilder():
    def __init__(self, builder, module):
        self.builder = builder
        self.module = module

    def operand_is_number(self, operand):
        return isinstance(operand, Number) or issubclass(type(operand), NumberOp)

    def operand_is_string(self, operand):
        return isinstance(operand, String) or issubclass(type(operand), StringOp)

    def build_op(self, left, right, operator):
        if operator == "SUM":
            return self.sum(left, right)
        if operator == "SUB":
            return self.sub(left, right)
        if operator == "MUL":
            return self.mul(left, right)
        if operator == "DIV":
            return self.div(left, right)

    def sum(self, left, right):
        if self.operand_is_number(left) and self.operand_is_number(right):
            return Sum(self.builder, self.module, left, right)
        if self.operand_is_string(left) and self.operand_is_string(right):
            return StringSum(self.builder, self.module, left, right)
        raise Exception("Suma inválida")

    def sub(self, left, right):
        if self.operand_is_number(left) and self.operand_is_number(right):
            return Sub(self.builder, self.module, left, right)
        raise Exception("Resta inválida")

    def mul(self, left, right):
        if self.operand_is_number(left) and self.operand_is_number(right):
            return Mul(self.builder, self.module, left, right)
        raise Exception("Multiplicación inválida")

    def div(self, left, right):
        if self.operand_is_number(left) and self.operand_is_number(right):
            return Div(self.builder, self.module, left, right)
        raise Exception("División inválida")


class BinaryOp():
    def __init__(self, builder, module, left, right):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right


class StringOp(BinaryOp):
    def format(self):
        return "%c" * self.get_string_length()


class StringSum(StringOp):
    def get_value(self):
        return self.left.get_value() + self.right.get_value()

    def get_string_length(self):
        return self.left.get_string_length() + self.right.get_string_length()

    def eval(self):
        return String(self.builder, self.module, self.get_value()).eval()


class NumberOp(BinaryOp):
    def _eval(self, func):
        return getattr(self.builder, func)(self.left.eval(), self.right.eval())

    def get_decimal_places(self):
        return max(self.left.get_decimal_places(), self.right.get_decimal_places())

    def format(self):
        return "%.{}f".format(self.get_decimal_places())


class Sum(NumberOp):
    def eval(self):
        return self._eval('fadd')


class Sub(NumberOp):
    def eval(self):
        return self._eval('fsub')


class Mul(NumberOp):
    def eval(self):
        return self._eval('fmul')


class Div(NumberOp):
    def eval(self):
        return self._eval('fdiv')


class Print():
    def __init__(self, builder, module, printf, value, format):
        self.builder = builder
        self.module = module
        self.printf = printf
        self.value = value

        if not hasattr(Print, 'format_dict'):
            Print.format_dict = {}

        voidptr_ty = ir.IntType(8).as_pointer()
        if not Print.format_dict.get(format):
            fmt = "{}\n\0".format(format)
            c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                                bytearray(fmt.encode("utf8")))
            Print.format_dict[format] = ir.GlobalVariable(self.module, c_fmt.type, name=format)
            Print.format_dict[format].value_type = c_fmt.type
            Print.format_dict[format].linkage = 'internal'
            Print.format_dict[format].global_constant = True
            Print.format_dict[format].initializer = c_fmt
        self.fmt_arg = self.builder.bitcast(Print.format_dict[format], voidptr_ty)

    def eval(self):
        value = self.value.eval()

        # Call Print Function
        self.builder.call(self.printf, [self.fmt_arg, value])

from llvmlite import ir


class StandardObject():
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value

    def eq(self, other):
        return self.get_value() == other.get_value()

    def gt(self, other):
        return self.get_value() > other.get_value()

    def lt(self, other):
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
        return bytearray(self.value.encode("utf8"))

    def eval(self):
        return self._eval(ir.ArrayType(ir.IntType(8), len(self.value)))

    def format(self):
        return "%c" * len(self.value)


class Boolean(StandardObject):
    def get_value(self):
        return int(self.value)

    def eval(self):
        return self._eval(ir.IntType(1))

    def format(self):
        return "VERDADERO" if self.value else "FALSO"


class BinaryOp():
    def __init__(self, builder, module, left, right):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right

    def _eval(self, func):
        return getattr(self.builder, func)(self.left.eval(), self.right.eval())

    def eq(self, other):
        return type(self) == type(other) and self.left == other.left and self.right == other.right

    def get_decimal_places(self):
        return max(self.left.get_decimal_places(), self.right.get_decimal_places())

    def format(self):
        return "%.{}f".format(self.get_decimal_places())


class Sum(BinaryOp):
    def eval(self):
        return self._eval('fadd')


class Sub(BinaryOp):
    def eval(self):
        return self._eval('fsub')


class Mul(BinaryOp):
    def eval(self):
        return self._eval('fmul')


class Div(BinaryOp):
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

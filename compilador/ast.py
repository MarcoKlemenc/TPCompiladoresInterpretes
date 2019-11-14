from llvmlite import ir


class Number():
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value

    def eval(self):
        i = ir.Constant(ir.DoubleType(), float(self.value))
        return i

    def get_decimal_places(self):
        number_components = self.value.split(".")
        return len(number_components[1]) if len(number_components) == 2 else 0

    def format(self):
        return "%.{}f".format(self.get_decimal_places())


class String():
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value

    def eval(self):
        i = ir.Constant(ir.ArrayType(ir.IntType(8), len(self.value)), bytearray(self.value.encode("utf8")))
        return i

    def format(self):
        return "%c" * len(self.value)


class BinaryOp():
    def __init__(self, builder, module, left, right):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right

    def get_decimal_places(self):
        return max(self.left.get_decimal_places(), self.right.get_decimal_places())

    def format(self):
        return "%.{}f".format(self.get_decimal_places())


class Sum(BinaryOp):
    def eval(self):
        i = self.builder.fadd(self.left.eval(), self.right.eval())
        return i


class Sub(BinaryOp):
    def eval(self):
        i = self.builder.fsub(self.left.eval(), self.right.eval())
        return i


class Mul(BinaryOp):
    def eval(self):
        i = self.builder.fmul(self.left.eval(), self.right.eval())
        return i


class Div(BinaryOp):
    def eval(self):
        i = self.builder.fdiv(self.left.eval(), self.right.eval())
        return i


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

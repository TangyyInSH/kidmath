#####option####
plus = True
minus = True
multiply = False
divide = False

num = 100
####type
# type1: 10 + 20 = ()
# type2: 10 + () = 20 / () + 10 = 20
# type3: 10 + () - 3 = 20 / () + 10 + 8 = 10 / 10 + 8 - () = 12
# type4: 10 + 3 = 20 + () / 10 + 3 = () + 20
type1 = True
type2 = True
type3 = True
type4 = False
negative_value_supported = False
boundary = 100

decimal = False

import random

class MathGenerator:
    def __init__(self, tp_list, op_list, boundary, negative_value_supported):
        self.tp_func = [getattr(self, 'gen_type' + str(i + 1)) for i, t in enumerate(tp_list) if t == True]
        self.op_list = [i for i, o in enumerate(op_list) if o == True]

        self.boundary = boundary
        self.negative_value_supported = negative_value_supported
        self.oper_map = {0: '+', 1: '-', 2: '*', 3: '/'}

    def test_decimal(self, eq):
        if eval(eq) == eval('1.0*' + eq):
            return True
        return False

    def randint(self, a, b):
        return int(round(random.uniform(a, b)))

    def gen_boundary(self):
        b1 = 0
        if negative_value_supported:
            b1 = -self.boundary
        b2 = self.boundary
        return b1, b2

    def gen_oper(self):
        oper = self.op_list[int(random.random() * 100) % len(self.op_list)]
        oper_str = self.oper_map[oper]
        return oper, oper_str

    def gen_type1(self):
        b1, b2 = self.gen_boundary()
        oper, oper_str = self.gen_oper()

        while True:
            a = self.randint(b1, b2)
            b = self.randint(b1, b2)
            if oper == 3 and b == 0:
                continue

            eq = '%d %s %d' % (a, oper_str, b)
            res = eval(eq)
            if not decimal and not self.test_decimal(eq):
                continue

            if res <= b2 and res >= b1:
                return '%d %s %d = (       )' % (a, oper_str, b), res

    def gen_type2(self):
# type2: 10 + () = 20 / () + 10 = 20
        b1, b2 = self.gen_boundary()
        oper, oper_str = self.gen_oper()
        while True:
            a = self.randint(b1, b2)
            b = self.randint(b1, b2)

            eq = '%d %s %d' % (a, oper_str, b)
            res = 0
            try:
                res = eval(eq)
            except ZeroDivisionError:
                continue

            if not decimal and not self.test_decimal(eq):
                continue

            if res <= b2 and res >= b1:
                pos = self.randint(0, 1)
                if pos == 0:
                    return '(       ) %s %d = %d' % (oper_str, b, res), a
                else:
                    return '%d %s (       ) = %d' % (a, oper_str, res), b

    def gen_4_number(self):
        b1, b2 = self.gen_boundary()
        oper1, oper_str1 = self.gen_oper()
        oper2, oper_str2 = self.gen_oper()
        while True:
            a = self.randint(b1, b2)
            b = self.randint(b1, b2)
            c = self.randint(b1, b2)

            eq = '%d %s %d %s %d' % (a, oper_str1, b, oper_str2, c)
            res = 0
            try:
                res = eval(eq)
            except ZeroDivisionError:
                continue

            if not decimal and not self.test_decimal(eq):
                continue

            if res <= b2 and res >= b1:
                return a, b, c, res, oper_str1, oper_str2

    def gen_type3(self):
        a, b, c, res, oper_str1, oper_str2 = self.gen_4_number()

# type3: 10 + () - 3 = 20 / () + 10 + 8 = 10 / 10 + 8 - () = 12
        pos = self.randint(0, 3)

        if pos == 0:
            return '(       ) %s %d %s %d = %d' % (oper_str1, b, oper_str2, c, res), a
        elif pos == 1:
            return '%d %s (       ) %s %d = %d' % (a, oper_str1, oper_str2, c, res), b
        elif pos == 2:
            return '%d %s %d %s (       ) = %d' % (a, oper_str1, b, oper_str2, res), c
        else:
            return '%d %s %d %s %d = (       )' % (a, oper_str1, b, oper_str2, c), res

    def gen_type4(self):
       return None, None

    def gen(self, num):
        equations = []
        answers = []
        for i in range(num):
            tp = self.tp_func[int(random.random() * 100) % len(self.tp_func)]
            eq, res = tp()
            equations.append(eq)
            answers.append(res)

        return equations, answers

    def print_and_gen(self, num):
        equations, answers = self.gen(num)
        columns = 3
        page_width = 83 
        w = page_width / columns

        #print "date:________________"
        #print "name:________________"
        print
        import sys
        idx = 0
        for eq in equations:
            sys.stdout.write(eq.ljust(w))
            idx += 1
            if idx == columns:
                sys.stdout.write("\n")
                idx = 0

def test():
    g = MathGenerator([type1, type2, type3, type4], [plus, minus, multiply, divide], boundary, negative_value_supported)
#    equations, answers = g.gen(num)
#    print '\n'.join(['%s %s' % (e, a) for e, a in zip(equations, answers)])
    for i in range(20):
        g.print_and_gen(num)

test()

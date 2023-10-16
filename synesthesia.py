# simple drop-in variant
def colorize(x):
    import hashlib
    r, g, b, *_ = hashlib.sha256(bytes(repr(x), 'utf-8')).digest()
    r /= 255
    g /= 255
    b /= 255
    if r < 0.5 and g < 0.5 and b < 0.5:
        r = 1 - r
        g = 1 - g
        b = 1 - b
    return r, g, b

class Color:
    def __init__(self, *args):
        if len(args) == 0:
            self.value = [0, 0, 0, 0]
        elif len(args) == 1:
            if isinstance(args[0], Color):
                self.value = args[0].value
            else:
                self.value = Color(*args[0]).value
        elif len(args) == 3:
            self.value = [*args, 1]
        elif len(args) == 4:
            self.value = list(args)
        else:
            raise TypeError('wrong number of arguments')
        self._clamp()

    @property
    def r(self): return self.value[0]
    @r.setter
    def r(self, value): self.value[0] = value
    @property
    def g(self): return self.value[1]
    @g.setter
    def g(self, value): self.value[1] = value
    @property
    def b(self): return self.value[2]
    @b.setter
    def b(self, value): self.value[2] = value
    @property
    def a(self): return self.value[3]
    @a.setter
    def a(self, value): self.value[3] = value

    def __repr__(self): return ''.join([
        'Color(',
        ', '.join([f'{i}' if type(i) == int else f'{i:.3}' for i in self.value]),
        ')',
    ])

    def __add__(self, other):
        return Color([i + j for i, j in zip(self.value, other.value)])

    def __sub__(self, other):
        return Color([i - j for i, j in zip(self.value, other.value)])

    def __mul__(self, amount):
        return Color([i * amount for i in self.value])

    def __rmul__(self, amount): return self.__mul__(amount)

    def __truediv__(self, amount):
        return self * (1 / amount)

    def brighten(self, amount):
        return Color([i * amount for i in self.value[:3]] + [self.a])

    def mix(self, *others):
        return sum([i / (1 + len(others)) for i in [self, *others]], Color())

    def css(self):
        result = 'rgba('
        for i in range(3):
            result += f'{round(255 * self.value[i])}, '
        result += f'{self.a})'
        return result

    def _clamp(self):
        self.value = [min(1, max(0, i)) for i in self.value]
        return self

def color(x):
    if type(x) == str:
        if len(x) == 0: return Color()
        elif len(x) == 1:
            return Color({
                'a': (  1,   1,   0,   1), 'b': (  1, 1/2, 1/2,   1), 'c': (1/2, 1/2,   1,   1), 'd': (  0,   0,   1,   1),
                'e': (  1,   0,   0,   1), 'f': (3/4, 3/4, 3/4,   1), 'g': (  0,   0,   0,   1), 'h': (1/2, 1/4,   0,   1),
                'i': (  1,   1,   1,   1), 'j': (  1, 3/4, 3/4,   1), 'k': (  0,   0,   0,   1), 'l': (1/2, 1/2, 1/2,   1),
                'm': (3/4,   0,   0,   1), 'n': (  0, 3/4,   0,   1), 'o': (  1,   1,   1,   1), 'p': (  1, 1/2,   0,   1),
                'q': (3/4,   0, 3/4,   1), 'r': (  0, 1/2,   0,   1), 's': (3/4, 3/4, 3/4,   1), 't': (  1, 3/4,   0,   1),
                'u': (  1,   1,   1,   1), 'v': (  1, 1/2,   0,   1), 'w': (1/2,   0,   0,   1), 'x': (1/4, 1/4, 1/4,   1),
                'y': (  1,   1,   0,   1), 'z': (1/2, 1/2, 1/2,   1),
            }.get(x.lower(), Color()))
        else:
            result = color(x[-1])
            for i in range(len(x) - 1, -1, -1): result = result.mix(color(x[i]))
            return result
    return (0, 0, 0, 0)

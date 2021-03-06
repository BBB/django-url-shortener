"""
Convert numbers from base 10 integers to base X strings and back again.

Original: http://www.djangosnippets.org/snippets/1431/

Sample usage:

>>> base20 = BaseConverter('0123456789abcdefghij')
>>> base20.from_decimal(1234)
'31e'
>>> base20.to_decimal('31e')
1234
"""
import numbers
import string


class EncodingError(ValueError):
    pass


class DecodingError(ValueError):
    pass


class BaseConverter(object):
    decimal_digits = string.digits

    def __init__(self, digits):
        self.digits = digits

    def from_decimal(self, i):
        if not isinstance(i, numbers.Real):
            raise EncodingError('%s is not an int()' % i)
        return self.convert(i, self.decimal_digits, self.digits)

    def to_decimal(self, s):
        if not isinstance(s, basestring):
            raise DecodingError('%s is not a basestring()' % s)
        for char in s:
            if char not in self.digits:
                raise EncodingError('Invalid character for encoding: %s' % digit)
        return int(self.convert(s, self.digits, self.decimal_digits))

    def convert(number, fromdigits, todigits):
        # Based on http://code.activestate.com/recipes/111286/
        if str(number)[0] == '-':
            number = str(number)[1:]
            neg = 1
        else:
            neg = 0

        # make an integer out of the number
        x = 0
        for digit in str(number):
            x = x * len(fromdigits) + fromdigits.index(digit)

        # create the result in base 'len(todigits)'
        if x == 0:
            res = todigits[0]
        else:
            res = ''
            while x > 0:
                digit = x % len(todigits)
                res = todigits[digit] + res
                x = int(x / len(todigits))
            if neg:
                res = '-' + res
        return res
    convert = staticmethod(convert)


bin = BaseConverter('01')
hexconv = BaseConverter(string.hexdigits)
base62 = BaseConverter(string.digits + string.letters)

"""SYSC 2100 Summer 2022, Lab 1."""

__author__ = 'Leandro Velazquez'
__student_number__ = '101094885'


def gcd(m: int, n: int) -> int:
    """Return the greatest common divisor of m and n.

    Precondition: m > 0, n > 0.

    >>> gcd(4, 1)
    1
    >>> gcd(30, 5)
    5
    >>> gcd(9, 17)
    1
    """
    while m % n != 0:
        m, n = n, m % n
    return n


class Fraction:
    def __init__(self, n: int, d: int) -> None:
        """Initialize self with numerator n and denominator d.

        Raise a ValueError exception if d is 0.

        When __init__ returns, this fraction will be in reduced form.
        This means that:
        (1) if the numerator is equal to 0, the denominator is always 1.
        (2) if the numerator is not equal to 0, the denominator is always
        positive. This means that negative fractions always have a negative
        numerator and a positive denominator.
        (3) the numerator and denominator have no common divisors other than 1.

        >>> Fraction(3, 4)
        Fraction(3, 4)
        >>> Fraction(6, 8)
        Fraction(3, 4)
        >>> Fraction(-3, 4)
        Fraction(-3, 4)
        >>> Fraction(3, -4)
        Fraction(-3, 4)
        >>> Fraction(-3, -4)
        Fraction(3, 4)
        >>> Fraction(0, 5)
        Fraction(0, 1)
        """

        if(d == 0):
            raise ValueError("denominator cannot be 0")

        x = gcd(n, d)
        n = n // x
        d = d // x

        if (n == 0):
            d = 1

        elif(d < 0):
            n = n * -1
            d = d * -1

        self._num = n
        self._den = d

    def __str__(self) -> str:
        """Return a string representation of self in the format: 'n/d'.

        >>> f = Fraction(3, 4)
        >>> str(f)
        '3/4'
        >>> f = Fraction(6, -8)
        >>> str(f)
        '-3/4'
        """
        n = self._num
        d = self._den
        s = str(n) + "/" + str(d)
        return s

    def __repr__(self) -> str:
        """Return a string representation of self in the format:
        'Fraction(n, d)'.

        >>> f = Fraction(3, 4)
        >>> repr(f)
        'Fraction(3, 4)'
        >>> f = Fraction(6, -8)
        >>> repr(f)
        'Fraction(-3, 4)'
        """
        return "Fraction({0}, {1})".format(self._num, self._den)

    def numerator(self) -> int:
        """Return the numerator of self.

        >>> f = Fraction(3, 4)
        >>> f.numerator()
        3
        """
        return self._num

    def denominator(self) -> int:
        """Return the denominator of self.

        >>> f = Fraction(3, 4)
        >>> f.denominator()
        4
        """
        return self._den

    def __add__(self, other_fraction: 'Fraction') -> 'Fraction':
        """Return the sum of self and other_fraction.

        >>> f1 = Fraction(3, 4)
        >>> f2 = Fraction(1, 8)
        >>> f1 + f2
        Fraction(7, 8)
        >>> f1 = Fraction(1, 4)
        >>> f2 = Fraction(1, 2)
        >>> f1 + f2
        Fraction(3, 4)
        """
        n = (self._num * other_fraction._den) + \
            (self._den * other_fraction._num)
        d = self._den * other_fraction._den
        a = Fraction(n, d)
        return a

    def __sub__(self, other_fraction: 'Fraction') -> 'Fraction':
        """Return the difference of self and other_fraction; that is,
        the Fraction that is obtained by subtracting other_fraction from self.

        >>> f1 = Fraction(3, 4)
        >>> f2 = Fraction(1, 8)
        >>> f1 - f2
        Fraction(5, 8)
        >>> f1 = Fraction(1, 4)
        >>> f2 = Fraction(1, 2)
        >>> f1 - f2
        Fraction(-1, 4)
        """
        n = (self._num * other_fraction._den) - \
            (self._den * other_fraction._num)
        d = self._den * other_fraction._den
        a = Fraction(n, d)
        return a

    def __mul__(self, other_fraction: 'Fraction') -> 'Fraction':
        """Return the product of self and other_fraction.

        >>> f1 = Fraction(3, 4)
        >>> f2 = Fraction(1, 8)
        >>> f1 * f2
        Fraction(3, 32)
        >>> f2 = Fraction(6, 8)
        >>> f1 * f2
        Fraction(9, 16)
        """
        n = self._num * other_fraction._num
        d = self._den * other_fraction._den
        a = Fraction(n, d)
        return a

    def __truediv__(self, other_fraction: 'Fraction') -> 'Fraction':
        """Return the result of dividing self by other_fraction.

        >>> f1 = Fraction(3, 4)
        >>> f2 = Fraction(1, 8)
        >>> f1 / f2
        Fraction(6, 1)
        >>> f2 = Fraction(2, 1)
        >>> f1 / f2
        Fraction(3, 8)
        """
        n = self._num * other_fraction._den
        d = self._den * other_fraction._num
        a = Fraction(n, d)
        return a

    def __eq__(self, other_fraction: 'Fraction') -> bool:
        """Return True if self equals other_fraction.

        >>> f1 = Fraction(3, 4)
        >>> f2 = Fraction(6, 8)
        >>> f1 == f2
        True
        >>> f2 = Fraction(1, 2)
        >>> f1 == f2
        False
        """
        first_num = self._num * other_fraction._den
        second_num = other_fraction._num * self._den

        return first_num == second_num

    def __gt__(self, other_fraction: 'Fraction') -> bool:
        """Return True if self is greater than other_fraction.

        >>> f1 = Fraction(3, 4)
        >>> f2 = Fraction(6, 8)
        >>> f1 > f2
        False
        >>> f2 = Fraction(7, 8)
        >>> f1 > f2
        False
        >>> f2 > f1
        True
        """
        first_num = self._num * other_fraction._den
        second_num = other_fraction._num * self._den
        return first_num > second_num

    def __ge__(self, other_fraction: 'Fraction') -> bool:
        """Return True if self is greater than or equal to other_fraction.

        >>> f1 = Fraction(3, 4)
        >>> f2 = Fraction(6, 8)
        >>> f1 >= f2
        True
        >>> f2 = Fraction(7, 8)
        >>> f1 >= f2
        False
        >>> f2 >= f1
        True
        """
        first_num = self._num * other_fraction._den
        second_num = other_fraction._num * self._den
        return first_num >= second_num

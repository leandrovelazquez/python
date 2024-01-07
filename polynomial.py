# SYSC 2100 Lab 6/Assignment 1

# An implementation of ADT Polynomial that uses a singly-linked list as the
# underlying data structure.

# A polynomial consists of 0 or more terms, with each term consisting of a
# coefficient and an exponent. Coefficients are integers, and terms with zero
# coefficients are not stored in the linked list. Exponents are non-negative
# integers.

from typing import Any

__author__ = 'bailey'
__version__ = '1.00'
__date__ = 'February 21, 2022'

"""
History:
1.00 Feb. 21, 2022 - Initial release.
"""


class Polynomial:

    class TermNode:
        def __init__(self, coefficient: int, exponent: int) -> None:
            """Initialize this node to represent a polynomial term with the
            given coefficient and exponent.

            Raise ValueError if the coefficent is 0 or if the exponent
            is negative.
            """
            if coefficient == 0:
                raise ValueError("TermNode: zero coefficient")
            if exponent < 0:
                raise ValueError("TermNode: negative exponent")

            self.coeff = coefficient
            self.exp = exponent
            self.next = None

    def __init__(self, coefficient: int = None, exponent: int = 0) -> None:
        """Initialize this Polynomial with a single term constructed from the
        coefficient and exponent.

        If one argument is given, the term is a constant coefficient
        (the exponent is 0).
        If no arguments are given, the Polynomial has no terms.

        # Polynomial with no terms:
        >>> p = Polynomial()
        >>> print(p._head)
        None
        >>> print(p._tail)
        None

        # Polynomial with one term (a constant):
        >>> p = Polynomial(12)
        >>> p._head.coeff
        12
        >>> p._head.exp
        0
        >>> print(p._head.next)
        None

        # Polynomial with one term:
        >>> p = Polynomial(12, 2)
        >>> p._head.coeff
        12
        >>> p._head.exp
        2
        >>> print(p._head.next)
        None
        """
        # A polynomial is stored as a singly linked list. Each node stores
        # one term, with the nodes ordered in descending order, based on the
        # exponent. (The head node is the term with the highest exponent,
        # and the tail node is the term with the lowest exponent.)
        if coefficient is None and exponent == 0:
            self._head = None
        else:
            self._head = Polynomial.TermNode(coefficient, exponent)
        self._tail = self._head

    def __str__(self) -> str:
        """Return a string representation of this polynomial.

        # Polynomial with no terms:
        >>> p = Polynomial()
        >>> str(p)
        ''

        # Polynomial with one term (a constant):
        >>> p = Polynomial(12)
        >>> str(p)
        '12'

        # Polynomials with one term:
        >>> p = Polynomial(12, 1)
        >>> str(p)
        '12x'

        >>> p = Polynomial(12, 2)
        >>> str(p)
        '12x^2'

        # See __add__ for string representations of polynomials with
        # more than one term.
        """
        curr = self._head
        s = ""

        if self._head == None:
            return s

        while (curr != None):

            c = curr.coeff
            x = curr.exp

            if curr != self._head and c > 0:
                s = s + "+"

            if x == 0:
                s = str(c)
                curr = curr.next
                continue

            if c == 1:
                s = s + "x"

            if c != 1:
                s = s + str(c) + "x"

            if x > 1:
                s = s + "^" + str(x)

            curr = curr.next
        return s

    def __repr__(self) -> str:
        """Return the same string as __str__."""
        return str(self)

    def degree(self) -> int:
        """Return this polynomial's degree.

        Raise ValueError if the polynomial has no terms.

        >>> p = Polynomial(12, 2)
        >>> p.degree()
        2
        """
        return self._head.exp

    def evaluate(self, x: float) -> float:
        """Evaluate the polynomial at x and return the result.

        Raise ValueError if the polynomial has no terms.

        >>> p = Polynomial(12, 2)
        >>> p.evaluate(3)
        108.0
        """
        c = float(self._head.coeff)
        e = float(self._head.exp)

        a = c * x ** e
        return a

    def __add__(self, rhs: 'Polynomial') -> 'Polynomial':
        """ Return a new Polynomial containing the sum of this polynomial
        and rhs.

        Raise ValueError if either polynomial has no terms.

        >>> p1 = Polynomial(12, 2)
        >>> p2 = Polynomial(-3, 1)
        >>> p3 = Polynomial(7)
        >>> p1 + p2
        12x^2-3x

        >>> p1 + p3
        12x^2+7

        >>> p1 + p2 + p3  # Equivalent to (p1 + p2) + p3
        12x^2-3x+7

        >>> p2 = Polynomial(3, 1)
        >>> p1 + p2 + p3
        12x^2+3x+7
        """
        p3 = Polynomial(1, 0)
        p1 = self._head
        p2 = rhs._head
        curr = None
        while (p1 != None or p2 != None):

            if curr != None:
                newTerm = Polynomial.TermNode(1, 0)
                curr.next = newTerm
                curr = newTerm
            else:
                curr = p3._head

            if p2 == None:
                curr.coeff = p1.coeff
                curr.exp = p1.exp
                p1 = p1.next
                continue

            if p1 == None:
                curr.coeff = p2.coeff
                curr.exp = p2.exp
                p2 = p2.next
                continue

            if p1.exp > p2.exp:
                curr.coeff = p1.coeff
                curr.exp = p1.exp
                p1 = p1.next

            elif p2.exp > p1.exp:
                curr.coeff = p2.coeff
                curr.exp = p2.exp
                p2 = p2.next

            elif p1.exp == p2.exp:
                currcoeff = p1.coeff + p2.coeff
                curr.exp = p1.exp
                p1 = p1.next
                p2 = p2.next

        return p3

    def __mul__(self, rhs: 'Polynomial') -> 'Polynomial':
        """ Return a new Polynomial containing the product of this polynomial
        and rhs.

        Raise ValueError if either polynomial has no terms.

        >>> p1 = Polynomial(12, 2)
        >>> p2 = Polynomial(-3, 1)
        >>> p3 = Polynomial(7)
        >>> poly = p1 + p2 + p3
        >>> poly
        12x^2-3x+7

        >>> p4 = Polynomial(2, 1)
        >>> p4 * poly
        24x^3-6x^2+14x
        """




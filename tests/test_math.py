import pytest
import sympy as sp

from SLiCAP import *  # TODO: change imports when import chain is reworked
import SLiCAP.SLiCAPmath as sm

SYMBOLIC_MATRIX = sp.sympify("""Matrix([
        [0, 0, 0, 0, 0, 1.0, 0],
        [0, -2.0, 0, 0, 1.0*g_m1, 1.0*g_m1, 0],
        [0, 0, -2.0, 1.0*g_m2, -1.0*g_m2, 0, 0],
        [0, 1.0, 0, 0.5*c_i2*s + 0.5/r_o1, -0.5*c_i2*s+ 0.5/r_o1, 0, 0],
        [0, 1.0, -1.0, -0.5*c_i2*s + 0.5/r_o1,
         0.5*c_i1*s+ 0.5*c_i2*s + 0.5/r_o2 + 0.5/r_o1 + 1.0/R, 0.5*c_i1*s, -0.5/r_o2],
        [1.0, 0, 0, 0, 0.5*c_i1*s, 0.5*c_i1*s, 0],
        [0, 0, 1.0, 0, -0.5/r_o2, 0, 0.5/r_o2 + 1.0/R_L]])"""
    )

# Calculated offline with SymPy's det()
DETERMINANT = sp.sympify("""
    -1.0*(0.5*R*R_L*c_i1*c_i2*r_o1*s**2 + 0.5*R*R_L*c_i1*s + 1.0*R*R_L*c_i2*g_m1*r_o1*s
    + 2.0*R*R_L*c_i2*s + 1.0*R*c_i1*c_i2*r_o1*r_o2*s**2
    + 1.0*R*c_i1*r_o2*s + 2.0*R*c_i2*g_m1*r_o1*r_o2*s + 1.0*R*c_i2*r_o1*s
    + 4.0*R*c_i2*r_o2*s + 1.0*R*g_m1*g_m2*r_o1*r_o2 + 2.0*R*g_m2*r_o2 + 1.0*R
    + 1.0*R_L*c_i2*r_o1*s + 1.0*R_L + 2.0*c_i2*r_o1*r_o2*s + 2.0*r_o2)/(R*R_L*r_o1*r_o2)
    """
    )


def test_det_empty():
    # Determinant of empty matrix should throw an exception
    with pytest.raises(ValueError):
        sm.det(sp.Matrix([]))


def test_det_nonsq():
    # Determinant of non-square matrix should throw an exception
    with pytest.raises(TypeError):
        sm.det(sp.Matrix([1, 2, 3]))


@pytest.mark.parametrize("matrix, determinant", [
        (sp.Matrix([-1.5e-5]), sp.N(-1.5e-5)),
        (sp.Matrix([[0, 0], [0, 0]]), sp.N(0)),
        (sp.Matrix([[1, 2], [-1, -2]]), sp.N(0)),
        (sp.Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), sp.N(1)),
        (SYMBOLIC_MATRIX, DETERMINANT),
    ])
def test_det(matrix, determinant):
    assert sp.simplify(sm.det(matrix) - determinant) == 0

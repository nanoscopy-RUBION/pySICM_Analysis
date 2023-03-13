import lmfit
import numpy as np
from sicm_analyzer.sicm_data import SICMdata
from symfit.core.minimizers import BFGS
import symfit
from symfit.core.objectives import LeastSquares



def polynomial_fifth_degree(x, y, p00=0, p10=0, p01=0, p20=0, p11=0, p02=0, p30=0, p21=0, p12=0, p03=0, p40=0, p31=0,
                            p22=0, p13=0, p04=0, p50=0, p41=0, p32=0, p23=0, p14=0, p05=0):
    """A two-dimensional polynomial function of fifth degree.
    x and y are independent variables."""
    return p00 + p10 * x + p20 * x**2 + p30 * x**3 + p40 * x**4 + p50 * x**5 \
               + p01 * y + p02 * y**2 + p03 * y**3 + p04 * y**4 + p05 * y**5 \
               + p11 * x*y + p12 * x * y**2 + p13 * x *y**3 + p14 * x * y**4 \
               + p21 * x**2 * y + p22 * x**2 * y**2 + p23 * x**2 + y**3 \
               + p31 * x**3 * y + p32 * x**3 * y**2 \
               + p41 * x**4 * y


def poly_xx_fit(data: SICMdata):
    """Fit data to a two-dimensional polynomial of fifth degree."""
    x = data.x.flatten("F")
    y = data.y.flatten("F")
    z = data.z.flatten("F")

    model = lmfit.Model(polynomial_fifth_degree, independent_vars=["x", "y"])

    params = lmfit.Parameters()
    params.add("p00", value=0)
    params.add("p10", value=0)
    params.add("p20", value=0)
    params.add("p30", value=0)
    params.add("p40", value=0)
    params.add("p50", value=0)
    params.add("p01", value=0)
    params.add("p02", value=0)
    params.add("p03", value=0)
    params.add("p04", value=0)
    params.add("p05", value=0)
    params.add("p11", value=0)
    params.add("p21", value=0)
    params.add("p31", value=0)
    params.add("p41", value=0)
    params.add("p12", value=0)
    params.add("p13", value=0)
    params.add("p14", value=0)
    params.add("p22", value=0)
    params.add("p32", value=0)
    params.add("p23", value=0)

    fit_result = model.fit(z, x=x, y=y, params=params)
    fitted_z = model.func(x=x, y=y, **fit_result.best_values)
    #print(type(fit_result.fit_report()))
    return fitted_z.reshape(data.z.shape, order="F"), fit_result.fit_report()



def polynomial_fifth_degree_symfit(x_data, y_data, z_data: np.array):
    """Returns data fitted to a polynomial of 5th degree with two
    variables x and y.
    """
    x, y, z = symfit.variables('x, y, z')
    p00, p10, p01, p20, p11, p02, p30, p21, p12, p03, p40, p31, p22, p13, p04, p50, p41, p32, p23, p14, p05 = symfit.parameters(
        "p00, p10, p01, p20, p11, p02, p30, p21, p12, p03, p40, p31, p22, p13, p04, p50, p41, p32, p23, p14, p05"
    )
    p00.value = 10
    p10.value = 0.01
    p20.value = 0.01
    p30.value = 0.01
    p40.value = 0.01
    p50.value = 0.01
    p01.value = 0.01
    p02.value = 0.01
    p03.value = 0.01
    p04.value = 0.01
    p05.value = 0.01
    p11.value = 0.01
    p21.value = 0.01
    p31.value = 0.01
    p41.value = 0.01
    p12.value = 0.01
    p13.value = 0.01
    p14.value = 0.01
    p22.value = 0.01
    p32.value = 0.01
    p23.value = 0.01

    model_dict = {
        z: symfit.Poly(
            {
                (0, 0): p00,
                (1, 0): p10,
                (0, 1): p01,
                (2, 0): p20,
                (1, 1): p11,
                (0, 2): p02,
                (3, 0): p30,
                (2, 1): p21,
                (1, 2): p12,
                (0, 3): p03,
                (4, 0): p40,
                (3, 1): p31,
                (2, 2): p22,
                (1, 3): p13,
                (0, 4): p04,
                (5, 0): p50,
                (4, 1): p41,
                (3, 2): p32,
                (2, 3): p23,
                (1, 4): p14,
                (0, 5): p05,
            },
            x, y
        ).as_expr()
    }
    model = symfit.Model(model_dict)

    # perform fit
    fit = symfit.Fit(model, x=x_data, y=y_data, z=z_data, objective=LeastSquares, minimizer=[BFGS])
    fit_result = fit.execute()
    #_print_fit_results_to_console(fit_result)
    z_fitted = model(x=x_data, y=y_data, **fit_result.params).z
    return z_fitted, fit_result

def _print_fit_results_to_console(fit_result):
    """A helper function for debugging."""
    print("###############################################")
    print("Fit results:")
    print(fit_result)
    print("###############################################")
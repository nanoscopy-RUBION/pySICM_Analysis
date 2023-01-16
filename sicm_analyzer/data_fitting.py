from lmfit import Model, Parameters
from sicm_analyzer.sicm_data import SICMdata


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

    model = Model(polynomial_fifth_degree, independent_vars=["x", "y"])

    params = Parameters()
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

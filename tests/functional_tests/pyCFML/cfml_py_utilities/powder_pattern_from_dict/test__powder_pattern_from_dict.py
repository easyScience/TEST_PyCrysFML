import inspect
import matplotlib.pyplot as plt
import numpy as np
from numpy.testing import assert_almost_equal
import os
import sys

sys.path.append(os.getcwd())  # to access tests/helpers.py
from tests.helpers import (chi_squared,
                           load_from_json,
                           path_to_input,
                           path_to_desired,
                           sub_to_ndarray)

from pycrysfml import cfml_py_utilities


PLOT_CHARTS_IN_TESTS = bool(int(os.environ.get('PLOT_CHARTS_IN_TESTS', '0')))

# Help functions

def compute_cw_pattern(study_dict:dict):
    #_, y = crysfml08lib.f_powder_pattern_from_json(study_dict)  # returns x and y arrays
    x, y = cfml_py_utilities.cw_powder_pattern_from_dict(study_dict)  # returns x and y arrays
    return x, y

def compute_tof_pattern(study_dict:dict):
    x, y = cfml_py_utilities.cw_powder_pattern_from_dict(study_dict)  # returns x and y arrays
    return x, y

def plot_charts(desired_x:np.ndarray,
                desired_y:np.ndarray,
                actual_x:np.ndarray,
                actual_y:np.ndarray,
                chi2:float,
                skip_last:int = 100): # skip last points as FullProf calculation is not good there
    if not PLOT_CHARTS_IN_TESTS:
        return
    vertical_shift = 10
    plt.plot(desired_x[:-skip_last], desired_y[:-skip_last])
    plt.plot(actual_x[:-skip_last], actual_y[:-skip_last], linestyle='dotted')
    plt.plot(desired_x[:-skip_last], actual_y[:-skip_last] - desired_y[:-skip_last] - vertical_shift)
    plt.legend(["FullProf", "PyCrysFML"])
    plt.title(f'{inspect.stack()[1].function}, chi2={chi2:.1f}')
    plt.show()

# Tests

def test__cw_powder_pattern_from_dict__Al2O3_uvwx_noassym(benchmark):
    # input
    project = load_from_json(path_to_input('al2o3_uvwx_no-assym.json'))
    # actual
    actual_x, actual_y = benchmark(compute_cw_pattern, project)
    actual_y = actual_y / actual_y.max() * 100  # normalize
    # desired
    desired_x, desired_y = sub_to_ndarray(path_to_desired('al2o3_uvwx_no-assym.sim'))
    desired_y = desired_y / desired_y.max() * 100  # normalize
    # goodness of fit
    chi2 = chi_squared(desired_y, actual_y)
    # compare
    skip_last = 100
    assert_almost_equal(chi2, 6.97, decimal=1, verbose=True)
    #assert_almost_equal(actual_x, desired_x, decimal=3, verbose=True)
    assert_almost_equal(actual_y[:-skip_last], desired_y[:-skip_last], decimal=0, verbose=True)
    # plot
    plot_charts(desired_x, desired_y, actual_x, actual_y, chi2, skip_last)

def test__cw_powder_pattern_from_dict__PbSO4(benchmark):
    # input
    project = load_from_json(path_to_input('pbso4_cw.json'))
    # actual
    actual_x, actual_y = benchmark(compute_cw_pattern, project)
    actual_y = actual_y / actual_y.max() * 100  # normalize
    # desired
    desired_x, desired_y = sub_to_ndarray(path_to_desired('pbso4_cw.sub'))
    desired_y = desired_y / desired_y.max() * 100  # normalize
    # goodness of fit
    chi2 = chi_squared(desired_y, actual_y)
    # compare
    skip_last = 100
    assert_almost_equal(chi2, 116.6, decimal=2, verbose=True)
    #assert_almost_equal(actual_x, desired_x, decimal=3, verbose=True)
    assert_almost_equal(actual_y[:-skip_last], desired_y[:-skip_last], decimal=0, verbose=True)
    # plot
    plot_charts(desired_x, desired_y, actual_x, actual_y, chi2, skip_last)

def _test__tof_powder_pattern_from_dict__Al2O3(benchmark):
    # input
    project = load_from_json(path_to_input('al2o3_tof.json'))
    # actual
    actual_x, actual_y = benchmark(compute_tof_pattern, project)
    actual_y = actual_y / actual_y.max() * 100  # normalize
    # desired
    desired_x, desired_y = sub_to_ndarray(path_to_desired('al2o3_tof.sim'))
    desired_y = desired_y / desired_y.max() * 100  # normalize
    # goodness of fit
    chi2 = chi_squared(desired_y, actual_y)
    # compare
    skip_last = 100
    #assert_almost_equal(actual_x, desired_x, decimal=3, verbose=True)
    #assert_almost_equal(actual_y[:-skip_last], desired_y[:-skip_last], decimal=0, verbose=True)
    # plot
    plot_charts(desired_x, desired_y, actual_x, actual_y, chi2, skip_last)

def _test__tof_powder_pattern_from_dict__ncaf(benchmark):
    # input
    project = load_from_json(path_to_input('ncaf_tof.json'))
    # actual
    actual_x, actual_y = benchmark(compute_tof_pattern, project)
    actual_y = actual_y / actual_y.max() * 100  # normalize
    # desired
    desired_x, desired_y = sub_to_ndarray(path_to_desired('ncaf_tof.sim'))
    desired_y = desired_y / desired_y.max() * 100  # normalize
    # goodness of fit
    chi2 = chi_squared(desired_y, actual_y)
    # compare
    skip_last = 100
    assert_almost_equal(actual_x, desired_x, decimal=3, verbose=True)
    #assert_almost_equal(actual_y[:-skip_last], desired_y[:-skip_last], decimal=0, verbose=True)
    # plot
    plot_charts(desired_x, desired_y, actual_x, actual_y, chi2, skip_last)

def _test__tof_powder_pattern_from_dict__Si(benchmark):
    # input
    project = load_from_json(path_to_input('si_tof.json'))
    # actual
    actual_x, actual_y = benchmark(compute_tof_pattern, project)
    actual_y = actual_y / actual_y.max() * 100  # normalize
    # desired
    desired_x, desired_y = sub_to_ndarray(path_to_desired('si_tof.sub'))
    desired_y = desired_y / desired_y.max() * 100  # normalize
    # goodness of fit
    chi2 = chi_squared(desired_y, actual_y)
    # compare
    skip_last = 100
    #assert_almost_equal(actual_x, desired_x, decimal=3, verbose=True)
    #assert_almost_equal(actual_y[:-skip_last], desired_y[:-skip_last], decimal=0, verbose=True)
    # plot
    plot_charts(desired_x, desired_y, actual_x, actual_y, chi2, skip_last)

# Debug

if __name__ == '__main__':
    pass

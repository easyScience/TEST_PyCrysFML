import inspect
import matplotlib.pyplot as plt
from numpy.testing import assert_almost_equal
import os
import sys

sys.path.append(os.getcwd())  # to access tests/helpers.py
from tests.helpers import load_from_json, path_to_input, path_to_desired, sub_to_ndarray

from pycrysfml import cfml_utilities


PLOT_CHARTS_IN_TESTS = bool(int(os.environ.get('PLOT_CHARTS_IN_TESTS', '0')))

# Help functions

def compute_cw_pattern(study_dict:dict):
    #_, y = crysfml08lib.f_powder_pattern_from_json(study_dict)  # returns x and y arrays
    x, y = cfml_utilities.cw_powder_pattern_from_json(study_dict)  # returns x and y arrays
    return x, y

# Tests

def test__cw_powder_pattern_from_json__Al2O3_uvwx_noassym(benchmark):
    # input
    project = load_from_json(path_to_input('al2o3_uvwx_no-assym.json'))
    # actual
    actual_x, actual_y = benchmark(compute_cw_pattern, project)
    actual_y = actual_y / actual_y.max() * 100  # normalize
    # desired
    desired_x, desired_y = sub_to_ndarray(path_to_desired('al2o3_uvwx_no-assym.sim'))
    desired_y = desired_y / desired_y.max() * 100  # normalize
    # plot
    skip_last = 100  # skip last points as FullProf calculation is not good there
    if PLOT_CHARTS_IN_TESTS:
        plt.plot(desired_x[:-skip_last], desired_y[:-skip_last])
        plt.plot(actual_x[:-skip_last], actual_y[:-skip_last], linestyle='dotted')
        plt.plot(actual_x[:-skip_last], actual_y[:-skip_last] - desired_y[:-skip_last] - 10)
        plt.title(f'{inspect.currentframe().f_code.co_name}')
        plt.show()
    # compare
    assert_almost_equal(desired_x, actual_x, decimal=3, verbose=True)
    assert_almost_equal(desired_y[:-skip_last], actual_y[:-skip_last], decimal=0, verbose=True)

def test__cw_powder_pattern_from_json__PbSO4_uvwx_noassym(benchmark):
    # input
    project = load_from_json(path_to_input('pbso4_uvwx_no-assym.json'))
    # actual
    actual_x, actual_y = benchmark(compute_cw_pattern, project)
    actual_y = actual_y / actual_y.max() * 100  # normalize
    # desired
    desired_x, desired_y = sub_to_ndarray(path_to_desired('pbso4_uvwx_no-assym.sub'))
    desired_y = desired_y / desired_y.max() * 100  # normalize
    # plot
    skip_last = 100  # skip last points as FullProf calculation is not good there
    if PLOT_CHARTS_IN_TESTS:
        plt.plot(desired_x[:-skip_last], desired_y[:-skip_last])
        plt.plot(actual_x[:-skip_last], actual_y[:-skip_last], linestyle='dotted')
        plt.plot(actual_x[:-skip_last], actual_y[:-skip_last] - desired_y[:-skip_last] - 10)
        plt.title(f'{inspect.currentframe().f_code.co_name}')
        plt.show()
    # compare
    assert_almost_equal(desired_x, actual_x, decimal=3, verbose=True)
    assert_almost_equal(desired_y[:-skip_last], actual_y[:-skip_last], decimal=0, verbose=True)

def test__cw_powder_pattern_from_json__PbSO4_uvwy_noassym(benchmark):
    # input
    project = load_from_json(path_to_input('pbso4_uvwy_no-assym.json'))
    # actual
    actual_x, actual_y = benchmark(compute_cw_pattern, project)
    actual_y = actual_y / actual_y.max() * 100  # normalize
    # desired
    desired_x, desired_y = sub_to_ndarray(path_to_desired('pbso4_uvwy_no-assym.sub'))
    desired_y = desired_y / desired_y.max() * 100  # normalize
    # plot
    skip_last = 100  # skip last points as FullProf calculation is not good there
    if PLOT_CHARTS_IN_TESTS:
        plt.plot(desired_x[:-skip_last], desired_y[:-skip_last])
        plt.plot(actual_x[:-skip_last], actual_y[:-skip_last], linestyle='dotted')
        plt.plot(actual_x[:-skip_last], actual_y[:-skip_last] - desired_y[:-skip_last] - 10)
        plt.title(f'{inspect.currentframe().f_code.co_name}')
        plt.show()
    # compare
    assert_almost_equal(desired_x, actual_x, decimal=3, verbose=True)
    assert_almost_equal(desired_y[:-skip_last], actual_y[:-skip_last], decimal=0, verbose=True)

# Debug

if __name__ == '__main__':
    pass

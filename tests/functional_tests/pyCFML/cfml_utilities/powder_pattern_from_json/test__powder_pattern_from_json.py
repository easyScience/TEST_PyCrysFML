import inspect
import matplotlib.pyplot as plt
import numpy as np
from numpy.testing import assert_almost_equal
import os
import sys

sys.path.append(os.getcwd())  # to access tests/helpers.py
from tests.helpers import load_from_json, path_to_data, path_to_desired, sub_to_ndarray

from pycrysfml import cfml_utilities


# Help functions

def compute_pattern(study_dict:dict):
    #_, y = crysfml08lib.f_powder_pattern_from_json(study_dict)  # returns x and y arrays
    x, y = cfml_utilities.powder_pattern_from_json(study_dict)  # returns x and y arrays
    return x, y

# Tests

def test__powder_pattern_from_json__SrTiO3_Pm3m(benchmark):
    # input
    project = load_from_json(path_to_data('srtio3.json'))
    # actual
    actual_x, actual_y = benchmark(compute_pattern, project)
    actual_y = actual_y / actual_y.max() * 100  # normalize
    # desired
    desired_x, desired = np.loadtxt(path_to_desired('srtio3-pm3m-pattern_Nebil-ifort.xy'), unpack=True)
    desired_y = desired - 20.0  # remove background
    desired_y = np.roll(desired_y, -1)  # compensate for a 1-element horizontal shift in y data between old Nebil windows build and Andrew current gfortran build
    desired_y = desired_y / desired_y.max() * 100  # normalize
    # plot
    plt.plot(desired_x, desired_y)
    plt.plot(actual_x, actual_y, linestyle='dotted')
    plt.plot(actual_x, actual_y - desired_y - 10)
    plt.title(f'{inspect.currentframe().f_code.co_name}')
    plt.show()
    # compare
    assert_almost_equal(desired_x, actual_x, decimal=3, verbose=True)
    assert_almost_equal(desired_y, actual_y, decimal=1, verbose=True)

def test__powder_pattern_from_json__SrTiO3_Pnma(benchmark):
    # input
    project = load_from_json(path_to_data('srtio3.json'))
    project['phases'][0]['SrTiO3']['_space_group_name_H-M_alt'] = 'P n m a'
    # actual
    actual_x, actual_y = benchmark(compute_pattern, project)
    actual_y = actual_y / actual_y.max() * 100
    # desired
    desired_y = np.loadtxt(path_to_desired('srtio3-pnma-pattern_Andrew-ifort.y'), unpack=True)
    desired_y = desired_y - 20.0  # remove background
    desired_y = desired_y / desired_y.max() * 100  # normalize
    # plot
    plt.plot(actual_x, desired_y)
    plt.plot(actual_x, actual_y, linestyle='dotted')
    plt.plot(actual_x, actual_y - desired_y - 10)
    plt.title(f'{inspect.currentframe().f_code.co_name}')
    plt.show()
    # compare
    assert_almost_equal(desired_y, actual_y, decimal=2, verbose=True)

def test__powder_pattern_from_json__PbSO4_uvwx_noassym(benchmark):
    # input
    project = load_from_json(path_to_data('pbso4.json'))
    # actual
    actual_x, actual_y = benchmark(compute_pattern, project)
    actual_y = actual_y / actual_y.max() * 100  # normalize
    # desired
    desired_x, desired_y = sub_to_ndarray(path_to_desired('pbso4-uvwx_no-assym.sub'))
    desired_y = desired_y / desired_y.max() * 100  # normalize
    # plot
    plt.plot(desired_x, desired_y)
    plt.plot(actual_x, actual_y, linestyle='dotted')
    plt.plot(actual_x, actual_y - desired_y - 10)
    plt.title(f'{inspect.currentframe().f_code.co_name}')
    plt.show()
    # compare
    assert_almost_equal(desired_x, actual_x, decimal=3, verbose=True)
    assert_almost_equal(desired_y, actual_y, decimal=1, verbose=True)

# Debug

if __name__ == '__main__':
    pass

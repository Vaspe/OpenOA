import unittest
import numpy as np
import pandas as pd
from numpy import testing as nptest

from operational_analysis.toolkits import power_curve
from operational_analysis.toolkits.power_curve.parametric_forms import *


noise = 0.1

class TestPowerCurveFunctions(unittest.TestCase):

    def setUp(self):
        np.random.seed(42)
        params = [1300, -7, 11, 2, 0.5]
        self.x = pd.Series(np.random.random(100)*30)
        self.y = pd.Series(logistic5param(self.x, *params) + np.random.random(100) * noise )
        pass

    def test_IEC(self):
        # Create test data using logistic5param form
        curve = power_curve.IEC(self.x, self.y)
        y_pred = curve(self.x)
        # Does the IEC power curve match the test data?
        nptest.assert_allclose(self.y, y_pred, rtol=1, atol=noise*2, err_msg="Power curve did not properly fit.")

    def test_logistic_5_param(self):
        # Create test data using logistic5param form
        curve = power_curve.logistic_5_parametric(self.x, self.y)
        y_pred = curve(self.x)
        # Does the logistic-5 power curve match the test data?
        nptest.assert_allclose(self.y, y_pred, rtol=1, atol=noise*2, err_msg="Power curve did not properly fit.")

    def test_spline_fit(self):
        # Create test data using logistic5param form
        curve = power_curve.spline_fit(self.x, self.y, 20)
        y_pred = curve(self.x)
        # Does the spline-fit power curve match the test data?
        nptest.assert_allclose(self.y, y_pred, rtol=1, atol=noise*2, err_msg="Power curve did not properly fit.")
        
    def tearDown(self):
        pass


class TestParametricForms(unittest.TestCase):

    def setUp(self):
        pass

    def test_logistic5parameter(self):
        y_pred = logistic5param(np.array([1., 2., 3.]), *[1300., -7., 11., 2., 0.5])
        y = np.array([ 2.29403585,  5.32662505, 15.74992462])
        nptest.assert_allclose(y, y_pred, err_msg="Power curve did not properly fit.")
        pass

    def test_logistic5parameter_capped(self):
        # Numpy array + Lower Bound
        y_pred = logistic5param_capped(np.array([1., 2., 3.]), *[1300., -7., 11., 2., 0.5], lower=5., upper=20.)
        y = np.array([5., 5.32662505, 15.74992462])
        nptest.assert_allclose(y, y_pred, err_msg="Power curve did not properly fit.")

        # Numpy array + Upper and Lower Bound
        y_pred = logistic5param_capped(np.array([1., 2., 3.]), *[1300., -7., 11., 2., 0.5], lower=5., upper=10.)
        y = np.array([5., 5.32662505, 10.])
        nptest.assert_allclose(y, y_pred, err_msg="Power curve did not properly fit.")

        # Pandas Series + Upper and Lower Bound
        y_pred = logistic5param_capped(pd.Series([1., 2., 3.]), *[1300., -7., 11., 2., 0.5], lower=5., upper=20.)
        y = pd.Series([5., 5.32662505, 15.74992462])
        nptest.assert_allclose(y, y_pred, err_msg="Power curve did not properly fit.")

        # Pandas Series + Upper and Lower Bound
        y_pred = logistic5param_capped(pd.Series([1., 2., 3.]), *[1300., -7., 11., 2., 0.5], lower=5., upper=10.)
        y = pd.Series([5., 5.32662505, 10.])
        nptest.assert_allclose(y, y_pred, err_msg="Power curve did not properly fit.")

    def tearDown(self):
        pass

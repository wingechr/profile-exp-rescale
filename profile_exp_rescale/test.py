import unittest

import numpy as np
from scipy.stats import rankdata

from .profile_exp_rescale import rescale


class TestRescale(unittest.TestCase):
    def setUp(self):
        self.xs1 = [0, 10, 2, 3, 5]
        self.xs1_rank = [1.0, 5.0, 2.0, 3.0, 4.0]
        self.xs1_sum = np.sum(self.xs1)
        self.xs1_max = np.max(self.xs1)

    def test_do_nothing(self):
        ys = rescale(self.xs1)
        self.assertAlmostEqual(np.sum(ys), self.xs1_sum)
        self.assertAlmostEqual(np.max(ys), self.xs1_max)
        self.assertListEqual(list(rankdata(ys)), self.xs1_rank)

    def test_linear_scale(self):
        target_sum = self.xs1_sum * 10
        target_max_value = self.xs1_max * 10
        ys = rescale(self.xs1, target_sum=target_sum, target_max_value=target_max_value)
        self.assertAlmostEqual(np.sum(ys), target_sum)
        self.assertAlmostEqual(np.max(ys), target_max_value)
        self.assertListEqual(list(rankdata(ys)), self.xs1_rank)

        target_sum = self.xs1_sum * 0.1
        target_max_value = self.xs1_max * 0.1
        ys = rescale(self.xs1, target_sum=target_sum, target_max_value=target_max_value)
        self.assertAlmostEqual(np.sum(ys), target_sum)
        self.assertAlmostEqual(np.max(ys), target_max_value)
        self.assertListEqual(list(rankdata(ys)), self.xs1_rank)

    def test_exp_scale_sum(self):
        target_sum = 40 - 0.01  # close to max
        ys = rescale(self.xs1, target_sum=target_sum)
        self.assertAlmostEqual(np.sum(ys), target_sum)
        self.assertAlmostEqual(np.max(ys), self.xs1_max)
        self.assertListEqual(list(rankdata(ys)), self.xs1_rank)

        target_sum = 10 + 0.01  # close to min
        ys = rescale(self.xs1, target_sum=target_sum)
        self.assertAlmostEqual(np.sum(ys), target_sum)
        self.assertAlmostEqual(np.max(ys), self.xs1_max)
        self.assertListEqual(list(rankdata(ys)), self.xs1_rank)

    def test_exp_scale_max(self):
        target_max_value = 20 - 0.01  # close to max
        ys = rescale(self.xs1, target_max_value=target_max_value)
        self.assertAlmostEqual(np.sum(ys), self.xs1_sum)
        self.assertAlmostEqual(np.max(ys), target_max_value)
        self.assertListEqual(list(rankdata(ys)), self.xs1_rank)

        target_max_value = 5 + 0.01  # close to min
        ys = rescale(self.xs1, target_max_value=target_max_value)
        self.assertAlmostEqual(np.sum(ys), self.xs1_sum)
        self.assertAlmostEqual(np.max(ys), target_max_value)
        self.assertListEqual(list(rankdata(ys)), self.xs1_rank)

    def test_exp_scale_sum(self):
        target_sum = 40 - 0.01  # close to max
        ys = rescale(self.xs1, target_sum=target_sum)
        self.assertAlmostEqual(np.sum(ys), target_sum)
        self.assertAlmostEqual(np.max(ys), self.xs1_max)
        self.assertListEqual(list(rankdata(ys)), self.xs1_rank)

        target_sum = 10 + 0.01  # close to min
        ys = rescale(self.xs1, target_sum=target_sum)
        self.assertAlmostEqual(np.sum(ys), target_sum)
        self.assertAlmostEqual(np.max(ys), self.xs1_max)
        self.assertListEqual(list(rankdata(ys)), self.xs1_rank)

    def test_pow_scale_max(self):
        target_max_value = 20 - 0.01  # close to max
        ys = rescale(self.xs1, target_max_value=target_max_value, method="pow")
        self.assertAlmostEqual(np.sum(ys), self.xs1_sum)
        self.assertAlmostEqual(np.max(ys), target_max_value)
        self.assertListEqual(list(rankdata(ys)), self.xs1_rank)

        target_max_value = 5 + 0.01  # close to min
        ys = rescale(self.xs1, target_max_value=target_max_value, method="pow")
        self.assertAlmostEqual(np.sum(ys), self.xs1_sum)
        self.assertAlmostEqual(np.max(ys), target_max_value)
        self.assertListEqual(list(rankdata(ys)), self.xs1_rank)

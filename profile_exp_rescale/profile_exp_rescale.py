import logging

import numpy as np
import scipy


def rescale(
    values,
    target_sum=None,
    target_max_value=None,
    target_max_rel=None,
    max_value=None,
    tol=1e-10,
):
    """Create rescaled profile.
    Args:
        values(iterable): profile values(>=0)
        target_sum(float, optional): sum of values of result profile.
            If missing, use sum of original data
        target_max_value(float, optional): theoretical maximum  of result profile.
            actual maximum of values may be lower.
            If missing, max_value will be used
        target_max_rel(float, optional): ration of actual/abs maximum in result profile.
            If missing,use ration from input profile
        max_value(float, optional): theoretical maximum
            actual maximum of values may be lower.
            If missing, actual maximum of values will be used
        tol(float, optional)
    Returns:
        array: numpy array with result profile
    """
    xs = np.array(values)
    xs_max = np.max(xs)
    xs_max_abs = max_value or xs_max
    xs_max_rel = xs_max / xs_max_abs
    xs_sum = np.sum(values)

    ys_sum = target_sum or xs_sum
    ys_max_abs = target_max_value or xs_max_abs
    ys_max_rel = target_max_rel or xs_max_rel
    ys_max = ys_max_abs * ys_max_rel

    # normalized (max=1) profile
    xs_norm = xs / xs_max
    ys_sum_norm = ys_sum / ys_max
    ys_norm = rescale_norm(values_norm=xs_norm, target_sum=ys_sum_norm, tol=tol)

    # denormalize result
    ys = ys_norm * ys_max

    # checks
    assert np.isclose(np.max(ys), ys_max)
    assert np.isclose(np.sum(ys), ys_sum)
    assert all(y >= 0 for y in ys)

    return ys


def rescale_norm(values_norm, target_sum, tol=1e-10):
    """Create rescaled profile from normalized profile (max=1).
    Args:
        values_norm(iterable): normalized profile (max=1)
        target_sum(float): sum of values of result profile.
        tol(float, optional)
    Returns:
        array: numpy array with result profile
    """
    xs_count = len(values_norm)
    xs_count_0 = len(values_norm[values_norm == 0])
    xs_count_1 = len(values_norm[values_norm == 1])
    xs_count_var = xs_count - xs_count_0 - xs_count_1
    xs_min = xs_count_1 + tol * xs_count_var
    xs_max = xs_count_1 + (1 - tol) * xs_count_var

    assert all(0 <= x <= 1 for x in values_norm)
    assert xs_count_1 > 0
    assert 0 <= xs_min <= target_sum <= xs_max

    alpha = find_optimal_alpha(values_norm, target_sum, tol)
    ys_norm = rescale_alpha(values_norm, target_sum, alpha, tol)
    return ys_norm


def rescale_exp(values, alpha):
    """Create exponentially rescaled profile with known exponent (alpha)."""
    if alpha:
        e_alpha_1 = 1 / (np.exp(alpha) - 1)
        return (np.exp(values * alpha) - 1) * e_alpha_1
    else:
        return values


def rescale_alpha(values_norm, target_sum, alpha, tol=1e-10):
    """Create exponentially rescaled profile with known exponent (alpha) to target area.
    Args:
        values_norm(iterable): normalized profile (max=1)
        target_sum(float): sum of values of result profile.
        alpha(float)
    Returns:
        array: numpy array with result profile
    """

    values_sum = np.sum(values_norm)
    values_exp = rescale_exp(values_norm, alpha)
    rescaled_sum = np.sum(values_exp)
    if alpha:
        beta = 1 - (values_sum - target_sum) / (values_sum - rescaled_sum)
    else:
        beta = 1

    logging.debug(f"rescale alpha: {alpha}, beta: {beta}")
    assert 0 - tol <= beta <= 1 + tol

    return values_norm * beta + values_exp * (1 - beta)


def find_optimal_alpha(values_norm, target_sum, tol=1e-10):
    """Find optimal alpha (so that beta == 1.0)

    Args:
        values_norm(iterable): normalized profile (max=1)
        target_sum(float): sum of values of result profile.
        tol(float, optional)
    Returns:
        array: numpy array with result profile
    """
    values_sum = np.sum(values_norm)
    if abs(values_sum - target_sum) < tol:
        return 0  # linear

    # create function to get root of
    def f(alpha):
        values_exp = rescale_exp(values_norm, alpha)
        rescaled_sum = np.sum(values_exp)
        sum_delta = rescaled_sum - target_sum
        return sum_delta

    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root_scalar.html#scipy.optimize.root_scalar  # noqa
    bound_alpha = np.log(1e64)
    res = scipy.optimize.root_scalar(f, bracket=(-bound_alpha, bound_alpha))
    assert res.converged
    alpha = res.root

    return alpha

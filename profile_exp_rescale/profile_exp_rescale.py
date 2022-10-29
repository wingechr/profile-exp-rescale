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
    method="exp",
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
        method(str, optional): 'exp' (the default) or 'pow' (not fully tested!!)

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
    ys_norm = rescale_norm(
        values_norm=xs_norm, target_sum=ys_sum_norm, tol=tol, method=method
    )

    # denormalize result
    ys = ys_norm * ys_max

    # checks
    assert np.isclose(np.max(ys), ys_max)
    assert np.isclose(np.sum(ys), ys_sum)
    assert all(y >= 0 for y in ys)

    return ys


def rescale_norm(values_norm, target_sum, tol=1e-10, method="exp"):
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

    alpha = find_optimal_alpha(values_norm, target_sum, tol, method)
    ys_norm = rescale_alpha(values_norm, target_sum, alpha, tol, method)
    return ys_norm


def rescale_exp(values, alpha):
    """Create exponentially rescaled profile with known exponent (alpha)."""
    if alpha:
        base = np.exp(alpha)
        e_alpha_1 = 1 / (base - 1)
        return (np.float_power(base, values) - 1) * e_alpha_1
    else:
        return values.copy()


def rescale_pow(values, alpha):
    """Create power rescaled profile with known base (alpha)."""
    if alpha:
        ## NOTE:  where: only user power for values != 0, otherwise numpy will return inf
        # return np.float_power(values, alpha, where=(values > 0))
        return np.float_power(values, alpha)
    else:
        return values.copy()


def get_rescale_fun(method="exp"):
    if method == "exp":
        return rescale_exp
    elif method == "pow":
        return rescale_pow
    else:
        raise NotImplementedError(method)


def rescale_alpha(values_norm, target_sum, alpha, tol=1e-10, method="exp"):
    """Create exponentially rescaled profile with known exponent (alpha) to target area.
    Args:
        values_norm(iterable): normalized profile (max=1)
        target_sum(float): sum of values of result profile.
        alpha(float)
    Returns:
        array: numpy array with result profile
    """

    values_sum = np.sum(values_norm)
    rescale_fun = get_rescale_fun(method)
    values_rescaled = rescale_fun(values_norm, alpha)
    rescaled_sum = np.sum(values_rescaled)
    if abs(rescaled_sum - values_sum) > tol:
        # linear correction
        # beta: weight of rescaled values, (1-beta): weight of original values
        beta = (values_sum - target_sum) / (values_sum - rescaled_sum)
        assert 0 - tol <= beta <= 1 + tol
        result = values_norm * (1 - beta) + values_rescaled * beta
    else:
        result = values_norm

    # correct for rounding errors
    result[result < 0] = 0
    result[result > 1] = 1

    if abs(np.sum(result) - target_sum) > tol:
        logging.warning(
            "resulting sum slightly off target (because of small precision errors)"
        )

    return result


def find_optimal_alpha(values_norm, target_sum, tol=1e-10, method="exp"):
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
    rescale_fun = get_rescale_fun(method)

    def f(alpha):
        values_rescaled = rescale_fun(values_norm, alpha)
        rescaled_sum = np.sum(values_rescaled)
        sum_delta = rescaled_sum - target_sum
        return sum_delta

    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root_scalar.html#scipy.optimize.root_scalar  # noqa
    if method == "exp":
        bound_alpha = np.log(1e64)
        bracket = (-bound_alpha, bound_alpha)
    elif method == "pow":
        bracket = (tol, 1 / tol)
    else:
        raise NotImplementedError(method)

    res = scipy.optimize.root_scalar(f, bracket=bracket)
    assert res.converged
    alpha = res.root

    return alpha

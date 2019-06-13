"""
scipy.linalg.basic.py中关于线性最小二乘法的实现
scikit-learn工具中的线性回归是以这个方法实现的，出处见sklearn.linear_model.base.py中的
"""
### Linear Least Squares

class LstsqLapackError(LinAlgError):
    pass


def lstsq(a, b, cond=None, overwrite_a=False, overwrite_b=False,
          check_finite=True, lapack_driver=None):
    """
    Compute least-squares solution to equation Ax = b.

    Compute a vector x such that the 2-norm ``|b - A x|`` is minimized.

    Parameters
    ----------
    a : (M, N) array_like
        Left hand side matrix (2-D array).
    b : (M,) or (M, K) array_like
        Right hand side matrix or vector (1-D or 2-D array).
    cond : float, optional
        Cutoff for 'small' singular values; used to determine effective
        rank of a. Singular values smaller than
        ``rcond * largest_singular_value`` are considered zero.
    overwrite_a : bool, optional
        Discard data in `a` (may enhance performance). Default is False.
    overwrite_b : bool, optional
        Discard data in `b` (may enhance performance). Default is False.
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.
    lapack_driver: str, optional
        Which LAPACK driver is used to solve the least-squares problem.
        Options are ``'gelsd'``, ``'gelsy'``, ``'gelss'``. Default
        (``'gelsd'``) is a good choice.  However, ``'gelsy'`` can be slightly
        faster on many problems.  ``'gelss'`` was used historically.  It is
        generally slow but uses less memory.

        .. versionadded:: 0.17.0

    Returns
    -------
    x : (N,) or (N, K) ndarray
        Least-squares solution.  Return shape matches shape of `b`.
    residues : () or (1,) or (K,) ndarray
        Sums of residues, squared 2-norm for each column in ``b - a x``.
        If rank of matrix a is ``< N`` or ``> M``, or ``'gelsy'`` is used,
        this is an empty array. If b was 1-D, this is an (1,) shape array,
        otherwise the shape is (K,).
    rank : int
        Effective rank of matrix `a`.
    s : (min(M,N),) ndarray or None
        Singular values of `a`. The condition number of a is
        ``abs(s[0] / s[-1])``. None is returned when ``'gelsy'`` is used.

    Raises
    ------
    LinAlgError
        If computation does not converge.

    ValueError
        When parameters are wrong.

    See Also
    --------
    optimize.nnls : linear least squares with non-negativity constraint

    """
    a1 = _asarray_validated(a, check_finite=check_finite)
    b1 = _asarray_validated(b, check_finite=check_finite)
    if len(a1.shape) != 2:
        raise ValueError('expected matrix')
    m, n = a1.shape
    if len(b1.shape) == 2:
        nrhs = b1.shape[1]
    else:
        nrhs = 1
    if m != b1.shape[0]:
        raise ValueError('incompatible dimensions')

    driver = lapack_driver
    if driver is None:
        driver = lstsq.default_lapack_driver
    if driver not in ('gelsd', 'gelsy', 'gelss'):
        raise ValueError('LAPACK driver "%s" is not found' % driver)

    lapack_func, lapack_lwork = get_lapack_funcs((driver,
                                                  '%s_lwork' % driver), (a1, b1))
    real_data = True if (lapack_func.dtype.kind == 'f') else False

    if m < n:
        # need to extend b matrix as it will be filled with
        # a larger solution matrix
        if len(b1.shape) == 2:
            b2 = np.zeros((n, nrhs), dtype=lapack_func.dtype)
            b2[:m, :] = b1
        else:
            b2 = np.zeros(n, dtype=lapack_func.dtype)
            b2[:m] = b1
        b1 = b2

    overwrite_a = overwrite_a or _datacopied(a1, a)
    overwrite_b = overwrite_b or _datacopied(b1, b)

    if cond is None:
        cond = np.finfo(lapack_func.dtype).eps

    if driver in ('gelss', 'gelsd'):
        if driver == 'gelss':
            lwork = _compute_lwork(lapack_lwork, m, n, nrhs, cond)
            v, x, s, rank, work, info = lapack_func(a1, b1, cond, lwork,
                                                    overwrite_a=overwrite_a,
                                                    overwrite_b=overwrite_b)

        elif driver == 'gelsd':
            if real_data:
                lwork, iwork = _compute_lwork(lapack_lwork, m, n, nrhs, cond)
                if iwork == 0:
                    # this is LAPACK bug 0038: dgelsd does not provide the
                    # size of the iwork array in query mode.  This bug was
                    # fixed in LAPACK 3.2.2, released July 21, 2010.
                    mesg = ("internal gelsd driver lwork query error, "
                            "required iwork dimension not returned. "
                            "This is likely the result of LAPACK bug "
                            "0038, fixed in LAPACK 3.2.2 (released "
                            "July 21, 2010). ")

                    if lapack_driver is None:
                        # restart with gelss
                        lstsq.default_lapack_driver = 'gelss'
                        mesg += "Falling back to 'gelss' driver."
                        warnings.warn(mesg, RuntimeWarning)
                        return lstsq(a, b, cond, overwrite_a, overwrite_b,
                                     check_finite, lapack_driver='gelss')

                    # can't proceed, bail out
                    mesg += ("Use a different lapack_driver when calling lstsq "
                             "or upgrade LAPACK.")
                    raise LstsqLapackError(mesg)

                x, s, rank, info = lapack_func(a1, b1, lwork,
                                               iwork, cond, False, False)
            else:  # complex data
                lwork, rwork, iwork = _compute_lwork(lapack_lwork, m, n,
                                                     nrhs, cond)
                x, s, rank, info = lapack_func(a1, b1, lwork, rwork, iwork,
                                               cond, False, False)
        if info > 0:
            raise LinAlgError("SVD did not converge in Linear Least Squares")
        if info < 0:
            raise ValueError('illegal value in %d-th argument of internal %s'
                             % (-info, lapack_driver))
        resids = np.asarray([], dtype=x.dtype)
        if m > n:
            x1 = x[:n]
            if rank == n:
                resids = np.sum(np.abs(x[n:]) ** 2, axis=0)
            x = x1
        return x, resids, rank, s

    elif driver == 'gelsy':
        lwork = _compute_lwork(lapack_lwork, m, n, nrhs, cond)
        jptv = np.zeros((a1.shape[1], 1), dtype=np.int32)
        v, x, j, rank, info = lapack_func(a1, b1, jptv, cond,
                                          lwork, False, False)
        if info < 0:
            raise ValueError("illegal value in %d-th argument of internal "
                             "gelsy" % -info)
        if m > n:
            x1 = x[:n]
            x = x1
        return x, np.array([], x.dtype), rank, None
import numpy as np

def related_words(given, n):
    # Separate Words from Vectors
    embeddings_dict = {}
    with open("GloVe_Python/PretrainedVectors/PreTrainedVec1.txt", 'r', encoding="utf-8") as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], "float32")
            embeddings_dict[word] = vector
    if given in embeddings_dict.keys():
        return sorted(embeddings_dict.keys(), key=lambda word: euclidean(embeddings_dict[word], embeddings_dict[given]))[:n]
    else:
        return "No Matches"

##### "SciPy.Spatial.Distance" #####

def _validate_vector(u, dtype=None):
    # XXX Is order='c' really necessary?
    u = np.asarray(u, dtype=dtype, order='c').squeeze()
    # Ensure values such as u=1 and u=[1] still return 1-D arrays.
    u = np.atleast_1d(u)
    if u.ndim > 1:
        raise ValueError("Input vector should be 1-D.")
    return u

def _validate_weights(w, dtype=np.double):
    w = _validate_vector(w, dtype=dtype)
    if np.any(w < 0):
        raise ValueError("Input weights should be all non-negative")
    return w

def minkowski(u, v, p=2, w=None):
    """
    Compute the Minkowski distance between two 1-D arrays.
    The Minkowski distance between 1-D arrays `u` and `v`,
    is defined as
    .. math::
       {||u-v||}_p = (\\sum{|u_i - v_i|^p})^{1/p}.
       \\left(\\sum{w_i(|(u_i - v_i)|^p)}\\right)^{1/p}.
    Parameters
    ----------
    u : (N,) array_like
        Input array.
    v : (N,) array_like
        Input array.
    p : scalar
        The order of the norm of the difference :math:`{||u-v||}_p`.
    w : (N,) array_like, optional
        The weights for each value in `u` and `v`. Default is None,
        which gives each value a weight of 1.0
    Returns
    -------
    minkowski : double
        The Minkowski distance between vectors `u` and `v`.
    Examples
    --------
    >>> from scipy.spatial import distance
    >>> distance.minkowski([1, 0, 0], [0, 1, 0], 1)
    2.0
    >>> distance.minkowski([1, 0, 0], [0, 1, 0], 2)
    1.4142135623730951
    >>> distance.minkowski([1, 0, 0], [0, 1, 0], 3)
    1.2599210498948732
    >>> distance.minkowski([1, 1, 0], [0, 1, 0], 1)
    1.0
    >>> distance.minkowski([1, 1, 0], [0, 1, 0], 2)
    1.0
    >>> distance.minkowski([1, 1, 0], [0, 1, 0], 3)
    1.0
    """
    u = _validate_vector(u)
    v = _validate_vector(v)
    if p < 1:
        raise ValueError("p must be at least 1")
    u_v = u - v
    if w is not None:
        w = _validate_weights(w)
        if p == 1:
            root_w = w
        elif p == 2:
            # better precision and speed
            root_w = np.sqrt(w)
        elif p == np.inf:
            root_w = (w != 0)
        else:
            root_w = np.power(w, 1/p)
        u_v = root_w * u_v
    dist = norm(u_v, ord=p)
    return dist

def euclidean(u, v, w=None):
    """
    Computes the Euclidean distance between two 1-D arrays.
    The Euclidean distance between 1-D arrays `u` and `v`, is defined as
    .. math::
       {||u-v||}_2
       \\left(\\sum{(w_i |(u_i - v_i)|^2)}\\right)^{1/2}
    Parameters
    ----------
    u : (N,) array_like
        Input array.
    v : (N,) array_like
        Input array.
    w : (N,) array_like, optional
        The weights for each value in `u` and `v`. Default is None,
        which gives each value a weight of 1.0
    Returns
    -------
    euclidean : double
        The Euclidean distance between vectors `u` and `v`.
    Examples
    --------
    >>> from scipy.spatial import distance
    >>> distance.euclidean([1, 0, 0], [0, 1, 0])
    1.4142135623730951
    >>> distance.euclidean([1, 1, 0], [0, 1, 0])
    1.0
    """
    return minkowski(u, v, p=2, w=w)

##### SciPy Vector Norm #####

def norm(a, ord=None, axis=None, keepdims=False):
    """
    Matrix or vector norm.
    This function is able to return one of seven different matrix norms,
    or one of an infinite number of vector norms (described below), depending
    on the value of the ``ord`` parameter.
    Parameters
    ----------
    a : (M,) or (M, N) array_like
        Input array. If `axis` is None, `a` must be 1D or 2D.
    ord : {non-zero int, inf, -inf, 'fro'}, optional
        Order of the norm (see table under ``Notes``). inf means NumPy's
        `inf` object
    axis : {int, 2-tuple of ints, None}, optional
        If `axis` is an integer, it specifies the axis of `a` along which to
        compute the vector norms.  If `axis` is a 2-tuple, it specifies the
        axes that hold 2-D matrices, and the matrix norms of these matrices
        are computed.  If `axis` is None then either a vector norm (when `a`
        is 1-D) or a matrix norm (when `a` is 2-D) is returned.
    keepdims : bool, optional
        If this is set to True, the axes which are normed over are left in the
        result as dimensions with size one.  With this option the result will
        broadcast correctly against the original `a`.
    """
    return np.linalg.norm(a, ord, axis, keepdims)
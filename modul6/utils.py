import math
import numpy as np
import json


def _handle_zeros_in_scale(scale, copy=True):
    ''' Makes sure that whenever scale is zero, we handle it correctly.
    This happens in most scalers when we have constant features.'''

    # if we are fitting on 1D arrays, scale might be a scalar
    if np.isscalar(scale):
        if scale == .0:
            scale = 1.
        return scale
    elif isinstance(scale, np.ndarray):
        if copy:
            # New array to avoid side-effects
            scale = scale.copy()
        scale[scale == 0.0] = 1.0
        return scale


def scale(X, axis=0, with_mean=True, with_std=True, copy=True):
    """Standardize a dataset along any axis
    Center to the mean and component wise scale to unit variance.
    Read more in the :ref:`User Guide <preprocessing_scaler>`.
    Parameters
    ----------
    X : {array-like, sparse matrix}
        The data to center and scale.
    axis : int (0 by default)
        axis used to compute the means and standard deviations along. If 0,
        independently standardize each feature, otherwise (if 1) standardize
        each sample.
    with_mean : boolean, True by default
        If True, center the data before scaling.
    with_std : boolean, True by default
        If True, scale the data to unit variance (or equivalently,
        unit standard deviation).
    copy : boolean, optional, default True
        set to False to perform inplace row normalization and avoid a
        copy (if the input is already a numpy array or a scipy.sparse
        CSR matrix and if axis is 1).
    Notes
    -----
    This implementation will refuse to center scipy.sparse matrices
    since it would make them non-sparse and would potentially crash the
    program with memory exhaustion problems.
    Instead the caller is expected to either set explicitly
    `with_mean=False` (in that case, only variance scaling will be
    performed on the features of the CSR matrix) or to call `X.toarray()`
    if he/she expects the materialized dense array to fit in memory.
    To avoid memory copy the caller should pass a CSR matrix.
    See also
    --------
    :class:`sklearn.preprocessing.StandardScaler` to perform centering and
    scaling using the ``Transformer`` API (e.g. as part of a preprocessing
    :class:`sklearn.pipeline.Pipeline`)
    """

    X = np.asarray(X)
    mean_ = 0
    scale_ = 0
    if with_mean:
        mean_ = np.mean(X, axis)
    if with_std:
        scale_ = np.std(X, axis)
    if copy:
        X = X.copy()
    # Xr is a view on the original array that enables easy use of
    # broadcasting on the axis in which we are interested in
    Xr = np.rollaxis(X, axis)
    if with_mean:
        Xr -= mean_
        mean_1 = Xr.mean(axis=0)
        # Verify that mean_1 is 'close to zero'. If X contains very
        # large values, mean_1 can also be very large, due to a lack of
        # precision of mean_. In this case, a pre-scaling of the
        # concerned feature is efficient, for instance by its mean or
        # maximum.
        if not np.allclose(mean_1, 0):
            print("Numerical issues were encountered "
                          "when centering the data "
                          "and might not be solved. Dataset may "
                          "contain too large values. You may need "
                          "to prescale your features.")
            Xr -= mean_1
    if with_std:
        scale_ = _handle_zeros_in_scale(scale_, copy=False)
        Xr /= scale_
        if with_mean:
            mean_2 = Xr.mean(axis=0)
            # If mean_2 is not 'close to zero', it comes from the fact that
            # scale_ is very small so that mean_2 = mean_1/scale_ > 0, even
            # if mean_1 was close to zero. The problem is thus essentially
            # due to the lack of precision of mean_. A solution is then to
            # substract the mean again:
            if not np.allclose(mean_2, 0):
                print("Numerical issues were encountered "
                              "when scaling the data "
                              "and might not be solved. The standard "
                              "deviation of the data is probably "
                              "very close to 0. ")
                Xr -= mean_2
    return X







def read_2048_file(file_path):
    data = []
    with open(file_path) as mini:
        i = 0
        block = {}
        block['board'] = []
        for line in mini:
            if line.find('Move') == 0:
                i += 1
                if block != {'board': []}:
                    block['board'] = np.array(block['board']).flatten().tolist()
                    yield block
                    block = {}
                block['board'] = []
                block['score'] = line.split('=')[1].rstrip('\r\n')
            else:
                # print(line)
                row = line.split(' ')
                flat_board = []
                if len(row) > 1:
                    for item in row:
                        item = item.rstrip('\r\n')
                        if item != '':
                            item = int(item)
                            if item == 0:
                                flat_board.append(0)
                            else:
                                flat_board.append(int(math.log2(int(item))))
                    block['board'].append(flat_board)
                else:
                    item = row[0].rstrip('\r\n')
                    if item != '':
                        block['move'] = int(item)

        block['board'] = np.array(block['board']).flatten().tolist()
        yield block


def write_training_data(in_file, out_file):
    errors = 0
    with open(out_file, 'w') as testorama:
        for block in read_2048_file(in_file):
            try:
                line = '%s, %i, %s\n' % (block['board'], block['move'], block['score'])
                testorama.write(line)
            except KeyError:
                errors += 1
                pass

        print("experienced %s errors" % errors)


def sick_if_bro(x):
    if x == [1, 0, 0, 0]:
        return 0
    elif x == [0, 1, 0, 0]:
        return 1
    elif x == [0, 0, 1, 0]:
        return 2
    elif x == [0, 0, 0, 1]:
        return 3


def sick_log2_bro(flat_board):
    result = []
    for i in range(len(flat_board)):
        if flat_board[i] > 0:
            result.append(int(math.log2(flat_board[i])))
        else:
            result.append(0)
    return result


def interpret_team_hereforbeer(in_file, out_file):
    with open(out_file, 'w+') as out:
        with open(in_file) as data_file:
            data = json.load(data_file)
            for object in data:
                output_str = str(sick_log2_bro(eval(object))) + ', ' + str(sick_if_bro(data[object])) + ', 0\n'
                out.write(output_str)



if __name__ == '__main__':
    interpret_team_hereforbeer('myfile.txt', 'hereforbeer_training.txt')
    # write_training_data('data2.txt', 'new_training_set.txt')

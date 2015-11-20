import theano.tensor as T
import theano
import numpy as np


def scale_images(feature_sets):
    return np.asarray(feature_sets, dtype=theano.config.floatX) / 255.


def rectify(x):
    return T.maximum(x, 0.)

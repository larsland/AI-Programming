import theano.tensor as T
import theano
import numpy as np


def scale_images(feature_sets):
    return np.asarray(feature_sets, dtype=theano.config.floatX) / 255.


def rectify(x):
    return T.maximum(x, 0.)


def prelu(x, alpha=0.5):
    pos = ((x + abs(x)) / 2.0)
    neg = alpha * ((x - abs(x)) / 2.0)
    return pos + neg
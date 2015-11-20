import theano.tensor as T


def preprocess_images(feature_sets):
    for image in range(len(feature_sets)):
        for value in range(len(feature_sets[image])):
            feature_sets[image][value] /= float(255)
    return feature_sets


def rectify(x):
    return T.maximum(x, 0.)

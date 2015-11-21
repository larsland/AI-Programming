<<<<<<< HEAD
from modul5.ann import ANN
import theano.tensor.nnet as Tann
from modul5.utils import rectify

if __name__ == '__main__':
    '''
    Arguments for each configuration:
    1: hidden nodes in each hidden layer
    2: activation functions in each layer
    3: learning rate
    4: batch size
    5: number of hidden layers
    6: number of epochs
    7: error function for backpropagation
    '''

    ann1 = ANN([50], [Tann.softplus, Tann.softplus, Tann.softmax], 0.01, 50, 1, 10, 'sum')
    ann2 = ANN([50, 50], [rectify, rectify, rectify, Tann.softmax], 0.01, 100, 2, 5, 'sum')
    ann3 = ANN([100], [Tann.sigmoid, Tann.sigmoid, Tann.sigmoid], 0.001, 50, 1, 5, 'sum')
    ann4 = ANN([30, 40, 50], [Tann.softplus, Tann.softplus, Tann.softplus, Tann.softplus, Tann.softplus], 0.01, 50, 3, 10, 'sum')

    ann1.run()

=======
import pickle
import gzip
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def load_data():
    f = gzip.open('modul5/mnist.pkl.gz', 'rb')
    training_data, validation_data, test_data = pickle.load(f, encoding='latin1')
    f.close()
    return (training_data, validation_data, test_data)


def load_data_wrapper():
    tr_d, va_d, te_d = load_data()
    training_inputs = [np.reshape(x, (784, 1)) for x in tr_d[0]]
    training_results = [vectorized_result(y) for y in tr_d[1]]
    training_data = zip(training_inputs, training_results)
    validation_inputs = [np.reshape(x, (784, 1)) for x in va_d[0]]
    validation_data = zip(validation_inputs, va_d[1])
    test_inputs = [np.reshape(x, (784, 1)) for x in te_d[0]]
    test_data = zip(test_inputs, te_d[1])
    return (training_data, validation_data, test_data)


def vectorized_result(j):
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e


def get_images(training_set):
    """ Return a list containing the images from the MNIST data
    set. Each image is represented as a 2-d numpy array."""
    flattened_images = training_set[0]
    return [np.reshape(f, (-1, 28)) for f in flattened_images]


def plot_mnist_digit(image):
    """ Plot a single MNIST image."""
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.matshow(image, cmap=cm.binary)
    plt.xticks(np.array([]))
    plt.yticks(np.array([]))
    plt.show()


def plot_10_by_10_images(images):
    """ Plot 100 MNIST images in a 10 by 10 table. Note that we crop
    the images so that they appear reasonably close together.  The
    image is post-processed to give the appearance of being continued."""
    fig = plt.figure()
    images = [image[3:25, 3:25] for image in images]
    #image = np.concatenate(images, axis=1)
    for x in range(0, 10):
        for y in range(0, 10):
            pos = 10*y+x + 1
            ax = fig.add_subplot(10, 10, pos)
            ax.matshow(images[10*y+x - 1], cmap=cm.binary)
            plt.xticks(np.array([]))
            plt.yticks(np.array([]))
    plt.show()


# Load the dataset
train_set, valid_set, test_set = load_data()

images = get_images(train_set)
plot_10_by_10_images(images[0::9])

'''

def shared_dataset(data_xy):
    """ Function that loads the dataset into shared variables

    The reason we store our dataset in shared variables is to allow
    Theano to copy it into the GPU memory (when code is run on GPU).
    Since copying data into the GPU is slow, copying a minibatch everytime
    is needed (the default behaviour if the data is not in a shared
    variable) would lead to a large decrease in performance.
    """
    data_x, data_y = data_xy
    shared_x = theano.shared(np.asarray(data_x, dtype=theano.config.floatX))
    shared_y = theano.shared(np.asarray(data_y, dtype=theano.config.floatX))
    # When storing data on the GPU it has to be stored as floats
    # therefore we will store the labels as ``floatX`` as well
    # (``shared_y`` does exactly that). But during our computations
    # we need them as ints (we use labels as index, and if they are
    # floats it doesn't make sense) therefore instead of returning
    # ``shared_y`` we will have to cast it to int. This little hack
    # lets us get around this issue
    return shared_x, T.cast(shared_y, 'int32')

test_set_x, test_set_y = shared_dataset(test_set)
valid_set_x, valid_set_y = shared_dataset(valid_set)
train_set_x, train_set_y = shared_dataset(train_set)

batch_size = 500    # size of the minibatch

# accessing the third minibatch of the training set

data  = train_set_x[2 * batch_size: 3 * batch_size]
label = train_set_y[2 * batch_size: 3 * batch_size]

'''
>>>>>>> 413913e2d78844f3aee346c4856df49e0b3ddb9a

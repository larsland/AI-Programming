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


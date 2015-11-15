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
    '''

    ann1 = ANN([50], [Tann.softplus, Tann.softplus, Tann.softmax], 0.005, 50, 1, 10)
    ann2 = ANN([100, 100], [Tann.softplus, rectify, rectify, Tann.softmax], 0.003, 50, 2, 30)

    ann1.run()
    #ann2.run()

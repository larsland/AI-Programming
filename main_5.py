from modul5.ann import ANN
import theano.tensor as tensor
import theano.tensor.nnet as Tann
from modul5.basics.mnist_basics import *

from modul5.utils import rectify

if __name__ == '__main__':
    '''
    Arguments for each configuration:
    1: Number of the ANN
    2: The images
    3: The test images
    4: hidden nodes in each hidden layer
    5: activation functions in each layer
    6: learning rate
    7: batch size
    8: number of hidden layers
    9: number of epochs
    10: error function for backpropagation
    '''

    cases = gen_flat_cases(60000)
    test_cases = gen_flat_cases(10000, type="testing")
    '''
    ann1 = ANN(1, cases, test_cases, [535], [Tann.softplus, Tann.softplus, Tann.softmax], 0.001, 50, 1, 8, 'sum')
    ann2 = ANN(2, cases, test_cases, [535], [Tann.softplus, Tann.softplus, Tann.softmax], 0.001, 100, 1, 2, 'mean')
    ann3 = ANN(3, cases, test_cases, [50, 50], [rectify, rectify, rectify, Tann.softmax], 0.01, 100, 2, 5, 'sum')
    ann4 = ANN(4, cases, test_cases, [200], [rectify, Tann.sigmoid, Tann.sigmoid], 0.001, 50, 1, 5, 'sum')
    ann5 = ANN(5, cases, test_cases, [30, 40, 50], [Tann.softplus, Tann.softplus, Tann.softplus, Tann.softplus, Tann.softplus], 0.01, 50, 3, 10, 'sum')
    '''

<<<<<<< HEAD
    ann1 = ANN(1, cases, test_cases, [535], [Tann.softplus, Tann.softplus, Tann.softmax], 0.001, 100, 1, 20, 'mean')
    ann2 = ANN(2, cases, test_cases, [535], [Tann.softplus, Tann.softplus, Tann.softmax], 0.001, 100, 1, 20, 'sum')
    ann3 = ANN(3, cases, test_cases, [100, 100], [rectify, rectify, rectify, Tann.softmax], 0.002, 100, 2, 20, 'mean')
    ann4 = ANN(4, cases, test_cases, [200], [rectify, Tann.sigmoid, Tann.sigmoid], 0.001, 50, 1, 20, 'sum')
    ann5 = ANN(5, cases, test_cases, [60, 80, 100], [Tann.softplus, Tann.softplus, Tann.softplus, Tann.softplus, Tann.softplus], 0.01, 50, 3, 20, 'sum')
=======
    #ann1 = ANN(1, cases, test_cases, [535], [Tann.softplus, Tann.softplus, Tann.softmax], 0.001, 100, 20, 'mean')
    ann2 = ANN(2, cases, test_cases, [535], [Tann.softplus, Tann.softplus, Tann.softmax], 0.001, 100, 20, 'sum')
    #ann3 = ANN(3, cases, test_cases, [100, 100], [rectify, rectify, rectify, Tann.softmax], 0.002, 100, 20, 'mean')
    #ann4 = ANN(4, cases, test_cases, [200], [rectify, Tann.sigmoid, Tann.sigmoid], 0.001, 50, 20, 'sum')
    #ann5 = ANN(5, cases, test_cases, [60, 80, 100], [Tann.softplus, Tann.softplus, Tann.softplus, Tann.softplus, Tann.softplus], 0.01, 50, 20, 'sum')
>>>>>>> 633f72a969f97332c3047222d2c4aae105a3b950



    #ann6 = ANN(6, cases, test_cases, [535], [tensor.tanh, tensor.tanh, Tann.softmax], 0.001, 100, 20, 'mean')

    #ann6.run()
    #ann1.run()
    ann2.run()
    #ann3.run()
    #ann4.run()
    #ann5.run()



from modul5.basics.mnist_basics import *
import theano
import numpy as np
import theano.tensor as T
import math
from modul5.utils import scale_images, rectify

nr_of_training_images = 60000
nr_of_testing_images = 10000
input_nodes = 784


class ANN:
    def __init__(self, nn, cases, test_cases, hidden_nodes, activation_functions, learning_rate, batch_size, epochs, error_func):
        self.images, self.labels = cases
        self.test_images, self.test_labels = test_cases
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.hidden_nodes = hidden_nodes
        self.act_funcs = activation_functions
        self.num_hidden_layers = len(activation_functions) - 2
        self.epochs = epochs
        self.error_func = error_func
        self.net_number = nn

        self.build_network()

    def build_network(self):
        input = T.fmatrix()
        target = T.fmatrix()
        weights = []
        layers = []

        # Setting weights for each layer
        weights.append(theano.shared(np.random.uniform(low=-.1, high=.1, size=(input_nodes, self.hidden_nodes[0]))))
        for i in range(1, self.num_hidden_layers):
            weights.append(theano.shared(np.random.uniform(low=-.1, high=.1, size=(self.hidden_nodes[i-1], self.hidden_nodes[i]))))
        weights.append(theano.shared(np.random.uniform(low=-.1, high=.1, size=(self.hidden_nodes[-1], 10))))

        # Creating all layers with respective activation functions
        layers.append(self.act_funcs[0](T.dot(input, weights[0])))
        for i in range(1, self.num_hidden_layers):
            layers.append(self.act_funcs[i](T.dot(layers[i-1], weights[i])))
        layers.append(self.act_funcs[-1](T.dot(layers[-1], weights[-1])))

        # Choosing error function
        if self.error_func == 'sum':
            error_function = T.sum(pow((target - layers[-1]), 2))
        elif self.error_func == 'mean':
            error_function = T.mean(T.nnet.categorical_crossentropy(layers[-1], target))
        else:
            error_function = None

        params = list(weights)
        gradients = T.grad(error_function, params)

        self.train = theano.function(inputs=[input, target], outputs=error_function, updates=self.rms_prop(params, gradients),
                                     allow_input_downcast=True)
        self.predict = theano.function(inputs=[input], outputs=layers[-1], allow_input_downcast=True)

    def rms_prop(self, params, gradients, rho=0.9, epsilon=1e-6):
        updates = []
        for p, g in zip(params, gradients):
            acc = theano.shared(p.get_value() * 0.)
            acc_new = rho * acc + (1 - rho) * g ** 2
            gradient_scaling = T.sqrt(acc_new + epsilon)
            g = g / gradient_scaling
            updates.append((acc, acc_new))
            updates.append((p, p - self.learning_rate * g))
        return updates

    def train_network(self, errors):
        with open("modul5/stats/test" + str(self.net_number) + '.txt', 'w+') as target:
            for i in range(self.epochs):
                print('-'*35 + '\n' + "epoch: " + str(i) + '\n' + '-'*35)
                error = 0
                i = 0
                j = self.batch_size
                while j < len(self.images):
                    image_group = self.images[i:j]
                    result_group = [[0 for i in range(10)] for i in range(self.batch_size)]
                    for k in range(self.batch_size):
                        label_index = self.labels[i + k]
                        result_group[k][label_index] = 1
                    i += self.batch_size
                    j += self.batch_size
                    if j % (self.batch_size * 100) == 0:
                        print("image nr: ", j)
                    error += self.train(image_group, result_group)
                print("(average error per image: " + str('%.5f' % (error/j)) + ')')
                errors.append(error)
                self.write_results(target)

    def write_results(self, target):
        res_test = self.test_on_testing_images()
        target.write(str(res_test))
        #res_train = self.test_on_training_images()
        #res_test = self.test_on_testing_images()
        #target.write(str(res_train))
        target.write('\n')
        #target.write(str(res_test))
        # target.write('\n')
        #target.write('\n')

    def test_on_testing_images(self):
        labels = []
        count = 0
        for i in range(len(self.test_images)):
            label = self.predict([self.test_images[i]])
            labels.append(label)
        for i in range(len(labels)):
            b = int(self.test_labels[i]) == np.argmax(labels[i])
            if b:
                count += 1
        print("Correct classification on testing images:", '%.5f' % ((count/float(len(self.test_labels))) * 100))
        return('%.5f' % ((count/float(len(self.test_labels))) * 100))

    def test_on_training_images(self):
        labels = []
        count = 0
        for i in range(len(self.images)):
            label = self.predict([self.images[i]])
            labels.append(label)
        for i in range(len(labels)):
            b = int(self.labels[i] == np.argmax(labels[i]))
            if b:
                count += 1
        print("Correct classification on training images:", '%.5f' % ((count/float(len(self.labels))) * 100))
        return('%.5f' % ((count/float(len(self.labels))) * 100))

    def blind_test(self, feature_sets):
        feature_sets = scale_images(feature_sets)
        labels = []

        for i in range(len(feature_sets)):
            label = np.argmax(self.predict([feature_sets[i]])).tolist()
            labels.append(label)
        return labels

    def run(self):
        self.images = scale_images(self.images)
        self.test_images = scale_images(self.test_images)
        errors = []

        self.train_network(errors)

        '''
        while True:
            print('-'*35 + '\n' + '1: Train' + '\n' + '2: Test on testing images' + '\n' +
                  '3: Test on training images' + '\n' + '4: Blind Test' + '\n' + '5: Exit' + '\n' + '-'*35)
            key_input = int(input("Input: "))
            if key_input == 1:
                self.train_network(errors)
            elif key_input == 2:
                self.test_on_testing_images()
            elif key_input == 3:
                self.test_on_training_images()
            elif key_input == 4:
                minor_demo(self)
            elif key_input == 5:
                quit(0)
        '''












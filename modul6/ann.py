import theano
import numpy as np
import theano.tensor as T

input_nodes = 16

class ANN:
    def __init__(self, hidden_nodes, activation_functions, learning_rate, batch_size, hidden_layers, epochs, error_func):
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.hidden_nodes = hidden_nodes
        self.act_funcs = activation_functions
        self.num_hidden_layers = hidden_layers
        self.epochs = epochs
        self.error_func = error_func

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

    def train_network(self):
        for i in range(self.epochs):
            print('-'*35 + '\n' + "epoch: " + str(i) + '\n' + '-'*35)
            error = 0
            i = 0
            j = self.batch_size
            while j < len(60000):
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

    def run(self):
        self.train_network()













import theano
import numpy as np
import theano.tensor as T

input_nodes = 32
output_nodes = 4


class ANN:
    def __init__(self, states, labels, scores, hidden_nodes, activation_functions, learning_rate, batch_size, epochs, error_func):
        self.scores = scores
        self.states = states
        self.labels = labels
        self.input_nodes = len(states[0])
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.hidden_nodes = hidden_nodes
        self.act_funcs = activation_functions
        self.num_hidden_layers = len(activation_functions) - 2
        self.epochs = epochs
        self.error_func = error_func
        self.build_network()

    def build_network(self):
        input = T.fmatrix()
        target = T.fmatrix()
        weights = []
        layers = []

        # Setting weights for each layer
        weights.append(theano.shared(np.random.uniform(low=-.1, high=.1, size=(self.input_nodes, self.hidden_nodes[0]))))
        for i in range(1, self.num_hidden_layers):
            weights.append(theano.shared(np.random.uniform(low=-.1, high=.1, size=(self.hidden_nodes[i-1], self.hidden_nodes[i]))))
        weights.append(theano.shared(np.random.uniform(low=-.1, high=.1, size=(self.hidden_nodes[-1], output_nodes))))

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

    def back_prop(self, params, gradients):
        updates = []
        for p, g in zip(params, gradients):
            updates.append((p, p - self.learning_rate * g))
        return updates

    def train_network(self):
        for i in range(self.epochs):
            print('-'*35 + '\n' + "epoch: " + str(i+1) + '\n' + '-'*35)
            error = 0
            i = 0
            j = self.batch_size
            while j < len(self.states):
                state_batch = self.states[i:j]
                label_batch = [[0 for i in range(output_nodes)] for i in range(self.batch_size)]
                for k in range(self.batch_size):
                    label_index = self.labels[i + k]
                    label_batch[k][label_index] = 1
                i += self.batch_size
                j += self.batch_size
                if j % (self.batch_size * 100) == 0:
                    print("Move nr: ", j)
                error += self.train(state_batch, label_batch)
            print("(average error per image: " + str('%.5f' % (error/j)) + ')')

    def test_on_training_states(self):
        labels = []
        count = 0
        for i in range(len(self.states)):
            label = self.predict([self.states[i]])
            labels.append(label)
        for i in range(len(labels)):
            b = int(self.labels[i] == np.argmax(labels[i]))
            if b:
                count += 1
        print("Correct classification on training images:", '%.5f' % ((count/float(len(self.labels))) * 100))
        return('%.5f' % ((count/float(len(self.labels))) * 100))

    def predict_move(self, state):
        return np.argmax(self.predict([state]))

    def predict_next_move(self, state):
        return self.predict([state])

    def run(self):
        self.train_network()
        self.test_on_training_states()

















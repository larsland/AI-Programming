from modul5.mnist_basics import *
from time import time
import theano
import numpy as np
import theano.tensor as T
import theano.tensor.nnet as Tann

nr_of_training_images = 60000
nr_of_testing_images = 10000
input_nodes = 28*28


class ImageRecognizer:
    def __init__(self, hidden_nodes, activation_functions, learning_rate, batch_size, hidden_layers):
        self.images, self.labels = gen_flat_cases(nr_of_training_images)
        self.test_images, self.test_labels = gen_flat_cases(nr_of_testing_images, type="testing")
        self.lrate = learning_rate
        self.batch_size = batch_size
        self.hidden_nodes = hidden_nodes
        self.act_funcs = activation_functions
        self.num_hidden_layers = hidden_layers

        self.build_network()

    # Setting default Theano bit width
    def floatX(self, X):
        return np.asarray(X, dtype=theano.config.floatX)

    def build_network(self):
        input = T.fmatrix()
        target = T.fmatrix()
        weights = []
        layers = []

        # Weight matrix for input layer
        weights.append(theano.shared(np.random.uniform(low=-.1, high=.1, size=(input_nodes, self.hidden_nodes[0]))))

        # Weight matrices for hidden layers
        for i in range(1, self.num_hidden_layers):
            weights.append(theano.shared(np.random.uniform(low=-.1, high=.1, size=(self.hidden_nodes[i-1], self.hidden_nodes[i]))))

        # Weight matrix for output layer
        weights.append(theano.shared(np.random.uniform(low=-.1, high=.1, size=(self.hidden_nodes[-1], 10))))
        
        input_layer = self.act_funcs[0](T.dot(input, weights[0]))
        layers.append(input_layer)

        for i in range(1, self.num_hidden_layers):
            layers.append(self.act_funcs[i](T.dot(layers[i-1], weights[i])))

        output_layer = self.act_funcs[-1](T.dot(layers[-1], weights[-1]))
        layers.append(output_layer)

        error = T.sum(pow((target - output_layer), 2))
        params = list(weights)
        gradients = T.grad(error, params)

        self.train = theano.function(inputs=[input, target], outputs=error, updates=self.rms_prop(params, gradients),
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
            updates.append((p, p - self.lrate * g))
        return updates

    def train_network(self, epochs=1, test_interval=None, errors=[]):
        starttime = time()
        for i in range(epochs):
            print("epoch: ", i)
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
            print(error)
            print("Avg error per image: " + str(error/j))
            errors.append(error)
        print("Training time: " + str((time()-starttime)) + " sec")
        return errors

    def test_network(self, nr_of_testing_images=10000, scatter=True, blind_test_images=None):
        if blind_test_images is not None:
            self.test_images = blind_test_images
            self.test_labels = None

        hidden_activations = []
        i = 0
        j = self.batch_size
        while j < len(self.test_images):
            image_group = self.test_images[i:j]
            i += self.batch_size
            j += self.batch_size
            end = self.predict(image_group)
            for res in end:
                hidden_activations.append(res)

        self.check_result(hidden_activations)
        return self.test_labels, hidden_activations

    def blind_test(self, images):
        #Raw images is a list with sublist of raw_images
        self.preprosess_images(images)
        raw_results = self.test_network(blind_test_images=images)
        results = []
        for i in range(len(raw_results)):
            highest_value = int(np.where(raw_results[i] == max(raw_results[i]))[0][0])
            results.append(highest_value)
        #Returns a list with the classifications of the images
        return results

    def preprosess_images(self, feature_sets):
        # Scales images to have values between 0.0 and 1.0 instead of 0 and 255
        for image in range(len(feature_sets)):
            for value in range(len(feature_sets[image])):
                feature_sets[image][value] = feature_sets[image][value]/float(255)

    def check_result(self, result):
        count = 0
        for i in range(len(result)):
            b = int(self.test_labels[i]) == np.argmax(result[i])
            if b:
                count += 1
        print("Correct classification:", (count/float(len(self.test_labels))) * 100)
        
    def run(self):
        self.preprosess_images(self.images)
        self.preprosess_images(self.test_images)
    
        errors = []
        start_time = time()
    
        errors = self.train_network(epochs=10, errors=errors)
    
        test_labels, result = self.test_network(nr_of_testing_images=nr_of_testing_images)
        print("Total time elapsed: " + str((time() - start_time)/60) + " min")
        
        
        

if __name__ == '__main__':
    # hidden nodes in each hidden layer, activation function in each layer, learning rate, batch size, hidden layers
    ann1 = ImageRecognizer([20, 100, 100], [Tann.softplus, Tann.softplus, Tann.softplus, Tann.softplus, Tann.softplus],
                           0.01, 50, 3)

    ann1.run()


   



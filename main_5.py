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
    def __init__(self, hidden_nodes, learning_rate, batch_size, hidden_layers):
        self.images, self.labels = gen_flat_cases(nr_of_training_images)
        self.test_images, self.test_labels = gen_flat_cases(nr_of_testing_images, type="testing")
        self.lrate = learning_rate
        self.batch_size = batch_size
        self.hidden_nodes = hidden_nodes
        self.hidden_layers = hidden_layers

        self.build_ann()

    # Setting default Theano bit width
    def floatX(self, X):
        return np.asarray(X, dtype=theano.config.floatX)

    def build_ann(self):
        input = T.fmatrix()
        target = T.fmatrix()

        weights = []
        weights.append(theano.shared(np.random.uniform(low=-.1, high=.1, size=(input_nodes, self.hidden_nodes[0]))))
        weights.append(theano.shared(np.random.uniform(low=-.1, high=.1, size=(self.hidden_nodes[0], self.hidden_nodes[1]))))
        weights.append(theano.shared(np.random.uniform(low=-.1, high=.1, size=(self.hidden_nodes[1], self.hidden_nodes[2]))))
        weights.append(theano.shared(np.random.uniform(low=-.1, high=.1, size=(self.hidden_nodes[2], 10))))

        activation_1 = Tann.softplus(T.dot(input, weights[0]))
        activation_2 = Tann.softplus(T.dot(activation_1, weights[1]))
        activation_3 = Tann.softplus(T.dot(activation_2, weights[2]))
        activation_4 = Tann.softmax(T.dot(activation_3, weights[3]))

        error = T.sum(pow((target - activation_4), 2))
        params = [weights[0], weights[1], weights[2], weights[3]]
        gradients = T.grad(error, params)

        self.get_x1 = theano.function(inputs=[input, target], outputs=error, allow_input_downcast=True)
        self.train = theano.function(inputs=[input, target], outputs=error, updates=self.RMSprop(params, gradients),
                                     allow_input_downcast=True)
        self.predict = theano.function(inputs=[input], outputs=activation_4, allow_input_downcast=True)

    def RMSprop(self, params, gradients, rho=0.9, epsilon=1e-6):
        updates = []
        for p, g in zip(params, gradients):
            acc = theano.shared(p.get_value() * 0.)
            acc_new = rho * acc + (1 - rho) * g ** 2
            gradient_scaling = T.sqrt(acc_new + epsilon)
            g = g / gradient_scaling
            updates.append((acc, acc_new))
            updates.append((p, p - self.lrate * g))
        return updates

    def do_training(self, epochs=1, test_interval=None, errors=[]):
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

    def do_testing(self, nr_of_testing_images=10000, scatter=True, blind_test_images=None):
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
        self.preprosessing(images)
        raw_results = self.do_testing(blind_test_images=images)
        results = []
        for i in range(len(raw_results)):
            highest_value = int(np.where(raw_results[i] == max(raw_results[i]))[0][0])
            results.append(highest_value)
        #Returns a list with the classifications of the images
        return results

    def preprosessing(self, feature_sets):
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

if __name__ == '__main__':
    # input nodes, hidden nodes, learning rate, batch size, hidden layers
    image_recog = ImageRecognizer([20, 100, 30], 0.01, 50, 3)

    image_recog.preprosessing(image_recog.images)
    image_recog.preprosessing(image_recog.test_images)

    errors = []
    start_time = time()

    errors = image_recog.do_training(epochs=20, errors=errors)

    test_labels, result = image_recog.do_testing(nr_of_testing_images=nr_of_testing_images)
    print("Total time elapsed: " + str((time() - start_time)/60) + " min")



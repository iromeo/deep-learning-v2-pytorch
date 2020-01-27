import numpy as np


class NeuralNetwork(object):
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        # Set number of nodes in input, hidden and output layers.
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # Initialize weights
        self.weights_input_to_hidden = np.random.normal(
            0.0, self.input_nodes ** -0.5,
            (self.input_nodes, self.hidden_nodes)
        )

        self.weights_hidden_to_output = np.random.normal(
            0.0, self.hidden_nodes ** -0.5,
            (self.hidden_nodes, self.output_nodes)
        )
        self.lr = learning_rate

        # Activation function for hidden layer:
        # * sigmoid function
        self.activation_function = lambda x: 1 / (1 + np.exp(-x))

        # * 'optimized' sigmoid function derivative, reuse 'output = sigmoid(x)' here:
        self.activation_function_output_2_derivative = lambda output: output * (1 - output)

    def train(self, features, targets):
        """ Train the network on batch of features and targets.

            Arguments
            ---------

            features: 2D array, each row is one data record, each column is a feature
            targets: 1D array of target values

        """
        n_records = features.shape[0]
        delta_weights_i_h = np.zeros(self.weights_input_to_hidden.shape)
        delta_weights_h_o = np.zeros(self.weights_hidden_to_output.shape)

        for X, y in zip(features, targets):
            # for convenience represent X vector as a Nx1 matix
            x = X[None, :]

            # forward pass 
            final_outputs, hidden_outputs = self.forward_pass_train(x)

            # backpropagation
            delta_weights_i_h, delta_weights_h_o = self.backpropagation(
                final_outputs, hidden_outputs, x, y, delta_weights_i_h, delta_weights_h_o
            )

        # update weights    
        self.update_weights(delta_weights_i_h, delta_weights_h_o, n_records)

    def forward_pass_train(self, X):
        """ Implement forward pass here

            Arguments
            ---------
            X: features batch

        """

        # ### Forward pass ###

        # Hidden layer

        # * signals into hidden layer
        hidden_inputs = np.dot(X, self.weights_input_to_hidden)

        # * signals from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)

        # Output layer

        # * signals into final output layer
        final_inputs = np.dot(hidden_outputs, self.weights_hidden_to_output)

        # * signals from final output layer, use f(x) activation function for this layer
        final_outputs = final_inputs

        return final_outputs, hidden_outputs

    def backpropagation(self, final_outputs, hidden_outputs, X, y, delta_weights_i_h, delta_weights_h_o):
        """ Implement backpropagation

            Arguments
            ---------
            final_outputs: output from forward pass
            hidden_outputs: output form hidden pass
            X: features batch
            y: target (i.e. label) batch
            delta_weights_i_h: change in weights from input to hidden layers
            delta_weights_h_o: change in weights from hidden to output layers

        """

        # ### Backward pass ###

        # Output error: difference between desired target and actual output.
        error = y - final_outputs
        output_error_term = error  # activation function is f(x), f'(x) = 1

        # Backpropagate error:
        # * Hidden layer's contribution to the error
        hidden_error = np.dot(output_error_term, self.weights_hidden_to_output.T)
        hidden_error_term = hidden_error * self.activation_function_output_2_derivative(hidden_outputs)

        # Weight step (input to hidden)
        delta_weights_i_h += np.dot(X.T, hidden_error_term)

        # Weight step (hidden to output)
        delta_weights_h_o += np.dot(hidden_outputs.T, output_error_term)

        return delta_weights_i_h, delta_weights_h_o

    def update_weights(self, delta_weights_i_h, delta_weights_h_o, n_records):
        """ Update weights on gradient descent step

            Arguments
            ---------
            delta_weights_i_h: change in weights from input to hidden layers
            delta_weights_h_o: change in weights from hidden to output layers
            n_records: number of records

        """
        # update hidden-to-output weights with gradient descent step
        self.weights_hidden_to_output += self.lr * delta_weights_h_o / n_records

        # update input-to-hidden weights with gradient descent step
        self.weights_input_to_hidden += self.lr * delta_weights_i_h / n_records

    def run(self, features):
        """ Run a forward pass through the network with input features

            Arguments
            ---------
            features: 1D array of feature values
        """

        # #### Implement the forward pass here ####

        # Let's reuse exising code in order not to duplicate it:
        final_outputs, _ = self.forward_pass_train(features)

        # If this project assumes copy-paste of forward pass, so the solution is below:
        #
        # # Hidden layer
        # hidden_inputs = np.dot(features, self.weights_input_to_hidden) # signals into hidden layer
        # hidden_outputs = self.activation_function(hidden_inputs) # signals from hidden layer

        # # Output layer
        # # * signals into final output layer
        # final_inputs = np.dot(hidden_outputs, self.weights_hidden_to_output)

        # # * signals from final output layer 
        # final_outputs = final_inputs # activation function is f(x)

        return final_outputs


#########################################################
# Set your hyperparameters here
##########################################################
iterations = 11000
learning_rate = 0.3
hidden_nodes = 5
output_nodes = 1
seed = 21

np.random.seed(seed)

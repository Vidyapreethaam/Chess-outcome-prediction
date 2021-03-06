
   #MLP implementation for the built dataset

   import argparse
   import h5py
   import numpy as np
   import tensorflow as tf
   from sklearn import metrics
   import matplotlib.pyplot as plt
   import sys

   sys.path.extend(['.', '..'])
   import build_dataset

    # For logging and summaries.
    LOG_EVERY_N_ITER = 50
    DEFAULT_BATCH_SIZE = 100
    DEFAULT_NUM_EPOCHS = 5
    TRAINING_SPLIT = 0.8
    LEARNING_RATE = 0.001
    DROPOUT_RATE = 0.4
    # If True, this will change the one-hot index values to be more analogous to a pixel value.
    MODIFY_ONE_HOT_INDICES = True
    NUM_CLASSES = 2
    PIXEL_VALUE_SCALING_FACTOR = 255 / 12

    tf.logging.set_verbosity(tf.logging.INFO)


    def convert_index_value(i):
    """Returns a new one-hot index that more closely matches a pixel
    representation of the label. Empty space is mapped to the middle
    value, and on either sides piece indices are reflected with the
    highest values furthest from center."""
    piece = build_dataset.ONE_HOT_INDICES[i]
        result_indices = ['K', 'Q', 'R', 'B', 'N', 'P', None, 'p', 'n', 'b', 'r', 'q', 'k']
        return result_indices.index(piece) * PIXEL_VALUE_SCALING_FACTOR

   #parameters
    learning rate = 0.001
    training_epochs = 15
    batch_size = 100
    display_step = 1

    
    #network paramters
    n_hidden_1 = 256
    n_hideen_2 = 256
    n_input = 784
    n_classes = 10

    #tf graph input
    X = tf.placeholder("float", [None, n_input])
    Y = tf.placeholder("float", [None, n_classes])

    # Store layers weight & bias
    weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]))}
   
    biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_classes]))}


# Create model
def multilayer_perceptron(x):
    # Hidden fully connected layer with 256 neurons
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    # Hidden fully connected layer with 256 neurons
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    # Output fully connected layer with a neuron for each class
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer

# Construct model
logits = multilayer_perceptron(X)

# Define loss and optimizer
loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
    logits=logits, labels=Y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
train_op = optimizer.minimize(loss_op)
# Initializing the variables
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)

    # Training cycle
    for epoch in range(training_epochs):
        avg_cost = 0.
        total_batch = int(build_dataset.train.num_examples/batch_size)
        # Loop over all batches
        for i in range(total_batch):
            batch_x, batch_y = build_dataset.train.next_batch(batch_size)
            # Run optimization op (backprop) and cost op (to get loss value)
            _, c = sess.run([train_op, loss_op], feed_dict={X: batch_x,
                                                            Y: batch_y})
            # Compute average loss
            avg_cost += c / total_batch
        # Display logs per epoch step
        if epoch % display_step == 0:
            print("Epoch:", '%04d' % (epoch+1), "cost={:.9f}".format(avg_cost))
    print("Optimization Finished!")

    # Test model
    pred = tf.nn.softmax(logits)  # Apply softmax to logits
    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(Y, 1))
    # Calculate accuracy
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print("Accuracy:", accuracy.eval({X: build_dataset.test.images, Y: build_dataset.test.labels}))

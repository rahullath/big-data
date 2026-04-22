# LM Big Data Management in Finance (36320) Birmingham Business School 

<!-- image -->

# Artificial Neural Network-Basics (ANN) 

<!-- image -->

Biological motivation 

<!-- image -->

Biological motivation Algorithm 

<!-- image -->

- Input layer: accepts the data vector or pattern
- Hidden layers: They accept the output from the previous layer, weight them, and pass through a, normally, non-linear activation function.
- Output layer: takes the output from the final hidden layer weights them, and possibly pass through an output nonlinearity, to produce the target values

# Artificial neural networks

- Artificial neural networks( ANNs)
-  Are composed of multiple artificial neuron nodes, which imitate biological neurons of the human brain. 
- Unlike biological neurons, there is only one type of link that connects one neuron to others. 
- The neurons take input data and simple operations are performed on those data. 
- The result of these operations is passed to other neurons. 
- Whether the result will be passed, is determined by the activation function
- The activation function plays an important role for both feature extraction and classification.
- Artificial Neural Networks are capable of learning non-linear functions. 

# Activation functions

- 
- Each neuron performs a dot product with the input (xi) and its weights (wi) , adds the bias and applies the non-linearity or activation function.
-  The activation function of ANNs helps in learning any complex relationship between input and output. 

<!-- image -->

<!-- image -->

ANN to Deep Neural Net (DNN)

<!-- image -->

# Deep learning

Artificial Intelligence

Machine Learning

Deep Learning

- Deep neural network(DNN) is a subset of machine learning.
- Deep refers to the number of layers
- The system uses many layers of nodes to derive high-level functions from input data. 
- Transforming the data into a more abstract component

<!-- image -->

# Why deep learning

- As we construct larger neural networks and train them with more and more data, their performance continues to increase.
-  This is generally different to other machine learning techniques that reach a plateau in performance.

- ANN are used usually with 1 hidden layer
- 
- Not good at learning weights with many layers

<!-- image -->

- Many hidden layers are included
- In each layer intermediate features are important for difficult classification tasks 

<!-- image -->

ANN vs. Deep learning ? 

ANN

Deep learning 

# Types of DNN

- Feed forward deep neural network (FF-DNN)
- Fully-Connected NN–feed forward or multilayer perceptron (MLP)
- Convolutional neural network (CNN)
- feed forward, sparsely-connected, weight sharing
- Recurrent NN (RNN)
- feedback
- Long Short-Term Memory (LSTM):
- feedback + storage 

# How DNN works

- Neuron : DNN is consist of multiple neurons, The neurons take input data and simple operations are performed on those data. The result of these operations is passed to other neurons(storing and identifying information)

- Layer : DNN is composed of input and output layers, and one or more hidden layer 

- Weight :the connection between two neurons of successive layers would have an associated weight. 

- Input : matrix or vector of inputs.

- Output : Feature maps (matrix)

- Activation function Whether the result will be passed, is determined by the activation function The activation function plays an important role for both feature extraction and classification 

- Learning mechanism (optimizer) : will help the neural network incrementally update the weights (that were randomly initialized) to a more suitable weight that aids into correct prediction of the outcome 

# Feed forward deep neural network (FF-DNN)

- A deep neural network (DNN) can be considered as stacked neural networks, i.e., networks composed of several layers.
- Feed forward deep neural network(FF-DNN): is multilayer perceptrons (MLP) 
- DNNs where there is more than one hidden layer and the network moves in only forward direction (no loopback). 
- FFDNN are suitable in both classification and prediction.
- When the FF-DNN is used as a classifier, the input and output nodes will match the input features and output classes.
- The most important concepts in a FF-DNN are weights, biases, nonlinear activation and backpropagation. 

# How DNN works

<!-- image -->

<!-- image -->

# Back-propogation algorithm

Phase 1:propagation 

 Each propagation involves the following steps

1. Propagation forwards to the network to generate the output values
2. Calculation of the cost(error term)
3. Propagation of the output activations back through the network  using the training pattern target in order to generate the deltas (difference between the targeted and actual outputs) of all outputs and hidden neurons

Phase 2: weight update

Following steps must be followed for each weight

1. The weights output delta and input activations are multiplied to find the gradient of the weight
2. Ratio of the weight gradient is subtracted from weight

# Other aspects

- H2o
- Tensorflow
- Deepnet
- nnet
- neuralnet
- kerasR
- Keras (uses TensorFlow as a backend)
- 

Why is it generally better than other methods on image, speech and certain other types of data? 

Deep learning R

- Series of layers between input &amp; output involved in 
- Feature identification 
- Processing in a series of stages  
- Very similar with  our brains function

<!-- image -->

<!-- image -->
#      LM Big Data Management in Finance  Birmingham Business School  Fundamentals of Machine Learning  

Dr. Animesh Acharjee 

<!-- image -->

# Agenda 

- What is machine learning
- Types of machine learning 
- Fundamentals of machine learning
- Validation matrices  
- Why penalization methods required?
- What is penalization? 

- Machine learning, a branch of artificial intelligence, concerns the construction and study of systems that can learn from data (http://en.wikipedia.org/wiki/Machine\_learning)

-  Why we should use machine learning? 
- Machine learning methods are not based on statistical assumptions such as normality, independence etc. 

- All machine learning methods are non-parametric but reverse is not always true

- Some machine learning algorithms are inspired by biological phenomena. Ex: Genetic algorithm, ant colony optimization  
- 

What is machine learning 

- Classical models are presented with rules and data to get answers
- 
- Machine learning systems is trained rather explicitly programmed 

Classical vs. machine learning models 

<!-- image -->

<!-- image -->

Artificial intelligence, machine learning, and deep learning 

- Artificial Intelligence (AI)
- Involves machines that can perform tasks/job that are characteristic of human intelligence.
- Might involve some machine learning
- 
- Machine Learning (ML)
- Development of algorithms, which improve by presenting data

- Deep Learning
- Part of machine learning and AI
- Deep models
- Based on artificial neural networks.

<!-- image -->

Explainable/Interpretable AI (XAI) 

Why

- Interpretability 
- The best explanation of a simple model is the model itself
- It perfectly represents itself and is easy to understand. 

<!-- image -->

Many different types 

- LIME (Local interpretable model-agnostic explanations)
- DeepLIFT
- Layer-Wise Relevance Propagation
- Model-Specific Approximation
- Linear SHAP
- Low-Order SHAP
- Max SHAP
- Deep SHAP (DeepLIFT + Shapley values)
- 

<!-- image -->

<!-- image -->

Types of learning  

<!-- image -->

<!-- image -->

<!-- image -->

Unlabelled data

Labeled data

Make a sequence of decisions from complex environment 

Algorithm

- Machine learning tasks are typically classified into three broad categories
- 

Supervised learning

- The computer/algorithm is presented with example inputs and their desired outputs, given by a “teacher” (user), and the goal is to learn a general rule that maps inputs to outputs
- 

Unsupervised learning

- No labels are given to the learning algorithm, leaving it on its own to find structure in its input 
- Unsupervised learning can be a goal in itself (discovering hidden patterns in data) 

Reinforcement learning

- A computer program interacts with a dynamic environment in which it must perform a certain goal (such as driving a vehicle), without a teacher explicitly telling it whether it has come close to its goal or not

<!-- image -->

Machine learning vs. Statistics 

<!-- image -->

<!-- image -->

y=α+ α1x1+ α2x2+…+ αnxn

<!-- image -->

Copyright@Dr. Animesh Acharjee

Questions

Input Data/

Data Structure

Parameters / Weights

Training/Testing 

Algorithm/

Method 

Evaluation 

Work Flow of Machine Learning Methods

<!-- image -->

- 

Questions are usually in two categories

- Observation/individual  related
- How observations are clustered? For example: Credit card fraud or not
- Outliers 
- Missing values
- 
- Feature/Variable related
- How variables/features are clusters?
- Which variables are making differences among many classes?
- Which variables are correlated ?
- Is it possible to identify them in the data set?
- Are those variables being predictive? Can be used as a stratification in different location?
- Are those variables being stable?
- Are those variables statistically significant?  
- 
- 

- 
- 
- 

Questions

<!-- image -->

- Input data can have different structures 
- It is very important to understand what type of question is being asked and does data support that 

Input Data

<!-- image -->

<!-- image -->

- Supervised Learning: Classification and regression
- Decision trees Ensembles 
- Support vector machine (SVM)
- k-NN Linear regression 
- Naive Bayes 
- Neural networks
- Logistic regression Perceptron 
- Unsupervised Learning
- Hierarchical Clustering
- k-means Clustering 
- Reinforcement Learning 
- Markov Decision Process 
- 

Example: Algorithm

Parameters and hyperparameter

- Each of the machine learning algorithms associated with some extra parameters 

-  Called as hyper parameters 
- 
- For example
- 
- Number of decision trees need to use in the Random Forest Model 
- 
- In classical statistics view : How many components need to use in PLS-DA model ? 

<!-- image -->

Test set 

Prediction Function, f(α)

Class 1

Class 2

Class 3

Test set 

Out of sample error /

Generalized error

Evaluation

Hastie et al., (2009) 2nd Ed., The Elements of Statistical Learning : Data Mining, Inference, and Prediction. 

<!-- image -->

- How to do it?
- Split the data in different parts
- Keep aside test data
- Build a model on training data 
- Evaluate on test set
- Repeat
- 

Types of Cross Validation

- 5 fold 
- 10 fold 
- Leave one out 
- Resampling 
- Why it is used for? 
- Picking variables to include in the model 
- Picking the type of prediction function to use
- Picking the parameters in the prediction function 
- Comparing different predictors 
- Depends on how many total samples are available
- Some times double cross validation is recommended due to hyper parameters 
- 

Cross Validation

Prediction model design

<!-- image -->

<!-- image -->

Rule of thumb

Subjective!!!

Evaluation

# Evaluating Performance  

Widely used evaluation metrics for classifiers:

- Accuracy is the amount of correctly classified instances of the total instances; defined as the ratio of number of correct predictions to the total number of predictions.
- Confusion matrix
- Confusion matrix - is a table that records the number of instances in a dataset that fall in a particular category.
- Precision 
- Recall/sensitivity.

# Evaluating Performance

<!-- image -->

- True Positives (TP) and True Negatives (TN) are number of positive and negative instances predicted correctly.
- False Positives (FP) and False Negatives(FN) are misclassified instances.

<!-- image -->

<!-- image -->

# F-Measure

- F-Measure- is a metric of a test’s accuracy
- F measure reaches its best value at 1 (perfect precision and recall) and worst at 0.

<!-- image -->

<!-- image -->

Other matrices 

# Regression matrices

- RMSE is defined as the square root of the average squared distance between the actual score and the predicted score

<!-- image -->

- Median Absolute Percentage Error 

<!-- image -->

where yi is the true value for the ith data point, yi-hat is the predicted value, and n is the number of data points.

# Regression revisit

Regression: One example

Here:

y  = Response

x1 = Predictor 1

- y (Response) = 0 + 1* X1 + Error

Slope / Coefficient/ Weights

1

Multiple linear regression

Regression Equation : Surface 

y = 0 + 1* X1+ 2 * X2 + Error

- 

More general Equation: multidimensional surface

y = 0 + 1*X1+ 2*X2+ 3*X3… + p*Xp+ Error

y

<!-- image -->

x1

x2

Question:

Do you see any problem / Issue in this example?

Same example but with x2:

y  = Response

x1 = Predictor 1

x2 = Predictor 1

<!-- image -->

Or in closed form 

If nr. of variable= “p”, then  

# Multicollinearity

- X1 and X2might be correlated
- Exact or near linear relationships between the x variables
- Also called as : collinearity, near-collinearity or ill-conditioning

What are the consequences? 

Regression coefficients 

- Unstable (sensitive to small changes)
- Not uniquely defined
- Have high variance
- Coefficients can get the wrong sign
- Absolute values of regression coefficients can be absurdly high
- Impossible to interpret individually
- Relative importance of variables cannot be estimated reliably

# Bouncing betas

<!-- image -->

Consequences of Multicollinearity 

The Elements of Statistical Learning: Data Mining, Inference, and Prediction ; Trevor Hastie, Robert Tibshirani, Jerome Friedman

Always occurs when 

- More variables (p) than objects (n) (p&gt;n)
- Therefore
- Normal multiple linear regression not possible !

Traditional solutions

- Collect more data
- Takes lots of time, money 
- Sometime  impossible because of logistics (Project plan)
- Use a set of variables psubset &lt; n
- Filter on quality criteria: ok
- Still p &gt;&gt; n
- Do not want to remove more if not known whether important

# Multicollinearity

# Also possible solutions

- Use selected variables based on “some”  criteria 
- Filter first on univariate methods (t-test, correlation, ANOVA)
- Problem
- Assumption is variables are independent
- Multiple testing 
- 
- Dimension reduction (PCA, clustering)
- Machine learning methods
- Penalized methods

- Penalization / Regularaization/ Sparse/ Shrinkage  methods  Lasso, Ridge and Elastic Net 

Recollect: Multiple linear regression

Regression Equation : Surface 

y = 0 + 1* X1+ 2 * X2 + Error

- 

More general Equation: multidimensional surface

y = 0 + 1*X1+ 2*X2+ 3*X3… + p*Xp+ Error

y

<!-- image -->

x1

x2

Question:

Do you see any problem / Issue in this example?

Same example but with x2:

y  = Response

x1 = Predictor 1

x2 = Predictor 1

<!-- image -->

Or in closed form 

If nr. of variable= “p”, then  

Hastie et al.(2009), The Elements of Statistical Learning: Data Mining, Inference, and Prediction

Bias, Variance and Model Complexity

<!-- image -->

<!-- image -->

Model Complexity = Bias + Variance 

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

A line that captures a general direction but does not capture many of the points. 

 A line that captures the general direction of the points but might not capture every point in the graph

A line that captures every single point in the graph

# Why is regularization important? 

- Regularization favours simpler models to more complex models to prevent your model from overfitting to the data. 
- How so? 
- They address the following concerns within a model:
- Variance-bias trade-off 
- Multicollinearity
- Sparse data handling(i.e. the situation where there are more observations than features)
- Feature selection
- An easier interpretation of the output.
- 

Penalization Methods

Variable Selection Methods

- LASSO (Tibshirani R, 1996)
- Elastic Net (Zou H, 2005)

Ranking Methods

- Ridge (Hoerl and Kennard, 1970)

LASSO (Tibshirani R, 1996)

- 
- Fused LASSO (Tibshirani and Saunders, 2005)
- Grouped LASSO (Yuan M, 2006)
- Adaptive LASSO (Zou H, 2006)
- Graphical LASSO (Friedman et al., 2007)

Type of methods

<!-- image -->

# Regularization: An Overview

36

# Introduction to LASSO

- Recollect least squares for OLS
- The OLS equation is also called as objective function/cost function
-  The residual sum of squares(RSS) plus the sum of absolute value is minimized

- LASSO stands for Least Absolute Shrinkage and Selection Operator
- LASSO regression performs L1 regularization, i.e. it adds a factor of sum of absolute value of coefficients in the optimization objective. 

<!-- image -->

<!-- image -->

<!-- image -->

# Properties of LASSO

LASSO (Least Absolute Shrinkage and Selection Operator)

- Variable will be selected, depending on λ
- λ is called as penalty parameter/ Shrinkage parameter
- The value of λ lies between 0 to 1 
- λ  close to 1 means
- Heavy penalization 
- Less variables will be selected
- Many variables shrunk to “0” (kicked out from model)
- Automatic variable/feature selection  !
- No grouping of correlated variables
- Maximum of “n” variables selected
- 

Bottle neck : Selection of “λ”

Should be estimated from data (Unbiased way)

<!-- image -->

# Ridge Regression

- Alternatively, we can choose a regularization term that penalizes the squares of the parameter magnitudes. Then, our regularized loss function is:
- 
- 
- 
- Note that               is the square of the l2  norm of the vector b
- 
- 

39

# Choosing l

- In both ridge and LASSO regression, we see that the larger our choice of the regularization parameter l, the more heavily we penalize large values in b,
- If l is close to zero, we recover the MSE, i.e. ridge and LASSO regression is just ordinary regression.
- If l is sufficiently large, the MSE term in the regularized loss function will be insignificant and the regularization term will force bridge and bLASSO to be close to zero.
- To avoid ad-hoc choices, we should select l using cross-validation.

40

Selection of “λ”

<!-- image -->

“λ” (lambda)

MSE

(Mean Square Error)

- Very critical 
- Can be optimised
- Linear optimization 
- Nonlinear optimization
- 
- The solution of the Ridge/Lasso regression involves three steps:
- Select λ 
- Find the minimum of the ridge/Lasso regression loss function and record the  MSE  on the validation set. 
- Find the λ that gives the smallest MSE
-  

<!-- image -->

Prediction Function, f(α)

Test set 

Out of sample error/

Generalized error/MSE

Evaluation

- Elastic Net produces a regression model that is penalized with both the L1-norm and L2-norm. 
- The consequence of this is to effectively shrink coefficients (like in ridge regression) and to set some coefficients to zero (as in LASSO).

Elastic Net Regression 

<!-- image -->

LASSO

Ridge 

# Elastic Net Regression 

<!-- image -->

# Elastic Net Regression 

- The elastic net method performs variable selection and regularization simultaneously.
- Groupings and variables selection are the key roles of the elastic net technique.
- The elastic net technique is most appropriate where the dimensional data is greater than the number of samples used.

- 
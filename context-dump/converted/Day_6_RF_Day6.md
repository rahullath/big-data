#      LM Big Data Management in Finance (36320) Birmingham Business School  

Dr. Animesh Acharjee 

<!-- image -->

# Methods 

# Decision Tree &amp; Random Forest 

# What is a decision tree?

- A decision tree consists of three different building blocks:
- Nodes 
- The nodes identify the splitting feature and implement the partitioning operation on the input subset of data
- Branches 
- the branches depart from a node and identify the different subsets of data produced by the partitioning operation
- Leaves. 
- The leaves, at the end of a path, identify a final subset of data and associate a class with that specific decision path

# Example binary classification tree

-  The root contains all samples
-  Each subsequent node contains a subset of the samples
-  Each decision rule splits up the samples into two  subgroups
-  Every rule is of the form
-  x &gt; t  for continuous x
-  x  A for categorical x
- 
-  Only one variable per rule
-  Same variable can be used again
-  Each leaf more or less ‘pure’
-  A new sample is run through the tree and one looks for the leaf it ends up
- Regression Trees: average of the values at that leaf
- 

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

Colour Grey ?

No

Yes

<!-- image -->

<!-- image -->

Mass &gt; 2000 kg ?

Neck &gt; 1.5 m ?

Yes

No

No

Yes

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

Example-1: Identify / separate species  

Mass &gt; 2000 kg ?

- Search, per step, ‘best’ variable and split point
- Each step: splitting only one of the nodes into two
- There are different ways to control how many splits are generated
- Gini Index
- The Gini index is based on Gini impurity. Gini impurity is defined as 1 minus the sum of the squares of the class probabilities in a dataset.
- Entropy 
- Entropy is a concept that is used to measure information 
- Information Gain
- How good a feature is for splitting, the difference in entropy before and after the split is calculated.

Criteria for splitting

Stopping criteria

- All nodes are pure (single class) or have a ‘final’ number of elements, e.g. 5
- Prune the tree back somewhat
- Remove splits with low decrease in impurity
- To protect against overfitting
- Unpruned trees
- Low bias (end nodes have maximum purity)
- High variance
- Widely different rules if the data or the samples change a little

Example 2: Spielberg movies

yes

yes

yes

Random Forest 

# Random forests (Breiman 2001)

- Both classification and multiple regression
- Handles high numbers of variables (p &gt;&gt; n)
- Handles categorical and continuous predictors
- Two-class and multi-class
- Robust to large numbers of noise variables
- Incorporates interactions between variables
- Internal cross validation
- Variable importance  is estimated
- Proximities between cases are computed
- can be used to do clustering (unsupervised)
- Extension of ‘Classification and regression trees’ (CART)
- 

<!-- image -->

# Random forest

- Ensemble method
- not one tree, but many
- Each single tree unpruned
- Low bias, high variance
- Introduce two forms of ‘randomness’ 
- Random training sets
- Random variable selection at each node
- Effects
- Individual trees are weak learners
- Low bias, low correlation, high variance
- Averaging over the trees retains low bias and reduces variance !
- ‘Bagging’ = bootstrap aggregation
- 

# Bootstrap

# Internal cross validation using ‘out of bag’ samples

# New sample: each tree casts vote, then majority voting

# Variable importance

- Idea: change values of a variable and check whether the OOB error changes dramatically
- 
- For each variable x do the following:
- For each tree of a forest permute the values of x for the ‘out of bag’ samples
- Redo the classification for the OOB samples
- Compare the OOB error with original OOB error
- If unchanged, or just a bit: variable was not so important
- If error increases a lot: variable was  important
- Also: quantify the increase in impurity 

# Random Forest using caret 

fit.rf &lt;- train(medv~., data=training, method="rf", metric="RMSE", preProc=c("center", "scale"), trControl=control)

<!-- image -->
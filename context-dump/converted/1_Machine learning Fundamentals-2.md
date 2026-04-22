#      LM Big Data Management in Finance (36320) Birmingham Business School  Fundamentals of Machine Learning

Dr. Animesh Acharjee 

<!-- image -->

- What is machine learning?
- Why machine learning is important in the financial technology?
- What is the difference between supervised vs unsupervised learning?
- What are the two basic ingredients for machine learning methods to learn the rules?
- What are the training and testing samples? 
- 

# Review Questions 

# Regression 

# Regression: Basics 

Why we use regression?

- Modeling  relationship between variables
- Predict outcome of one variable as a function of others
- Investigate the relative importance of the predictors
- Assumptions : Linearity, Homoscedasticity, Independence, Normality

Types of regression 

- Linear 
- Simple linear 
- Multiple linear 
- Nonlinear/Curvilinear

- y=Dependent / response / outcome 
- X=Independent / regressor / predictor
-    =Random variable representing the result of both errors in model specification and measurement. 
- 
- In the figure 
- Number of observations (n)=10
- Number of response variables (y) =1
- Number of predictor variables (X) =1
- 

- How one variable changes with another
- How “X” and “y” are behaving

Regression: Basics 

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

# Practical 

<!-- image -->

<!-- image -->

The caret package (short for Classification And REgression Training

# How to pre-process using caret? 

- Pre-processing is a important step in the data analysis 
- We need to standardize to make every variable in the same scale
- Data becomes more like gaussian distribution
- We can do it using following function

fit.lm2 &lt;- train(medv~., data=training, method="lm", metric="RMSE", preProc=c("center", "scale"), trControl=control) 

- #Install the Caret Package and its depencencis if it is not already installed

if (!require("caret")) install.packages("caret", dependencies=T)

- 

#Load the Package

library("caret")

install.packages("mlr")

#load packages

library(caret)

library(mlbench)

# load dataset

data(BostonHousing)

# cheking the dimensions 

dim(BostonHousing)

head(BostonHousing) 

# create 80% and /20% for training and validation datasets

set.seed(9)

# create a partition on the data  

validation\_index &lt;- createDataPartition(BostonHousing$medv, p=0.80, list=FALSE)

training &lt;- BostonHousing[validation\_index,]

dim(training)

# dimension of the validation data  

validation &lt;- BostonHousing[-validation\_index,]

# dimension of the validation data  

dim(validation)

- 

<!-- image -->

<!-- image -->

# train a model and summarize model

control &lt;- trainControl(method="cv", number=10)

# Create model on training set 

fit.lm &lt;- train(medv~., data=training, method="lm", metric="RMSE", trControl=control)

print(fit.lm)

print(fit.lm$finalModel)

# predict on test set  

predictions &lt;- predict(fit.lm, newdata=validation)

write.csv(predictions, "predictionsModel.csv ") 

- 

# Methods 

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

24

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

- Alternatively, we can choose a regularization term that penalizes the squares of the parameter magnitudes. 
- 
- Then, our regularized loss function is:
- 
- 
- 
- Note that                           is the square of the l2  norm of the vector b
- 
- 

# Choosing l 

- In both ridge and LASSO regression, we see that the larger our choice of the regularization parameter l, the more heavily we penalize large values in b,
- If l is close to zero, we recover the MSE, i.e. ridge and LASSO regression is just ordinary regression.
- If l is sufficiently large, the MSE term in the regularized loss function will be insignificant and the regularization term will force bridge and bLASSO to be close to zero.
- To avoid ad-hoc choices, we should select l using cross-validation.

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

Unsupervised Learning 

- Clustering
- Hierarchical Clustering

# Clustering

- Clustering = Class discovery
- Group attributes/features/variables that behave similarly over a set of samples
- ‘Guilt by association’
- Group observations based on similar features
- Clustering = unsupervised classification
- Information about grouping is unknown or unused

Variables

Observations

Clustering on variables

Variables

Observations

Clustering on observations/samples

Variables

Observations

Clustering on observations/samples  &amp; variables simultaneously=Bi-clustering

Aim of clustering

<!-- image -->

- A set of objects that are close/similar to each other in some  defined aspect(s) and separated from other groups of objects.

- Example: green/ red data points were generated from two different normal distributions

Definition of ‘close’ is not always that obvious

<!-- image -->

<!-- image -->

<!-- image -->

Distance measure and algorithm

- Distance measure: Quantification of  (dis)similarity of objects.
- What do we regard as ‘similar’ ?
- How best quantified ?
- Cluster algorithm: A procedure to group objects. 
- Aim: small within-cluster distances, large between-cluster distances.
- Procedure to form such groups

Given vectors x = (x1, …, xp), y = (y1, …, yp)

- Euclidean distance 
- 
- Manhattan distance
- 
- Pearson correlation distance

Distance/Similarity

- Squared correlation distance
- 
- 
- Angular separation / cosine correlation distance

Distance/Similarity

# Which distance measure to use?

- Euclidean and Manhattan distance both measure absolute differences between vectors. 
- Manhattan distance is more robust against outliers.
- When the variables are measured on different scales it is wise to apply standardization to the observations
- Standardization makes Euclidean and correlation distances equivalent 

- Hierarchical
- Agglomerative (UPGMA, single linkage, furthest linkage)
- Divisive
- Partitioning
- K-means
- Self organizing maps

Clustering algorithms

Hierarchical Clustering

- Produces a dendrogram (tree)
- Avoids pre specification of the number of clusters K  
- The tree can be built in two distinct ways: 
- Bottom-up: agglomerative clustering
- Top-down: divisive clustering

<!-- image -->

Agglomerative Hierarchical Clustering

- Start with n sample (or p variables) clusters
- Each sample is a cluster
- At each step, merge two closest clusters
- Need a distance/similarity metric
- E.g. Correlation, cosine, Manhattan distance, Euclidean distance
- And a definition of the between-cluster distance
- As soon as clusters consist of more than one element you have to decide what the distance between the clusters is.
- Examples of between-cluster distances: 
- Unweighted Pair Group Method using Arithmetic averages (UPGMA):  average of pair wise distances
- Single-link (Nearest Neighbour): minimum of pair wise distances
- Complete-link (Furthest Neighbour): maximum of pair wise distances

How does it work?

distance

15 clusters

Find pair that is ‘closest’ according to distance measure

distance

14 clusters

Continue with the next closest pair(s)

distance

12 clusters

Next: one that is closest to an earlier pair

distance

12 clusters

Now: one cluster of three elements

distance

11 clusters

Go on a number of times

distance

8 clusters

Very close to two other clusters 

distance

8 clusters

distance

7 clusters

# Next step

All elements are in groups, but unconnected

distance

6 clusters

Red group

distance

5 clusters

Three groups (but: group identity unknown!)

distance

3 clusters

Two groups left

distance

2 clusters

All elements in one big group

distance

1 cluster

Distances between clusters

-    Calculation of the distance between two clusters is based on the pairwise distances between members of the clusters.
- 
- Complete linkage: largest distance 
- Average linkage:   average distance 
- Single linkage:       smallest distance
- 
- Complete linkage gives preference to compact/spherical clusters. 
- Single linkage can produce long stretched clusters.
- 

Hierarchical clustering

Single linkage

Complete linkage

Average linkage

<!-- image -->

# Partitioning methods

- K-means clustering
- Self-organizing maps (SOM)
- Bayesian Hierarchical Clustering (BHC)
- Partitioning around medoids (PAM)
- Model-based clustering

# Practical 

# Clustering  

The Dataset

- mtcars(motor trend car road test) comprise fuel consumption, performance, and 10 aspects of automobile design for 32 automobiles. 
- It comes pre-installed with dplyr package in R. 
- 

# Installing the package

install.packages("dplyr")

   

# Loading package

library(dplyr)

   

# Summary of dataset in package

head(mtcars)

# Finding distance matrix

distance\_mat &lt;- dist(mtcars, method = 'euclidean')

 

# Fitting Hierarchical clustering Model

set.seed(240)  # Setting seed

Hierar\_cl &lt;- hclust(distance\_mat, method = "average")

Hierar\_cl

 

# Plotting dendrogram

plot(Hierar\_cl)

 

# Choosing no. of clusters

# Cutting tree by height

abline(h = 110, col = "green")

 

# Cutting tree by no. of clusters

fit &lt;- cutree(Hierar\_cl, k = 3 )

fit

 

table(fit)

rect.hclust(Hierar\_cl, k = 3, border = "green")

<!-- image -->

<!-- image -->

# How to decide number of clusters? Missing data imputation 

- Animesh Acharjee

# Methods to decide number of the clusters 

- The Elbow Method
- The Gap Statistic
- The Silhouette Method
- The Sum of Squares Method
- 

# The "Elbow" method

- The "Elbow" method is a technique used to determine the optimal number of clusters in a dataset for a k-means clustering algorithm.
- It involves running the k-means clustering algorithm on the dataset for a range of values of k (number of clusters) and plotting the within-cluster sum of squares (WCSS) against the number of clusters. 
- 

<!-- image -->

Steps 

1. 
2. Choose a range of values for k (number of clusters). 
3. For each value of k, run the k-means clustering algorithm on the dataset and calculate the WCSS.
4. Plot the WCSS values against the corresponding values of k.
5. Look for the point on the plot where the rate of decrease in WCSS sharply changes or levels off, forming an "elbow" shape.
6. The value of k at the elbow is considered a good estimate for the optimal number of clusters.

# The Gap Statistic 

- 
- The gap statistic assesses the total within-cluster variation for various values of k by comparing them to their expected values within a null reference distribution of the data.
- The optimal number of clusters is estimated as the value that maximizes the gap statistic, indicating a significant departure from the random, uniform distribution of points. 
- In other words, it identifies the clustering structure that deviates most from random chance.

<!-- image -->

# The Silhouette Method

- The Silhouette Method is a way of evaluating the effectiveness of clustering in a dataset. 

- The Silhouette Score for each data point is then computed using the similarity and dissimilarity measures.
-  The score ranges from -1 to 1.
- 
- A high Silhouette Score (close to 1) 
- indicates that the data point is well-matched to its own cluster and clearly separated from other clusters.
- 
- A low Silhouette Score (close to -1) 
- suggests that the data point may be assigned to the wrong cluster, as it is more similar to points in a neighbouring cluster.

<!-- image -->

# The Sum of Squares Method

Sum of Squares Within Clusters (SSW):

- 
- For a given number of clusters (k), the Sum of Squares Within Clusters (SSW) is calculated. 
- SSW measures the total squared distance of each data point within its assigned cluster from the cluster's centroid (center point).

# R packages 

- Excellent packages for clustering 
- NbClust 
- Clustree
- cValid	

https://www.rdocumentation.org/packages/NbClust/versions/3.0.1/topics/NbClust
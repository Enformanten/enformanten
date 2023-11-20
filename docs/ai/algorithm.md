## Mathematical Formulation and Explication of Room Occupancy Detection Using Unsupervised Anomaly Detection with Isolation Forest

### Problem Definition

#### Overview

As described in the "Overview" section, the objective is to provide a measurement of whether a given room had been in use at a given time. This information is intended for downstream analytics. The setting includes \( n \) municipalities, each with \( m \) schools and \( k \) rooms. Each room has a time series of multivariate sensor data collected at 15-minute intervals.

#### Notations

- \( N \) : Set of municipalities, with size \( |N| = n \)
- \( M_i \) : Set of schools in municipality \( i \), with size \( |M_i| = m_i \)
- \( K_j \) : Set of rooms in school \( j \), with size \( |K_j| = k_j \)
- \( T \) : Set of discrete time intervals, sampled every 15 minutes, \( T = \{ t_1, t_2, \ldots, t_T \} \)
- \( x_{r,t} \) : Multivariate sensor data for room \( r \) at time \( t \)

#### Objective

The objective is to find a function \( f \) that takes as input the sensor data \( x_{r,t} \) for a room \( r \) at time \( t \) and outputs a label \( y_{r,t} \) indicating whether the room has been in use.

\[
f: x_{r,t} \mapsto y_{r,t}
\]

Here, \( y_{r,t} \) is a binary label:

- \( y_{r,t} = 1 \) if the room \( r \) is in use at time \( t \)
- \( y_{r,t} = 0 \) if the room \( r \) is not in use at time \( t \)

---

### Extended Mathematical Formulation: Anomaly Detection with Isolation Forest in Unlabeled Settings

#### Motivation for Anomaly Detection in Unlabeled Settings

Traditional supervised learning methods require labeled data, which we do not have in our case. This makes anomaly detection, particularly using Isolation Forest, an appealing choice because it can function well in unsupervised settings.

#### Why Isolation Forest?

Isolation Forest is highly suited for this task because it doesn't require labeled data for training. Instead, it focuses on isolating anomalies, providing an efficient and robust mechanism to classify rooms based on their usage.

#### Algorithmic Details

##### Feature Engineering: Kinematic Quantities

As before, we use function \( g: x_{r,t} \mapsto z_{r,t} \) to transform raw sensor data into derived kinematic quantities \( z_{r,t} \).

##### Isolation Forest Algorithm 

The Isolation Forest algorithm builds an ensemble of Isolation Trees, denoted as \( \mathcal{T} \), for the data sample. Each tree is constructed recursively as follows:

1. Randomly select a feature \( d \) from the data.
2. Randomly select a split value \( v \) between the minimum and maximum values of feature \( d \).
3. Partition the data into two subsets: \( D_{left} = \{z_{r,t} \in D | z_{r,t}[d] < v\} \) and \( D_{right} = \{z_{r,t} \in D | z_{r,t}[d] \geq v\} \).
4. Repeat the process for each subset until the tree reaches a certain height \( h_{max} \), or the subset contains fewer than a certain number of points.

The anomaly score for each data point \( z_{r,t} \), denoted by \( s(z_{r,t}) \), is computed as the average path length from the root to the terminal node across all trees in the forest:

\[
s(z_{r,t}) = \frac{1}{| \mathcal{T} |} \sum_{t \in \mathcal{T}} h_t(z_{r,t})
\]

Here, \( h_t(z_{r,t}) \) is the path length of data point \( z_{r,t} \) in tree \( t \).

Anomalies are the points that have shorter path lengths, meaning they are easier to isolate. Therefore, a smaller score indicates that the data point is more likely an anomaly.

##### Function \( f \)

Given the Isolation Forest's anomaly score function \( s(z_{r,t}) \), we can set a threshold \( \theta \) to determine the binary label \( y_{r,t} \) as follows:

\[
f(x_{r,t}) = 
\begin{cases}
1 & \text{if } s(g(x_{r,t})) < \theta \\
0 & \text{otherwise}
\end{cases}
\]

In this case, if the anomaly score is less than the threshold \( \theta \), the room is considered to be in use (\( y_{r,t} = 1 \)). Otherwise, it is considered not in use (\( y_{r,t} = 0 \)).

---

### Individualized Room Models: Tailoring Isolation Forest for Each Room

#### Rationale for Individual Models

Due to the significant variation in room characteristics such as size, number of windows, and presence of air conditioning, using a single Isolation Forest model for all rooms is insufficient. These factors affect the sensor readings, and thereby the derived kinematic quantities, in a way that can be highly room-specific. Therefore, it becomes crucial

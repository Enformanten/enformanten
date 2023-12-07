### Algorithm: Room Occupancy Detection

Simply stated, the objective is to provide a measurement of whether a given room had been in use at a given time. This information is intended for downstream analytics. The setting includes n municipalities, each with m schools and k rooms. Each room has a time series of multivariate sensor data collected at 15-minute intervals.

### Notations
* N: Set of municipalities, with size |N| = n
* M<sub>i</sub>: Set of schools in municipality i, with size |M<sub>i</sub>| = m<sub>i</sub>
* K<sub>j</sub>: Set of rooms in school j, with size |K<sub>j</sub>| = k<sub>j</sub>
* T: Set of discrete time intervals, sampled every 15 minutes, T = {t<sub>1</sub>, t<sub>2</sub>, ..., t<sub>T</sub>}
* x<sub>r,t</sub>: Multivariate sensor data for room r at time t

### Objective
The objective is to find a function f that takes as input the sensor data x<sub>r,t</sub> for a room r at time t and outputs a label y<sub>r,t</sub> indicating whether the room has been in use.

f: x<sub>r,t</sub> ↦ y<sub>r,t</sub>

Here, y<sub>r,t</sub> is a binary label:

* y<sub>r,t</sub> = 1 if the room r is in use at time t

* y<sub>r,t</sub> = 0 if the room r is not in use at time t


### Motivation for Anomaly Detection
Traditional supervised learning methods require labeled data, which we do not have in our case. This makes anomaly detection, particularly using Isolation Forest, an appealing choice because it can function well in unsupervised settings.

Isolation Forest is highly suited for this task because it doesn't require labeled data for training. Instead, it focuses on isolating anomalies, providing an efficient and robust mechanism to classify rooms based on their usage.

### Isolation Forest Algorithm
The Isolation Forest algorithm builds an ensemble of Isolation Trees, denoted as ℑ, for the data sample. Each tree is constructed recursively as follows:

* Randomly select a feature d from the data.
* Randomly select a split value v between the minimum and maximum values of feature d.
* Partition the data into two subsets:  
    * D<sub>left</sub> = {z<sub>r,t</sub> ∈ D | z<sub>r,t</sub>[d] < v} and 
    * D<sub>right</sub> = {z<sub>r,t</sub> ∈ D | z<sub>r,t</sub>[d] ≥ v}.
* Repeat the process for each subset until the tree reaches a certain height h<sub>max</sub>, or the subset contains fewer than a certain number of points.

The anomaly score for each data point z<sub>r,t</sub>, denoted by s(z<sub>r,t</sub>), is computed as the average path length from the root to the terminal node across all trees in the forest:

s(z<sub>r,t</sub>) = (1 / |ℑ|) ∑<sub>t ∈ ℑ</sub> h<sub>t</sub>(z<sub>r,t</sub>)

Here, h<sub>t</sub>(z<sub>r,t</sub>) is the path length of data point z<sub>r,t</sub> in tree t.

Anomalies are the points that have shorter path lengths, meaning they are easier to isolate. Therefore, a smaller score indicates that the data point is more likely an anomaly.

#### Scoring Function f

Given the Isolation Forest's anomaly score function `s(z_r,t)`, we can set a threshold `θ` to determine the binary label `y_r,t` as follows:

`f(x_r,t) = 1 if s(g(x_r,t)) < θ, else 0`

In this case, if the anomaly score is less than the threshold `θ`, the room is considered to be in use (`y_r,t = 1`). Otherwise, it is considered not in use (`y_r,t = 0`).

### Individualized Room Models
Due to the significant variation in room characteristics such as size, number of windows, and presence of air conditioning, using a single Isolation Forest model for all rooms is insufficient. These factors affect the sensor readings, and thereby the derived kinematic quantities, in a way that can be highly room-specific. Therefore, it becomes crucial to train a separate model for each room.
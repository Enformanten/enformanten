# Algorithm
The following sections provide a detailed description of the AI model, the algorithm behind the room utilization model (Tilly, denoted as `the solution` in the following) and its implementation. 

## Domain
## Problem Definition

### Overview

As described in the "Overview" section, the objective is to provide a measurement of whether a given room had been in use at a given time. This information is intended for downstream analytics. The setting includes \( n \) municipalities, each with \( m \) schools and \( k \) rooms. Each room has a time series of multivariate sensor data collected at 15-minute intervals.

### Notations

- \( \mathcal{N} \): Set of municipalities, \( |\mathcal{N}| = n \)
- \( \mathcal{M}_i \): Set of schools in municipality \( i \), \( |\mathcal{M}_i| = m_i \)
- \( \mathcal{K}_j \): Set of rooms in school \( j \), \( |\mathcal{K}_j| = k_j \)
- \( \mathcal{T} \): Set of discrete time intervals, sampled every 15 minutes, \( \mathcal{T} = \{t_1, t_2, \ldots, t_T\} \)
- \( \mathbf{x}_{r,t} \): Multivariate sensor data for room \( r \) at time \( t \)

### Objective

The objective is to find a function \( f \) that takes as input the sensor data \( \mathbf{x}_{r,t} \) for a room \( r \) at time \( t \) and outputs a label \( y_{r,t} \) indicating whether the room has been in use.

\[
f: \mathbf{x}_{r,t} \mapsto y_{r,t}
\]

Here, \( y_{r,t} \) is a binary label:

- \( y_{r,t} = 1 \) if the room \( r \) is in use at time \( t \)
- \( y_{r,t} = 0 \) if the room \( r \) is not in use at time \( t \)

The challenge is to train and validate this function \( f \) given the noisy sensor data, varying data quality, and significant differences in room characteristics.




Therefore, the solution is trained on a per-room basis, meaning that a separate model is trained for each room.




This is done by training a supervised machine learning model on historical data from Enformanten's database, which contains sensor data from schools across municipalities. The model is trained on a per-room basis, meaning that a separate model is trained for each room. This is due to the fact that the utilization rate is highly dependent on the room's characteristics, such as size, number of windows, and number of students.


## Model
The room utilization model is a supervised machine learning model that predicts the utilization rate of a given room at a given time. The model is trained on historical data from Enformanten's database, which contains sensor data from schools across municipalities. The model is trained on a per-room basis, meaning that a separate model is trained for each room. This is due to the fact that the utilization rate is highly dependent on the room's characteristics, such as size, number of windows, and number of students.
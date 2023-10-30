## Problem Definition

### Overview

As described in the "Overview" section, the objective is to provide a measurement of whether a given room had been in use at a given time. This information is intended for downstream analytics. The setting includes $ n $ municipalities, each with $ m $ schools and $ k $ rooms. Each room has a time series of multivariate sensor data collected at 15-minute intervals.

### Notations

- $ N $ : Set of municipalities, with size $ |N| = n $
- $ M_i $ : Set of schools in municipality $ i $, with size $ |M_i| = m_i $
- $ K_j $ : Set of rooms in school $ j $, with size $ |K_j| = k_j $
- $ T $ : Set of discrete time intervals, sampled every 15 minutes, $ T = \{ t_1, t_2, \ldots, t_T \} $
- $ x_{r,t} $ : Multivariate sensor data for room $ r $ at time $ t $

### Objective

The objective is to find a function $ f $ that takes as input the sensor data $ x_{r,t} $ for a room $ r $ at time $ t $ and outputs a label $ y_{r,t} $ indicating whether the room has been in use.

$$
f: x_{r,t} \mapsto y_{r,t}
$$

Here, $ y_{r,t} $ is a binary label:

- $ y_{r,t} = 1 $ if the room $ r $ is in use at time $ t $
- $ y_{r,t} = 0 $ if the room $ r $ is not in use at time $ t $

The challenge is to train and validate this function $ f $ given the noisy sensor data, varying data quality, and significant differences in room characteristics.

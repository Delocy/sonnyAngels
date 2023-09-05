# Problem Statement - 1: Optimize Advertisement Moderation
To tackle this problem we first cleaned the data provided.

## Data Cleaning Process
In the data cleaning process, we performed the following steps to prepare our dataset for analysis:

### Cleaning the delivery_country Column
The delivery_country column was processed to make it more consistent and informative. We replaced special characters with commas, removed leading and trailing whitespace, and split the values into lists. Additionally, we applied custom logic to handle specific cases like 'USCA' and 'MENA', splitting them into their respective countries.

###  Cleaning the ad_revenue Column
We handled missing values in the ad_revenue column by filling them with zeros, ensuring that we maintain data consistency for analysis.

###  Preparation for the Moderator Dataset
Removing Moderators with Null Productivity and Utilization
To maintain data quality, we removed moderators with null values in both the 'Productivity' and 'Utilisation %' columns from the Moderator dataset.

###  Removing Moderators with Null Accuracy
To ensure data consistency, moderators with null values in the 'accuracy' column were removed from the dataset.

These data cleaning steps were essential to prepare our dataset for subsequent analysis and modeling tasks.

## Data Processing and Scoring of the Ads

### Decision Weights
We assigned decision weights to different factors to reflect their relative importance in our scoring process. These weights help us adjust the contribution of each factor to the final score:

Latest Weight: Assigned a weight of 20.
Start Weight: Assigned a weight of 20.
Ad Revenue Weight: Assigned a weight of 35.
ST Weight: Assigned a weight of 25.
Ad Revenue Score
We calculated the Ad Revenue Score by measuring the difference between the 'ad_revenue' and the average ad revenue ('avg_ad_revenue'). The score was then scaled between the maximum and minimum differences, with the weight assigned to the Ad Revenue factor.

### Baseline ST Score
The Baseline ST Score was calculated by scaling the 'baseline_st' values between the maximum and minimum values, with the weight assigned to the ST factor.

### Latest Punish Score
To determine the Latest Punish Score, we considered the time difference between the 'p_date' and the 'latest_punish_begin_date.' The score was scaled between the maximum and minimum time differences and further adjusted based on the number of punishments ('punish_num').

### Start Time Score
The Start Time Score was calculated by measuring the time difference between the 'p_date' and the 'start_time.' Similar to other scores, it was scaled between the maximum and minimum time differences, with the weight assigned to the Start Time factor.

### Total Score
The Total Score for each entry was computed by summing the scores for Ad Revenue, Baseline ST, Latest Punish, and Start Time. This provides an overall assessment of each entry's performance.

### Normalization
To ensure that our scores are on a consistent scale, we applied Min-Max scaling to the "total_score" column, transforming it to a range between 0 and 1. This normalization allows for fair comparisons between different entries.

## Data Processing and Scoring of the Moderators

### Calculating Real Productivity
We computed the "Real Productivity" for each moderator by subtracting the "Utilisation %" from the "Productivity" value. This metric represents the actual productivity after accounting for utilization.

### Renaming Columns
We renamed the " accuracy " column to "accuracy" to remove leading and trailing whitespaces.

### Removing Incomplete or Invalid Data
We removed rows where the "accuracy" value was either "-" or ' - '. Additionally, any rows with missing values in the "accuracy" column were dropped to ensure data quality.

### Scoring Moderators
We assigned weights to different factors to determine the moderators' overall score:

Weight_Real_Productivity: Assigned a weight of 0.4.
Weight_Accuracy: Assigned a weight of 0.45.
Weight_Handling_Time: Assigned a weight of 0.15.

### Normalization
To ensure that scores are on a consistent scale, we applied Min-Max scaling to the "score" column. This transformation scales the scores between 0 and 1, allowing for fair comparisons between moderators.

### Exporting Results
Finally, we exported the dataset with the calculated scores to an Excel file named "mods_score.xlsx."

These scoring and processing steps enable us to rank and analyze the data effectively based on the defined criteria and weights.

## Optimising matching
Finally, for our GA_Algo.py code, the objective was to optimize the allocation of advertisements to moderators in a way that maximizes the overall satisfaction or alignment between each ad and the chosen moderator. To achieve this, the code employed a simulated annealing algorithm, a probabilistic optimization technique. The goal was to find an allocation that minimizes the proximity between the performance scores of ads and moderators, considering factors like real productivity and accuracy. 

At the heart of the simulated annealing loop, the code calculates a crucial value known as "proximity_change" when it compares the current solution to a potential neighboring solution. This "proximity_change" quantifies the difference in performance between the current and neighboring solutions. The probability of accepting this neighboring solution follows the **Metropolis criterion**, expressed mathematically as:

**P(accept) = exp(-proximity_change / current_temperature)**

Here, exp represents the exponential function, and current_temperature controls the likelihood of accepting a solution that is worse than the current one. Lower temperatures reduce the probability of accepting worse solutions, guiding the search toward more optimal allocations.

In this equation, "exp" denotes the exponential function, and the "current_temperature" parameter plays a vital role. It governs the likelihood of accepting a solution that might be worse than the current one. As the temperature decreases during the simulated annealing process, this mathematical formula becomes less inclined to accept worse solutions. This gradual reduction in temperature serves as a crucial mechanism for guiding the search towards more optimal allocations by controlling the randomness and exploration-exploitation balance in the optimization process. In essence, it dynamically reassigns advertisements from one moderator to another, systematically exploring potential improvements in the allocation configuration while ensuring the algorithm converges towards better solutions.

Ultimately, the code aimed to discover the most suitable allocation of ads to moderators, optimizing the performance of the overall system based on defined criteria and weights. Thus, potentially leading to a 10+% increase in utilization of the ads moderator and an increase in revenue as compared to prior to model implementation.

![IMAGE 2023-09-06 01:54:43](https://github.com/Delocy/sonnyAngels/assets/94375191/06cfe19e-8efb-4317-bc55-c5e6089d5093)


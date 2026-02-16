# Bootcamp-Projects

## Overview
This repository contains my projects developed during the bootcamp program.  
For each project, I document the end-to-end workflow including data preprocessing, feature engineering, modeling/evaluation, and key insights.


## Projects

### 1) Amazon Review Rating & Review Sorting
- Goal: Compute the product rating using time-based weighting and rank reviews in the most reliable way.
- Steps:
  - Compare Average Rating vs. Time-Weighted Rating
  - Create `helpful_no`
  - Compute `score_pos_neg_diff`, `score_average_rating`, and `wilson_lower_bound`
  - Select Top 20 reviews based on WLB
- Files:
  - `amazon_review_project.py`
  - `amazon_yorumlari.csv`

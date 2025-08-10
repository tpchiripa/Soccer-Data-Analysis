# Soccer Data Analysis Project

## Overview
This project presents a comprehensive data analysis of player attributes sourced from the European Soccer Database. The primary objective is to explore player data, identify meaningful trends, and group players into distinct clusters based on their skills and characteristics using machine learning techniques. By leveraging data cleaning, feature scaling, and clustering algorithms, the project uncovers player profiles and offers insights into the different types of players in European soccer.

## Key Insights
- **Data Cleaning and Preparation:**  
  The initial dataset required significant cleaning, including handling missing values, which improved the quality and accuracy of subsequent analysis.

- **Feature Scaling and Clustering:**  
  By scaling player attributes and applying K-Means clustering, players were grouped into distinct clusters. Each cluster corresponds to a player type such as defenders, midfielders, attackers, and goalkeepers based on their statistical profiles.

- **Player Type Identification:**  
  Parallel coordinates plots provided a powerful visualization tool that highlighted the defining attributes of each player cluster. This visualization demonstrated how different player types excel in different areas — for example, defenders have high marking and tackling scores, while attackers show high finishing and shot power.

## Requirements
The following Python libraries are required to run this notebook:
- `sqlite3`
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `sklearn` (specifically `KMeans` and `scale` from `sklearn.cluster` and `sklearn.preprocessing`)

## Data Source
The dataset used in this project is the [European Soccer Database](https://www.kaggle.com/hugomathien/soccer) from Kaggle, which contains detailed information on players, matches, and teams from 11 European leagues spanning the years 2008 to 2016.

## Disclaimer
This project was created solely for educational purposes to demonstrate workflows in data analysis and machine learning.


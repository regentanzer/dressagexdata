import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

# Database Connection
conn = sqlite3.connect('dressage.db')

###############################################
##### Distribution of Scores Across Tests #####
###############################################
# Query
data = "SELECT test_year, test_level, percentage_score FROM test_results"
df = pd.read_sql_query(data, conn)

# Boxplot
plt.figure(figsize=(10,6))
sns.boxplot(x='test_level', y='percentage_score', hue='test_year', data=df)
plt.title('Distribution of Percentage Scores by Test Level and Year')
plt.ylabel('Percentage Score')
plt.xlabel('Test Level')
plt.legend(title='Test Year', loc='upper right')
plt.xticks(rotation=45)
plt.tight_layout()

# Save Figure
plt.savefig('output/overall_score_distribution.png') 
conn.commit()  



##################################
##### Judge Ratings by Score #####
##################################
# Query
data = "SELECT judge_rating, percentage_score, test_level FROM test_results"
df = pd.read_sql_query(data, conn)

# Boxplot
plt.figure(figsize=(10,6))
sns.boxplot(x='judge_rating', y='percentage_score', hue='test_level', data=df)
plt.title('Judge Rating vs. Percentage Score by Test Level')
plt.xlabel('Judge Rating')
plt.ylabel('Percentage Score')
plt.tight_layout()

# Save Figure
plt.savefig('output/judge_score.png') 
conn.commit()  



############################
##### Scores over Time #####
############################

# Query the data
data = "SELECT test_datetime, percentage_score FROM test_results"
df = pd.read_sql_query(data, conn)
df['test_datetime'] = pd.to_datetime(df['test_datetime'])
df['test_year'] = df['test_datetime'].dt.year

# Boxplot
plt.figure(figsize=(10,6))
sns.boxplot(x='test_year', y='percentage_score', data=df)
plt.title('Distribution of Percentage Scores by Year')
plt.xlabel('Year')
plt.ylabel('Percentage Score')
plt.tight_layout()
plt.show()

# Save Figure
plt.savefig('output/scores_by_year.png') 
conn.commit()



###########################################
##### Scatterplot of Scores Over Time #####
###########################################
# Query 
data = "SELECT test_datetime, percentage_score, test_level, test_id FROM test_results"
df = pd.read_sql_query(data, conn)
df['test_datetime'] = pd.to_datetime(df['test_datetime'])

# Ordering Test Levels
df = df.sort_values(by='test_id')
test_level_order = {level: i for i, level in enumerate(df['test_level'].unique())}
df['level_order'] = df['test_level'].map(test_level_order)

# Scatter Plot
plt.figure(figsize=(10,6))

# Color map
norm = plt.Normalize(df['level_order'].min(), df['level_order'].max())
cmap = plt.cm.Blues 
cmap = cmap(np.linspace(0.3, 1.0, cmap.N)) 
cmap = plt.cm.colors.ListedColormap(cmap)

scatter = sns.scatterplot(x='test_datetime', y='percentage_score', hue='level_order', palette=cmap, 
                          hue_norm=norm, data=df, legend=False)

for level, order in test_level_order.items():
    scatter.scatter([], [], color=cmap(norm(order)), label=level)

plt.legend(title='Test Level', loc='center left', bbox_to_anchor=(1, 0.5))

# Color bar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])

# Plot customization
plt.title('Scores Over Time By Level')
plt.xlabel('Test Date')
plt.ylabel('Percentage Score')
plt.show()

# Save Figure
plt.savefig('output/scatterplot_scores_by_time_level.png')
conn.commit()



##############################################
##### Avg Movement Score by Type by Gait #####
##############################################
# Query
data = """
SELECT 
    CASE 
        WHEN movement_direction = 'Straight' AND movement_gait = 'Passage to Piaffe to Passage' THEN 'Centerline'
        WHEN movement_type = 'Transition' THEN 'Transition'
        WHEN movement_type = 'Lead Change' AND movement_gait LIKE '%to%' THEN 'Simple Change'
        WHEN movement_type = 'Centerline' THEN 'Centerline'
        WHEN LOWER(movement_gait) LIKE '%canter%' THEN 'Canter'
        WHEN LOWER(movement_gait) LIKE '%trot%' THEN 'Trot'
        WHEN LOWER(movement_gait) LIKE '%walk%' THEN 'Walk'
        ELSE TRIM(movement_gait)
    END AS movement_gait, 
    movement_direction,
    AVG(score) AS average_score
FROM 
    movement_results
WHERE 1=1
    AND movement_direction <> 'Serpentine'
GROUP BY 1,2
"""
df = pd.read_sql_query(data, conn)

# Pivot the DataFrame to get the format needed for a heatmap
heatmap_data = df.pivot(index="movement_direction", columns="movement_gait", values="average_score")


# Create the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu", cbar_kws={'label': 'Average Score'})

# Plot customization
plt.title('Average Scores by Movement Direction and Gait')
plt.xlabel('Movement Gait')
plt.ylabel('Movement Direction')
plt.tight_layout()
plt.show()

# Save the heatmap as an image
plt.savefig('output/heatmap_average_scores.png')
conn.commit()

# Close Connection
conn.close()
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import numpy as np

# Connect to the database
conn = sqlite3.connect('dressage.db')







#####################################################
##### Avg Movement Score by Type by Gait - TC #####
#####################################################
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
    AND horse_show_name = 'The Alchemist'
GROUP BY 1,2
"""
df = pd.read_sql_query(data, conn)

# Pivot the DataFrame to get the format needed for a heatmap
heatmap_data = df.pivot(index="movement_direction", columns="movement_gait", values="average_score")


# Create the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu", cbar_kws={'label': 'Average Score'})

# Plot customization
plt.title('Average Scores by Movement Direction and Gait - TC')
plt.xlabel('Movement Gait')
plt.ylabel('Movement Direction')
plt.tight_layout()
plt.show()

# Save the heatmap as an image
plt.savefig('output/heatmap_average_scores_tc.png')
conn.commit()


"""

###################################
##### Movement Scores by Type #####
###################################
# Query
data = "SELECT movement_type, score FROM movement_results"
df = pd.read_sql_query(data, conn)

# Boxplot
plt.figure(figsize=(10,6))
sns.boxplot(x='movement_type', y='score', data=df)
plt.title('Movement Type vs. Score')
plt.xlabel('Movement Type')
plt.ylabel('Score')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Save Figure
plt.savefig('output/movement_type.png') 
conn.commit()  

"""

conn.close()
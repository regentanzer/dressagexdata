import sqlite3
import pandas as pd

conn = sqlite3.connect('dressage.db')
test_results = pd.read_sql_query("SELECT overall_results_id, gaits_mark, impulsion_mark, submission_mark, rider_mark, rider_position_mark, rider_effectiveness_mark, rider_harmony_mark, percentage_score  FROM test_results", conn)
movement_results = pd.read_sql_query("SELECT individual_scores_id, score FROM movement_results", conn)

def descriptive_stats(df):
    print("Descriptive Stats:")
    print(df.describe())

## Overall Results ##
print("Overall Results")
descriptive_stats(test_results)
descriptive_stats(movement_results)

## Regentanzer Results ##
print("Regentanzer Results")
test_results_rico = pd.read_sql_query("SELECT overall_results_id, gaits_mark, impulsion_mark, submission_mark, rider_mark, rider_position_mark, rider_effectiveness_mark, rider_harmony_mark, percentage_score  FROM test_results WHERE horse_show_name = 'Regentanzer'", conn)
movement_results_rico = pd.read_sql_query("SELECT individual_scores_id, score FROM movement_results  WHERE horse_show_name = 'Regentanzer'", conn)

descriptive_stats(test_results_rico)
descriptive_stats(movement_results_rico)

## The Alchemist Results ##
print("The Alchemist Results")
test_results_tc = pd.read_sql_query("SELECT overall_results_id, gaits_mark, impulsion_mark, submission_mark, rider_mark, rider_position_mark, rider_effectiveness_mark, rider_harmony_mark, percentage_score  FROM test_results WHERE horse_show_name = 'The Alchemist'", conn)
movement_results_tc = pd.read_sql_query("SELECT individual_scores_id, score FROM movement_results  WHERE horse_show_name = 'The Alchemist'", conn)

descriptive_stats(test_results_tc)
descriptive_stats(movement_results_tc)

conn.close()
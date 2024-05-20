import pandas as pd
import sqlite3
import numpy as np

con=sqlite3.connect("C:\\Users\\regen\\Documents\\Python\\dressage_database.sqlite")

overall_results = pd.read_sql_query("SELECT * FROM overall_results", con)
individual_scores = pd.read_sql_query("SELECT * FROM individual_scores", con)
test_movements = pd.read_sql_query("SELECT * FROM test_movements", con)
test = pd.read_sql_query("SELECT * FROM test", con)
horse = pd.read_sql_query("SELECT * FROM horse", con)
judge = pd.read_sql_query("SELECT * FROM judge", con)
show = pd.read_sql_query("SELECT * FROM show", con)
facility = pd.read_sql_query("SELECT * FROM facility", con)

"""
print(overall_results)
print(individual_scores)
print(test_movements)
print(test)
print(horse)
print(judge)
print(show)
print(facility)
"""
# Display Settings
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 80)
#pd.describe_option('display')

# Update Column Names
#overall_results = overall_results.rename(columns={"Horse":"HorseShowName","Judge":"JudgeName"})
#horses = horses.rename(columns={"ShowName":"HorseShowName"})
#show_judge = show_judge.rename(columns={"Judge":"JudgeName"})
#show = show.rename(columns={"ShowFacility":"FacilityName"})

# Update Individual Records
#overall_results.loc[overall_results['OverallResultsID'] == 97, ['Points']] = [187] 
#overall_results.loc[overall_results['OverallResultsID'] == 98, ['Points']] = [183.5] 
#overall_results.loc[overall_results['OverallResultsID'] == 99, ['Points']] = [225.5] 
##overall_results.loc[overall_results['OverallResultsID'] == 100, ['Points']] = [211.5] 
#judges.loc[judges['JudgeID'] == 10, ['JudgeName']] = ['Creeky Routsen'] 
#judges.loc[judges['JudgeID'] == 20, ['JudgeName']] = ['Janet Curtis']
#judges.loc[judges['JudgeID'] == 22, ['JudgeName']] = ['Melanie Kessler']
#judges.loc[judges['JudgeID'] == 24, ['JudgeName']] = ['Melissa Creswick']
#judges.loc[judges['JudgeID'] == 27, ['JudgeName']] = ['Cauleen Glass']
#overall_results.loc[overall_results['OverallResultsID'] == 60, ['JudgeName']] = ['Fran Dearing']



# Lowercase movements
test_movements['movement_type'] = test_movements['movement_type'].str.lower()
test_movements['movement_gait'] = test_movements['movement_gait'].str.lower()
test_movements['movement_direction'] = test_movements['movement_direction'].str.lower()


# Merge/Joins

os = pd.merge(pd.merge(pd.merge(overall_results,judge[judge.duplicated(subset='judge_id',keep="first")==False],on='judge_id',suffixes=('', '_DROP')),show[show.duplicated(subset='show_id',keep="first")==False], on="show_id",suffixes=('', '_DROP')),test[test.duplicated(subset='test_id',keep='first')==False],on='test_id',suffixes=('','_DROP')).filter(regex='^(?!.*_DROP)').drop_duplicates()
im = pd.merge(pd.merge(pd.merge(individual_scores,test_movements[test_movements.duplicated(subset='movement_id',keep="first")==False],on="movement_id",suffixes=('', '_DROP')),overall_results[overall_results.duplicated(subset='overall_results_id',keep="first")==False], on="overall_results_id",suffixes=('', '_DROP')),horse[horse.duplicated(subset='horse_id',keep="first")==False],on="horse_id",suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')

#print(os)
#print(im)

#print(os["overall_results_id"].nunique())
#print(im["individual_scores_id"].nunique())

#print(os.columns)

# Create Percentage Column
os['percentage'] = os['points_earned']/os['test_total_points']

print(os)

# Change Data Types
from datetime import datetime
#def ___convert_to_datetime(d):
#    return datetime.strptime(np.datetime_as_string(d,unit='s'), '%Y-%m-%dT%H:%M:%S')
    
#individual_scores["Score"] = pd.to_numeric(individual_scores["Score"])
#overall_results["DateTime"] = pd.to_datetime(overall_results["DateTime"])
#overall_results["DateTime"] = ___convert_to_datetime(overall_results["DateTime"])


# Extract DateTime Fields
#overall_results['Year'] = pd.DatetimeIndex(overall_results['DateTime']).year
#overall_results['Month'] = pd.DatetimeIndex(overall_results['DateTime']).month
#overall_results['Hour'] = pd.DatetimeIndex(overall_results['DateTime']).hour

#overall_results['AMPM'] = np.where(overall_results['Hour'] > 11,'Afternoon','Morning')
#overall_results['LuckyNumber'] = np.where(overall_results['Number'] < 100,'Less than 100','More than 100')

# Two Judges
#overall_results['TestOrder'] = np.where(overall_results.groupby('Date')['DateTime'].rank(method='first', ascending = True) == 1.0,'First Test','Not First Test')


#print(overall_results.dtypes)
#print(overall_results["DateTime"])
#overall_results["TwoJudges"] = overall_results[overall_results["DateTime"]].duplicated(keep=False)
# would like the above code to flag all duplicates as duplicates but alas, it does not work 

#overall_results['TwoJudges'] = np.where(overall_results.groupby('DateTime')['DateTime'].rank(method='first', ascending = True) == 1.0,'Not Duplicated Test','Duplicated Test')

#print(overall_results[['OverallResultsID','HorseShowName','JudgeName','DateTime','TwoJudges','TestOrder']].sort_values(by=['DateTime']))



"""
print(overall_results.dtypes)
print(horses.dtypes)
print(show.dtypes)
print(tests.dtypes)
"""

# Select first 5 rows
"""
print(overall_results.head(5))
"""

# Select individual columns
"""
print(tests[['TestID','Level']])
"""

# Where clause/Filters
"""
FourthLevel = tests[tests.Level == 'Fourth'][['Level','TestID','TotalPoints']]
ThirdLevel = tests[tests.Level == 'Third'][['Level','TestID','TotalPoints']]
print(FourthLevel)
print(ThirdLevel)
"""

# Select distinct/unique values
"""
print(tests.Level.unique())
"""

# Count distinct / number of unique values
"""
print(tests.Level.nunique())
"""

# Count rows (select x, count(x))
"""
print(tests.Level.value_counts())
"""

# Case when / functions

"""
print(overall_results["Points"])

points = overall_results["Points"]
totalpoints = overall_results["TestPoints"]
"""

# Aggregates
"""
# Average Points by Level
ptsbylevel = tests[['Level','TotalPoints']].groupby('Level').mean()\
    .sort_values(by='TotalPoints', ascending=False)
print(ptsbylevel.sort_values(by=['TotalPoints'])) 

# Average Percentage by Test
avgpctbytest = overall_results[['LevelTest','Percentage']].groupby('LevelTest').mean()\
    .sort_values(by='Percentage', ascending=False)
print(avgpctbytest.sort_values(by=['Percentage']))

# Median Percentage by Test
avgpctbytest = overall_results[['LevelTest','Percentage']].groupby('LevelTest').median()\
    .sort_values(by='Percentage', ascending=False)
print(avgpctbytest.sort_values(by=['Percentage']))

# Average Percentage by Horse
avgpctbyhorse = overall_results[['ShowName','Percentage']].groupby('ShowName').mean()\
    .sort_values(by='Percentage', ascending=False)
print(avgpctbyhorse.sort_values(by=['Percentage']))

# Median Percentage by Horse
avgpctbyhorse = overall_results[['ShowName','Percentage']].groupby('ShowName').median()\
    .sort_values(by='Percentage', ascending=False)
print(avgpctbyhorse.sort_values(by=['Percentage']))
"""


"""
def agg(table, variable, aggregateby):
    table=table
    variable=variable
    aggregateby = aggregateby
    avg = table[[variable,aggregateby]].groupby(variable).mean()\
        .sort_values(by=aggregateby, ascending=False)
    med = table[[variable,aggregateby]].groupby(variable).median()
    min = table[[variable,aggregateby]].groupby(variable).min()
    max = table[[variable,aggregateby]].groupby(variable).max()
    count = table[[variable,aggregateby]].groupby(variable).count()
    merge = pd.merge(pd.merge(pd.merge(pd.merge(avg, med, on=variable, sort = False), min,on=variable,sort=False),max,on=variable,sort=False),count,on=variable,sort=False)
    merge.columns = ["Average","Median","Minimum","Maximum","Count"]
    print(merge)
    return


# Aggregates by Test/Number
print(agg(os,'TestOrder','Percentage'))
print(agg(os,'NumberParse','Percentage'))
"""


#print(os)

# Compare collective mark average to individual average
# Compare total score average of first test to second test



# to work on:
#   text analysis of comments by horse by level etc
#   plots
#   add judge levels
#   time between tests
#   first or second test
#   collective scores




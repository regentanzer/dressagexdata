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

# Lowercase movements
test_movements['movement_type'] = test_movements['movement_type'].str.lower()
test_movements['movement_gait'] = test_movements['movement_gait'].str.lower()
test_movements['movement_direction'] = test_movements['movement_direction'].str.lower()

# Merge/Joins
os = pd.merge(pd.merge(pd.merge(pd.merge(pd.merge(overall_results,judge[judge.duplicated(subset='judge_id',keep="first")==False],on='judge_id',suffixes=('', '_DROP')),show[show.duplicated(subset='show_id',keep="first")==False], on="show_id",suffixes=('', '_DROP')),test[test.duplicated(subset='test_id',keep='first')==False],on='test_id',suffixes=('','_DROP')),horse[horse.duplicated(subset='horse_id',keep='first')==False],on='horse_id',suffixes=('','_DROP')),facility[facility.duplicated(subset='facility_id',keep='first')==False],on='facility_id',suffixes=('','_DROP')).filter(regex='^(?!.*_DROP)').drop_duplicates()
im = pd.merge(pd.merge(pd.merge(individual_scores,test_movements[test_movements.duplicated(subset='movement_id',keep="first")==False],on="movement_id",suffixes=('', '_DROP')),overall_results[overall_results.duplicated(subset='overall_results_id',keep="first")==False], on="overall_results_id",suffixes=('', '_DROP')),horse[horse.duplicated(subset='horse_id',keep="first")==False],on="horse_id",suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')

# Data Types
os['test_level'] = os['test_level'].astype(str)
os['test_number'] = os['test_number'].astype(str)
im['score'] = pd.to_numeric(im['score'])

#Create Columns 
os['percentage'] = os['points_earned']/os['test_total_points']
os['test_level_number']=os['test_level']+' Test '+os['test_number']

# Function to calculate Average, Median, Minimum, Maxmimum, and Count
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
"""
print("\n\n\n\n\n*****************AGGREGATES OVERALL*****************\n\n\n\n\n")

# Aggregates by Horse
print(agg(os,'horse_show_name','percentage'))

# Aggregates by Test 
print(agg(os,'test_level','percentage'))
print(agg(os,'test_name','percentage'))
print(agg(os,'test_level_number','percentage'))

# Aggregates by Judge
print(agg(os,'judge_name','percentage'))
print(agg(os,'judge_gender','percentage'))

# Aggregates by Facility/Show
print(agg(os,'show_name','percentage'))
print(agg(os,'facility_name','percentage'))

# Aggregates by Movement
#print(agg(im,'movement_name','score'))

print(agg(im,'coefficient','score'))
print(agg(im,'movement_type','score'))
print(agg(im,'is_lateral_work','score'))
print(agg(im,'is_lengmedext','score'))
print(agg(im,'movement_direction','score'))
print(agg(im,'movement_gait','score'))
"""

"""
print("\n\n\n\n\n*****************AGGREGATES BY RICO*****************\n\n\n\n\n")

# Aggregates by Test
print(agg(os[os["horse_show_name"]=="Regentanzer"],'test_level','percentage'))
print(agg(os[os["horse_show_name"]=="Regentanzer"],'test_name','percentage'))
print(agg(os[os["horse_show_name"]=="Regentanzer"],'test_level_number','percentage'))

# Aggregates by Judge
print(agg(os[os["horse_show_name"]=="Regentanzer"],'judge_name','percentage'))
print(agg(os[os["horse_show_name"]=="Regentanzer"],'judge_gender','percentage'))

# Aggregates by Facility/Show
print(agg(os[os["horse_show_name"]=="Regentanzer"],'show_name','percentage'))
print(agg(os[os["horse_show_name"]=="Regentanzer"],'facility_name','percentage'))

# Aggregates by Movement
print(agg(im[im["horse_show_name"]=="Regentanzer"],'coefficient','score'))
#print(agg(im[im["horse_show_name"]=="Regentanzer"],'movement_name','score'))
print(agg(im[im["horse_show_name"]=="Regentanzer"],'movement_type','score'))
print(agg(im[im["horse_show_name"]=="Regentanzer"],'is_lateral_work','score'))
print(agg(im[im["horse_show_name"]=="Regentanzer"],'is_lengmedext','score'))
print(agg(im[im["horse_show_name"]=="Regentanzer"],'movement_direction','score'))
print(agg(im[im["horse_show_name"]=="Regentanzer"],'movement_gait','score'))

"""
print("\n\n\n\n\n*****************AGGREGATES BY TC*****************\n\n\n\n")

# Aggregates by Test
print(agg(os[os["horse_show_name"]=="The Alchemist"],'test_level','percentage'))
print(agg(os[os["horse_show_name"]=="The Alchemist"],'test_name','percentage'))
print(agg(os[os["horse_show_name"]=="The Alchemist"],'test_level_number','percentage'))

# Aggregates by Judge
print(agg(os[os["horse_show_name"]=="The Alchemist"],'judge_name','percentage'))
print(agg(os[os["horse_show_name"]=="The Alchemist"],'judge_gender','percentage'))

# Aggregates by Facility/Show
print(agg(os[os["horse_show_name"]=="The Alchemist"],'show_name','percentage'))
print(agg(os[os["horse_show_name"]=="The Alchemist"],'facility_name','percentage'))

# Aggregates by Movement
print(agg(im[im["horse_show_name"]=="The Alchemist"],'coefficient','score'))
#print(agg(im[im["horse_show_name"]=="The Alchemist"],'movement_name','score'))
print(agg(im[im["horse_show_name"]=="The Alchemist"],'movement_type','score'))
print(agg(im[im["horse_show_name"]=="The Alchemist"],'is_lateral_work','score'))
print(agg(im[im["horse_show_name"]=="The Alchemist"],'is_lengmedext','score'))
print(agg(im[im["horse_show_name"]=="The Alchemist"],'movement_direction','score'))
print(agg(im[im["horse_show_name"]=="The Alchemist"],'movement_gait','score'))





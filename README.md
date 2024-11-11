# dressagexdata
This is a project I've been wanting to do for years and I finally sat down and have been working on it. 

From 2004 to 2020, I was a competitive dressage rider. I've competed from the lowest levels through to the Grand Prix, primarily on two horses (Regentanzer and The Alchemist), but I have included tests from two other horses (Larkin, who I started my dressage career on, and Le Mans, my trainer's horse who I did my first FEI tests on). 

This data shows the many mistakes I've made and some pretty scathing comments. But it also shows my accomplishments and some incredibly kind words. It shows how I grew as a rider on two very different horses. And this project is the culmination of it all, as in 2021 I shut down my horse training business for good and am now working as a Data Engineer in tech and living the amateur lifestyle with TC (The Alchemist) who is mostly trail riding right now.

## Database Setup
I used a SQLite3 database. 

## Data Modeling
I probably went a little overboard with the data modeling, my plan was to fully flesh out the facility, judge, and show tables with additional information that I could cut the data by. 

For example, I've been drawn to certain facilities and will eventually add more information regarding footing, distance from my home barn, and even the spookiness of the facility. Potentially I may want to add location data so that I can retrieve historical weather data. At least one of these tests was ridden in a wind storm that drastically reduced the score due to tension. 

## Analysis 
My primary desire for doing this project was to answer pressing questions such as:
- What is my lucky number?
- Are younger and/or lower level dressage judges actually meaner? (A common claim)
- Did my rider scores go up over the years? 

And some additional, more serious questions cropped up as well:
- Which horse did I score better on?
- Which level did I compete the most?
- Which collective movements accounted for the most variance in the overall score?
- How did the sentiment of my comments change over time?

## Descriptive Statistics
To answer a lot of these questions, I built out some descriptive statistics 



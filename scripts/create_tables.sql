DROP TABLE IF EXISTS test_results;
CREATE TABLE test_results AS
SELECT 
    o.overall_results_id,
    t.test_id,
    o.test_datetime,
    t.test_year,
    t.test_level,
    t.test_number,
    CASE
        WHEN t.test_number IS NULL THEN t.test_level
        ELSE CONCAT(t.test_level,' Test ',CAST(test_number AS VARCHAR))
        END AS test_name,
    j.judge_name,
    o.judge_rating,
    j.judge_gender,
    h.horse_show_name,
    CAST(SUBSTR(o.test_datetime,7,4) AS INT) - h.horse_yob AS horse_age,
    -- this can't be done with a substring since it will be 10/26/2004 vs 5/2/2004
    o.points_earned, 
    o.gaits_mark,
    o.impulsion_mark,
    o.submission_mark,
    o.rider_mark,
    o.rider_position_mark,
    o.rider_effectiveness_mark,
    o.rider_harmony_mark,
    o.overall_comments,
    (o.points_earned * 1.0 / t.test_total_points) AS percentage_score
FROM overall_results o
JOIN tests t 
ON o.test_id = t.test_id
JOIN horse h 
ON o.horse_id = h.horse_id
JOIN judge j 
ON o.judge_id = j.judge_id
;

DROP TABLE IF EXISTS movement_results;
CREATE TABLE movement_results AS
SELECT 
    i.individual_scores_id,
    r.overall_results_id,
    r.test_datetime,
    r.test_year,
    r.test_level,
    r.test_number,
    r.test_name,
    r.judge_name,
    r.judge_rating,
    r.judge_gender,
    r.horse_show_name,
    r.horse_age,
    t.movement_name,
    t.movement_type,
    t.is_lateral_work,
    t.is_lengmedext,
    t.movement_direction,
    t.movement_gait,
    i.coefficient,
    i.score,
    i.points,
    t.movement_total_points,
    i.comment
FROM individual_scores i
JOIN test_results r
ON i.overall_results_id = r.overall_results_id
JOIN test_movements t
ON i.movement_id = t.movement_id
;
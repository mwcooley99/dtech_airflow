import itertools
from sqlalchemy import create_engine
from statistics import mean
import itertools
import math

def calculate_outcome_average(outcome_results):
    """ Return the simple average, with or without the lowest score dropped, whichever is greater
    Keyword arguments:
    outcome_results -- list of results for a single user, course, outcome. 
    Must be sorted by user_id, course_id, outcome_id, score, last_assessed_at in ascending order.
    """
    # Get columns names and values from the first row
    first_outcome_result = outcome_results[0]
    keys = ["user_id", "course_id", "outcome_id"]
    outcome_average = {key: first_outcome_result[key] for key in keys}

    # If there's only one the drop_average is set to zero so it will never be the max.
    if len(outcome_results) == 1:
        drop_average = 0
    else:
        drop_average = round(mean([outcome_result["score"] for outcome_result in outcome_results[1:]]), 2)
    average = round(mean([outcome_result["score"] for outcome_result in outcome_results]), 2)

    outcome_average["outcome_average"] = max(drop_average, average)
    return outcome_average

def get_outcome_results(engine, stmt):
    with engine.connect() as conn:
        keys = ["user_id", "course_id", "outcome_id", "score", "submitted_or_assessed_at"]
        outcome_results = [dict(zip(keys, res)) for res in conn.execute(stmt)]
    
    return outcome_results

def get_outcome_averages(outcome_results):
    # print(outcome_results[0])
    outcome_results_groups = itertools.groupby(outcome_results, lambda x: (x["user_id"], x["course_id"], x["outcome_id"]))
    
    outcome_averages = [calculate_outcome_average(list(group)) for key, group in outcome_results_groups]
    return outcome_averages

def calculate_traditional_grade(scores, calculation_dictionaries):
    # check if the outcome is assessed.
    first_score = scores[0]
    grade_cols = [
        "course_id",
        "user_id",
    ]
    grade = {key: first_score[key] for key in grade_cols}
    scores = [score["outcome_average"] for score in scores]

    if len(scores) == 0 or scores[0] == -1:
        grade["grade"] = "n/a"
        grade["threshold"] = None
        grade["min_score"] = None
        return grade
 
    scores_sorted = sorted(scores, reverse=True)

    # Find the 75% threshold --> floored
    threshold_index = math.floor(0.75 * len(scores_sorted)) - 1

    # Calculate the threshold scores to generate grade
    grade["threshold"] = scores_sorted[threshold_index]
    grade["min_score"] = scores_sorted[-1]

    for _i in range(len(calculation_dictionaries)):
        curr_grade = calculation_dictionaries[_i]
        if grade["threshold"] >= curr_grade["threshold"] and grade["min_score"] >= curr_grade["min_score"]:
            grade["grade"] = curr_grade["grade"]
            return grade 
    grade["grade"] = calculation_dictionaries[-1]["grade"]
    return grade

def get_grade_dictionaries(engine):
    stmt = "select grade, threshold, min_score from grade_calculation order by grade_rank"
    with engine.connect() as conn:
        keys = ["grade", "threshold", "min_score"]
        grade_dictionaries = [dict(zip(keys, res)) for res in conn.execute(stmt)]

    return grade_dictionaries

def calculate_grades(outcome_averages, grade_dictionaries):
    outcome_average_groups = itertools.groupby(outcome_averages, lambda x: (x["user_id"], x["course_id"]))
    grades = [calculate_traditional_grade(list(group), grade_dictionaries) for key, group in outcome_average_groups]

    return grades

if __name__ == "__main__":
    engine = create_engine("postgresql://TheDoctor:secret@cbl-lti-app-db-1:5432/cbldb")
    stmt = """
        select
            user_id,
            course_id,
            outcome_id,
            score,
            submitted_or_assessed_at
        from raw_canvas.outcome_results
        where score is not null
        order by 1, 2, 3, 4, 5
    """
    outcome_results = get_outcome_results(engine, stmt)
    outcome_averages = get_outcome_averages(outcome_results)
    grade_dictionaries = get_grade_dictionaries(engine)
    grades = calculate_grades(outcome_averages, grade_dictionaries)
    print(grades)
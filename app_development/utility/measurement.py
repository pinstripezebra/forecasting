import pandas as pd
from random import randint


def makelist(count):
    return [randint(1, 100) for _ in range(count)]

test_optimal = {'temperature_2m': 20,
        'cloudcover': 5,
        'windspeed_10m': 0}

test_forecast = {'temperature_2m':makelist(200),
                 'cloudcover': makelist(200),
                 'windspeed_10m': makelist(200)
}

def measure_running_conditions(optimal_values, forecasted_values):

    '''helper function to measure difference between two lists, one containing
    forecasted conditions and one containing actual conditions'''

    score = sum([abs(i - j)^2 for i, j in zip(optimal_values, forecasted_values)])
    return score


def find_optimal_window(optimal_conditions, forecasted_conditions, max_window):

    '''takes forecasts of temperature and returns tuples cotnaining the optimal indices to go on a run
    ranked from best to worst

    INPUT:
        optimal_conditions: dict
            contains (feature: optimal_condition) pair where feature is wind, temp, etc in int form
        forecasted_conditions: dict
            contains (feature: forecast) pair where feature is wind, temp, etc and forecast is a list
        
    RETURNS:
        ranked_windows: list
            list of tupples containing the start/stop time for optimal runs
            ex. [(start1, stop1), (start2, stop2),...,(startn, stopn)]
    
    '''

    ranking_indice, ranking = [],[]
    
    factor_keys = list(optimal_conditions.keys())
    optimal_values = [optimal_conditions[i] for i in factor_keys]
    # Iterating through all indices and evaluating score
    for indice in range(len(forecasted_conditions[factor_keys[0]])):

        # returning forecasted values at current timestep
        forecasted_values = [forecasted_conditions[i][indice] for i in factor_keys]

        # evaulating quality at current indice
        current_score = measure_running_conditions(optimal_values, forecasted_values)
        ranking_indice.append(indice)
        ranking.append(current_score)

    score_df = pd.DataFrame({'Indice': ranking_indice,
                             'Score': ranking}).sort_values(by = 'Score').reset_index(drop=True)
    return score_df



# Testing function
#score = find_optimal_window(test_optimal, test_forecast, 1000)
#print(score)

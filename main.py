from datetime import datetime, timedelta
from scipy.interpolate import make_interp_spline, BSpline
from collections import defaultdict

import time
import numpy as np
import matplotlib.pyplot as plt
import os

# TODO: Converter os arquivos em csv
# TODO: Definir um score de maturação
# TODO: Montar um gráfico de dispersão
# TODO: Teste de média entre os grupos verietais e entre os locais.
# TODO: Definir se vai ser um modelo linear ou nao linear.
# TODO: Testar os ajustes dos modelos, com (Temperatura, chuva, irradiação, umidade relativa)
# TODO: Definir melhor modelo
# TODO: Validação cruzada
# TODO: Explica o modelo

COLOR_WEIGHTS = {'white': 0,
                 'yellow': 40,
                 'orange': 60,
                 'brown': 80,
                 'black': 100}


def parse_zero(data_string, position_0, position_1):
    try:
        return float(data_string[position_0].split(';')[position_1])
    except ValueError:
        return 0.0


def open_and_parse_csv(f_name):
    peanut_colors = {'dates': [],
                     'white': [],
                     'yellow': [],
                     'orange': [],
                     'brown': [],
                     'black': []}
    with open(f_name, 'r') as f:
        f_as_list = f.readlines()
        lines = 0
        date_col_line = [2, 1]
        colors = [5, 3]
        amount_of_tables = int((len(f_as_list) + 1)/12)
        for i in range(0, amount_of_tables):
            date = f_as_list[date_col_line[0]].split(';')[date_col_line[1]]
            date = datetime.strptime(date, '%d/%m/%Y').date()
            peanut_colors['dates'].append(date)
            peanut_colors['white'].append(parse_zero(f_as_list, colors[0], colors[1]))
            peanut_colors['yellow'].append(parse_zero(f_as_list, colors[0] + 1, colors[1]))
            peanut_colors['orange'].append(parse_zero(f_as_list, colors[0] + 2, colors[1]))
            peanut_colors['brown'].append(parse_zero(f_as_list, colors[0] + 3, colors[1]))
            peanut_colors['black'].append(parse_zero(f_as_list, colors[0] + 4, colors[1]))

            lines += 12
            date_col_line[0] += 12
            colors[0] += 12

        return peanut_colors


def plot_place(data_dict):
    plt.xlim(data_dict['dates'][0] + timedelta(days=-1),
             data_dict['dates'][-1] + timedelta(days=+1))
    for k, v in data_dict.items():
        if k != 'dates':
            plt.scatter(data_dict['dates'], v, color=k)
    plt.show()


def calculate_score(score_dict):
    sum_of_weights = 0
    for k, v in score_dict.items():
        sum_of_weights += v * COLOR_WEIGHTS[k]
    return sum_of_weights/100


def compute_weights(parsed_maturity_scores):
    parsed_maturity_scores['scores'] = []
    for i in range(len(parsed_maturity_scores['dates'])):
        scores = {}
        for k, v in parsed_maturity_scores.items():
            if k not in ['dates', 'scores']:
                scores[k] = v[i]
        parsed_maturity_scores['scores'].append(calculate_score(scores))

    return parsed_maturity_scores


def plot_maturity_score_graph(computed_scores, graph_name):
    dates = np.array([time.mktime(i.timetuple()) for i in computed_scores['dates']])
    # dates = np.array([float(i) for i in range(0, len(computed_scores['scores']))])
    scores = np.array(computed_scores['scores'])

    plt.plot(computed_scores['dates'], computed_scores['scores'])
    plt.show()

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.set_title('Curva de maturação {}'.format(graph_name))
    # INTERPOLATION
    X_Y_Spline = make_interp_spline(dates, scores)
    X_ = np.linspace(dates.min(), dates.max(), 20)
    Y_ = X_Y_Spline(X_)
    X_ = [datetime.utcfromtimestamp(i).strftime('%d/%m/%Y') for i in X_]
    fig.autofmt_xdate()
    plt.plot(X_, Y_)
    ax.set_xlabel("Data")
    ax.set_ylabel("Score de maturação")
    plt.savefig('fig_maturacao/{}.png'.format(graph_name))
    plt.show()


def parse_data_into_single_dict_of_lists():
    list_of_maturity_points = defaultdict(list)
    for f_name in os.listdir('.'):
        if f_name.endswith('.csv'):
            data = open_and_parse_csv(f_name)
            computed_maturity = compute_weights(data)
            for k, v in computed_maturity.items():
                list_of_maturity_points[k].extend(v)
    return list_of_maturity_points


def plot_dispersion():
    data = parse_data_into_single_dict_of_lists()
    for date, maturity_measure in map(list, zip(data['dates'], data['scores'])):
        plt.scatter(date, maturity_measure, color='green')
    plt.savefig('maturity.png')
    plt.show()
    # for k, v in data.items():
    #     if k != 'dates':
    #         print(k)
    #         for date, maturity_measure in map(list, zip(data['dates'], v)):
    #             plt.scatter(date, maturity_measure, color=k)

if __name__ == '__main__':

    # data = open_and_parse_csv('cazarotto.csv')
    # computed_maturity = compute_weights(data)
    # plot_maturity_score_graph(computed_maturity, 'Cazarotto')
    # print("fim cazarotto")
    #
    # data = open_and_parse_csv('fernando.csv')
    # computed_maturity = compute_weights(data)
    # plot_maturity_score_graph(computed_maturity, 'Fernando')
    # print("fim fernando")
    #
    # data = open_and_parse_csv('renato_camargo.csv')
    # computed_maturity = compute_weights(data)
    # plot_maturity_score_graph(computed_maturity, 'Renato Camargo')
    # print("fim renato camargo")
    #
    # data = open_and_parse_csv('renato_camargo_503.csv')
    # computed_maturity = compute_weights(data)
    # plot_maturity_score_graph(computed_maturity, 'Renato camargo 503')
    # print("fim renato camargo 503")

    print(plot_dispersion())




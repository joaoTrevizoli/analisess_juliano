if __name__ == '__main__':

    data = open_and_parse_csv('cazarotto.csv')
    plot_place(data, "Cazarotto IAC 503")

    computed_maturity = compute_weights(data)
    plot_maturity_score_graph(computed_maturity, 'Cazarotto')
    print("fim cazarotto")

    data = open_and_parse_csv('fernando.csv')
    plot_place(data, "Fernando IAC 503")

    # computed_maturity = compute_weights(data)
    # plot_maturity_score_graph(computed_maturity, 'Fernando')
    print("fim fernando")

    data = open_and_parse_csv('renato_camargo.csv')
    plot_place(data, "Renato Camargo OL3")

    # computed_maturity = compute_weights(data)
    # plot_maturity_score_graph(computed_maturity, 'Renato Camargo')
    print("fim renato camargo")

    data = open_and_parse_csv('renato_camargo_503.csv')
    plot_place(data, "Renato Camargo IAC 503")

    # computed_maturity = compute_weights(data)
    # plot_maturity_score_graph(computed_maturity, 'Renato camargo 503')
    print("fim renato camargo 503")

    print(plot_dispersion())
    # print(linear_regression())
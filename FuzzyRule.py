interest = ctrl.Antecedent(np.arange(0, 11, 1), 'interest')
popularity = ctrl.Antecedent(np.arange(0, 11, 1), 'popularity')
recommendation = ctrl.Consequent(np.arange(0, 11, 1), 'recommendation')

interest.automf(3)
popularity.automf(3)

recommendation['low'] = fuzz.trimf(recommendation.universe, [0, 0, 5])
recommendation['medium'] = fuzz.trimf(recommendation.universe, [0, 5, 10])
recommendation['high'] = fuzz.trimf(recommendation.universe, [5, 10, 10])

rule1 = ctrl.Rule(interest['poor'] | popularity['poor'], recommendation['low'])
rule2 = ctrl.Rule(interest['average'] & popularity['average'], recommendation['medium'])
rule3 = ctrl.Rule(interest['good'] | popularity['good'], recommendation['high'])

recommendation_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
recommendation_simulator = ctrl.ControlSystemSimulation(recommendation_ctrl)

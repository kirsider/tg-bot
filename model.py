import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model

import db


def verdict(user_id):
    usr = db.find_record(user_id)
    slist = usr['statlist']
    plt.clf()
    print(slist)
    if len(slist) < 1:
        return 'Позанимайтесь еще!'
    plt.plot(range(len(slist)), slist, 'or', label='your tries')
    regressor = linear_model.LinearRegression()
    regressor.fit(np.array(range(len(slist))).reshape(-1, 1), np.array(slist))
    a0 = regressor.intercept_
    a1 = regressor.coef_
    x = np.linspace(0, len(slist) - 1, num=100)
    plt.plot(x, a0 + a1 * x, label='regression')
    plt.xlabel('game number')
    plt.ylabel('accuracy')
    plt.legend(loc='best')

    plt.savefig('plot.png')
    if a1 < 0.001:
        return "Вам стоит подучиться!"
    else:
        return "Так держать!"

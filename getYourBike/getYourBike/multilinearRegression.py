import numpy as np
import statsmodels.api as sm

def detailedMultipleRegression(y, x):
    ones = np.ones(len(x[0]))
    X = sm.add_constant(np.column_stack((x[0], ones)))
    for ele in x[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    results = sm.OLS(y, X).fit()
    return results

def simpleMultipleRegression(y, x):
    X = np.column_stack(x+[[1]*len(x[0])])
    coefs = np.linalg.lstsq(X,y)[0]
    return coefs

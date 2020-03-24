from sklearn import preprocessing, metrics, neighbors, model_selection, svm, ensemble
import xgboost as xgb
import numpy as np
import matplotlib.pyplot as plt

def kfold_risk(X, y, mod, k):
    """ calculate the MSE of the model under k_fold cross validation
    Param:
        X: predict variables
        y: respose variables
        mod: module 
        k: k-fold
    Return:
        mean of risk
    """
    kf = model_selection.KFold(k)
    kf_risk = []
    for train_index, test_index in kf.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y[train_index], y[test_index]
        mod.fit(X_train, y_train)
        y_pred = np.round(mod.predict(X_test)/0.5)*0.5
        risk = metrics.mean_squared_error(y_pred,y_test)
        kf_risk.append(risk)
    mean_risk = np.mean(kf_risk)
    return(mean_risk)   


class Predictor():
    """
    Create predictors by KNN or SVM, fit the training data, 
    tune the parameters and make prediction on the test data
    """
    
    def __init__(self, para_list, model_type, k_fold = 5):
        """
        Param:
            para_list: list of hyperparameters
            model_type: string of model name
        """
        self.k_fold = k_fold
        self.model_type = model_type
        self.para_list = para_list
        self.models = []
        for para in self.para_list:
            if model_type == "KNN":
                model = neighbors.KNeighborsRegressor(para)
            if model_type == "SVM":
                model = svm.SVR(C = para, gamma = 'auto')
            self.models.append(model)
            
    def fit_and_tune(self, X_tr, y_tr):
        """ fit_and_tune
        Param:
            X_tr: X of training set
            y_tr: y of training set
        """
        self.calculate_MSE(X_tr, y_tr)
        self.plot_MSE()
        for i, MSE in enumerate(self.MSEs):
            if MSE == np.min(self.MSEs):
                print("The parameter tuned is {}".format(self.para_list[i]))
                self.choice_model = self.models[i]

    def predict(self, X_te, y_te):
        """ prediction
        Param:
            X_te: X of testing set
            y_te: y of testing set
        """
        y_pred = np.round(self.choice_model.predict(X_te)/0.5)*0.5
        MSE = metrics.mean_squared_error(y_pred,y_te)
        R_2 = self.choice_model.score(X_te, y_te)
        acc = sum(y_pred == y_te)/len(y_te)
        print('{}: the MSE on the test set is {}, the R_2 score is {}'.format(self.model_type,MSE, R_2))
        print("The accurancy is {}".format(acc))
        
    def calculate_MSE(self, X_tr, y_tr):
        """ calculate_MSE
        Param:
            X_tr: X of training set
            y_tr: y of training set
        """
        self.MSEs = []
        for model in self.models:
            MSE =  kfold_risk(X_tr,y_tr,model,self.k_fold)
            self.MSEs.append(MSE)
            
    def plot_MSE(self):
        """ make plot
        """
        plt.plot(self.para_list,self.MSEs,label = self.model_type)
        plt.ylabel('MSE')
        if self.model_type == "KNN":
            plt.xlabel('k (neighbors)')
        if self.model_type == "SVM":
            plt.xlabel('C')
        plt.title('The MSE of {} models with {}_fold CV'.format(self.model_type, self.k_fold))
        plt.legend()
        plt.show()

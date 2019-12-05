import os
import sys
sys.path.append('..')

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import sklearn
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold, StratifiedKFold, TimeSeriesSplit, GroupKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.utils import resample


import lightgbm


def rmsle(y_true, y_pred):
    '''Evaluation function for this competition'''
    # score = np.sqrt(metrics.mean_squared_log_error(y_true, pred))
    y_pred = np.clip(y_pred, 0.0, None)
    score = np.sqrt(np.mean(np.power(np.log1p(y_pred) - np.log1p(y_true), 2)))
    return score


def custom_metric(pred, data):
    return 'RMSLE', rmsle(data.get_label(), pred), False


metrics_func = rmsle


class Model():

    def __init__(self, model_type):
        self.model_type = model_type
        self.metric = None

    def _lgbm_train_and_predict(self, params, train_params, X_train, X_valid, y_train, y_valid, X_test):
        train_data = lightgbm.Dataset(X_train, label=y_train)
        valid_data = lightgbm.Dataset(X_valid, label=y_valid, reference=train_data)

        model = lightgbm.train(
            params,
            train_data,
            valid_sets=[train_data, valid_data],
            **train_params,
            feval=custom_metric
        )

        y_valid_pred = model.predict(X_valid, num_iteration=model.best_iteration)
        y_pred = model.predict(X_test, num_iteration=model.best_iteration)
        _, score, _ = custom_metric(y_valid_pred, valid_data)
        return y_pred, score, model

    def _xgb_train_and_predict(self, X_train, X_valid, y_train, y_valid, X_test):
        pass

    def _rf_train_and_predict(self, params, X_train, X_valid, y_train, y_valid, X_test):
        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)

        y_valid_pred = model.predict_proba(X_valid)[:, 1]
        y_pred = model.predict_proba(X_test)[:, 1]

        score = metrics_func(y_valid, y_valid_pred)
        return y_pred, score, model

    def train_and_predict(self, params, train_params, X, y, test, n_fold, is_shuffle, seed=None):
        y_preds = []
        scores = []
        models = []

        cv_method = KFold(n_splits=n_fold, shuffle=is_shuffle, random_state=seed)
        for i, (train_index, valid_index) in enumerate(cv_method.split(X)):
            print(f'\n--- Start Train of {i+1} Fold ---')
            X_train, y_train = X.iloc[train_index, :], y.iloc[train_index]
            X_valid, y_valid = X.iloc[valid_index, :], y.iloc[valid_index]

            if self.model_type == 'lgbm':
                y_pred, score, model = self._lgbm_train_and_predict(
                    params, train_params, X_train, X_valid, y_train, y_valid, test)
            else:
                y_pred, score, model = self._lgbm_train_and_predict(
                    params, train_params, X_train, X_valid, y_train, y_valid, test)

            y_preds.append(y_pred)
            scores.append(score)
            models.append(model)

        self.feature_importance = self.get_feature_importance(models)
        return y_preds, scores, models

    def get_feature_importance(self, models):
        feature_importance = pd.DataFrame(
            [model.feature_importance() for model in models],
            columns=models[0].feature_name()).T

        feature_importance['Agerage_Importance'] = feature_importance.iloc[:, :len(models)].mean(axis=1)
        feature_importance['importance_std'] = feature_importance.iloc[:, :len(models)].std(axis=1)

        feature_importance.sort_values(by='Agerage_Importance', inplace=True)
        return feature_importance

    def plot_importance(self, max_num_features=80, figsize=(24, 36)):
        plt.figure(figsize=figsize)
        self.feature_importance[-max_num_features:].plot(
            kind='barh', title='Feature importance', figsize=figsize,
            y='Agerage_Importance', xerr='importance_std',
            grid=True, align="center"
        )
        plt.legend()

    def save_feature_importance(self, filepath):
        fig_filepath = f'./figure/feature_importance/{filepath}.png'
        csv_filepath = f'./model/feature_importance/{filepath}.csv'

        if not os.path.exists(fig_filepath.rsplit('/', 1)[0]):
            os.makedirs(fig_filepath.rsplit('/', 1)[0])

        if not os.path.exists(csv_filepath.rsplit('/', 1)[0]):
            os.makedirs(csv_filepath.rsplit('/', 1)[0])

        plt.figure()
        self.plot_importance()
        plt.savefig(fig_filepath)
        plt.close('all')

        self.feature_importance.to_csv(csv_filepath, index=False)


class GroupKfoldModel(Model):
    def train_and_predict(self, params, train_params, X, y, test,
                          group_col, n_fold, is_shuffle, seed=None):
        y_preds = []
        scores = []
        models = []

        cv_method = GroupKFold(n_splits=n_fold)
        for i, (train_index, valid_index) in enumerate(cv_method.split(X, y, X[group_col])):
            print(f'\n--- Start Train of {i+1} Fold ---')
            X_train, y_train = X.iloc[train_index, :], y.iloc[train_index]
            X_valid, y_valid = X.iloc[valid_index, :], y.iloc[valid_index]

            if self.model_type == 'lgbm':
                y_pred, score, model = self._lgbm_train_and_predict(
                    params, train_params, X_train, X_valid, y_train, y_valid, test)
            else:
                y_pred, score, model = self._lgbm_train_and_predict(
                    params, train_params, X_train, X_valid, y_train, y_valid, test)

            y_preds.append(y_pred)
            scores.append(score)
            models.append(model)

        self.feature_importance = self.get_feature_importance(models)
        return y_preds, scores, models


class RandSeedModel(Model):
    def train_and_predict(self, params, train_params, X, y, test, n_fold, is_shuffle, seed=None):
        y_preds = []
        scores = []
        models = []

        for i in range(n_fold):
            print(f'\n--- Start Train of {i+1} Fold ---')
            X_train, X_valid, y_train, y_valid = train_test_split(
                X, y, test_size=0.2, shuffle=is_shuffle, random_state=seed + i)

            # bootstrap sampling
            X_valid, y_valid = resample(X_valid, y_valid, n_samples=int(X_valid.shape[0] * 0.8))

            # X_train, y_train = random_under_sampling(
            #     X_train, y_train, drop_rate=0.2, seed=seed + i)

            if self.model_type == 'lgbm':
                y_pred, score, model = self._lgbm_train_and_predict(
                    params, train_params, X_train, X_valid, y_train, y_valid, test)
            else:
                y_pred, score, model = self._lgbm_train_and_predict(
                    params, train_params, X_train, X_valid, y_train, y_valid, test)

            y_preds.append(y_pred)
            scores.append(score)
            models.append(model)

        self.feature_importance = self.get_feature_importance(models)
        return y_preds, scores, models

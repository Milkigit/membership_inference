from typing import List, Tuple, Dict

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.base import clone


class ShadowModels:
    """
    Creates a swarm of shadow models and trains them with a split
    of the synthetic data.

    TODO:
        - Split the synth data in n_models parts
        - The splited data is splited again in train and test (1/2)
        - Instance n models (must be similar to the target model)
        - Train each model on training splited data
        - Run prediction on both training and test splited data
        - Label the resulting prediction vector with "in"/"out"
          if it was train or test
        - drop mic
    """

    def __init__(self, n_models: int, data: np.ndarray,
                 target_classes: int, learner):

        self.n_models = n_models
        self.data = data
        self.target_classes = target_classes
        self.splits = self._split_data(self.data, self.n_models)
        self.learner = learner
        self.models = self._get_models(self.learner, self.n_models)

    @staticmethod
    def _split_data(data, n_splits, shuffle=False) -> List[np.ndarray]:
        if shuffle:
            np.random.shuffle(data)  # shufle data just in case
        splited = np.vsplit(data, n_splits)
        return splited

    @staticmethod
    def _get_model_list(learner, n) -> List:
        """
        Intances n shadow models, copies of the input parameter learner
        """
        models = [clone(learner) for _ in range(n)]
        return models

    def fit(self):

        # TRAIN
        for model, data_subset in zip(self.models, self.splits):
            X = data_subset[:, :-1]
            y = data_subset[:, -1]
            X_train, X_test, y_train, y_test = train_test_split(X, y)
            model.fit(X_train, y_train)

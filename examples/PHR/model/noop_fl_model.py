import logging

from ibmfl.util import config
from ibmfl.util import fl_metrics
from ibmfl.model.fl_model import FLModel
from ibmfl.model.model_update import ModelUpdate
from ibmfl.exceptions import FLException, LocalTrainingException, ModelException

logger = logging.getLogger(__name__)


class NoopFLModel(FLModel):
    """
    An FLModel that does nothing.
    """

    def __init__(self, model_name,
                 model_spec,
                 keras_model=None,
                 **kwargs):
        super().__init__(model_name, model_spec, **kwargs)

    def fit_model(self, train_data, fit_params=None, **kwargs):
        return None

    def update_model(self, model_update):
        pass

    def get_model_update(self):
        return None

    def predict(self, x, batch_size=128, **kwargs):
        return None

    def evaluate(self, test_dataset, **kwargs):
        return None

    def save_model(self, filename=None):
        return filename

    def load_model(self, file_name, custom_objects={}):
        return None
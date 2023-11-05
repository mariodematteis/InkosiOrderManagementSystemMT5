from typing import Any

import torch

from inkosi.log.log import Logger
from inkosi.utils.settings import get_risk_management_models

logger = Logger(
    module_name="risk_management",
    package_name="portfolio",
)


class RiskManagementMetaclass(type):
    models_initialised: dict = {}

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if get_risk_management_models() is None:
            logger.warn("No Risk Management models have been implemented")
        else:
            for model in get_risk_management_models():
                model_initialisation = self.models_initialised.get(model, 0)
                if model_initialisation == 0:
                    self.initialise_model(model_path=model)

        return super().__call__(*args, **kwds)

    def initialise_model(
        self,
        model_path: str,
    ) -> bool:
        logger.info(f"Trying to load the following model: {model_path}")

        try:
            model = torch.jit.load(model_path)
            model.eval()
        except Exception as error:
            logger.error(
                f"Unable to load the model in the following path: {model_path}. Error"
                f" occurred: {error}"
            )
            return False
        else:
            self.models_initialised[model_path] = model
            return True


class RiskManagement(metaclass=RiskManagementMetaclass):
    def __init__(self) -> None:
        ...

    def compute_volume(
        self,
    ) -> float:
        return 0.1

    def adjust_take_profit(
        self,
    ) -> float:
        return 5.0

    def adjust_stop_loss(
        self,
    ) -> float:
        return 5.0

from typing import Any

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

        for model in get_risk_management_models():
            model_initialisation = self.models_initialised.get(model, 0)
            if model_initialisation == 0:
                self.initialise_model(model_path=model)

        return super().__call__(*args, **kwds)

    def initialise_model(
        self,
        model_path: str,
    ) -> bool:
        logger.info(f"Model correctly initialised: {model_path}")
        self.models_initialised[model_path] = 1
        ...


class RiskManagement(metaclass=RiskManagementMetaclass):
    def __init__(self) -> None:
        pass

    def trade(
        self,
    ) -> float:
        pass

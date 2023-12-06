from typing import Any

import torch

from inkosi.log.log import Logger
from inkosi.utils.settings import get_risk_management_models

logger = Logger(
    module_name="risk_management",
    package_name="portfolio",
)


class RiskManagementMetaclass(type):
    """
    Metaclass for the RiskManagement class responsible for managing trading risk.

    Attributes:
        models_initialised (dict): Dictionary to track initialized risk management
        models.

    Methods:
        __call__(self, *args: Any, **kwds: Any) -> Any:
            Override the call method to initialize risk management models if available.

        initialise_model(self, model_path: str) -> bool:
            Initialize a risk management model from the specified path.

    Note:
        This metaclass is responsible for dynamically initializing risk management
        models when an instance of the RiskManagement class is created. It utilizes a
        dictionary (`models_initialised`) to track the initialization status of each
        model.
    """

    models_initialised: dict = {}

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        """
        Override the call method to initialize risk management models if available.

        Parameters:
            *args (Any): Variable arguments.
            **kwds (Any): Keyword arguments.

        Returns:
            Any: Result of calling the superclass's call method.
        """

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
        """
        Initialize a risk management model from the specified path.

        Parameters:
            model_path (str): Path to the risk management model.

        Returns:
            bool: True if the model is successfully initialized, False otherwise.
        """

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
    """
    Risk management class responsible for managing trading risk.

    Attributes:
        None

    Methods:
        __init__(self) -> None:
            Constructor method for initializing the RiskManagement instance.

        compute_volume(self) -> float:
            Compute the trading volume based on risk management rules.

        adjust_take_profit(self) -> float:
            Adjust the take-profit value based on risk management rules.

        adjust_stop_loss(self) -> float:
            Adjust the stop-loss value based on risk management rules.

        unload_model(self) -> None:
            Unload the risk management model.

    Note:
        This class serves as an interface for implementing risk management strategies
        in a trading system. It includes methods for computing volume, adjusting
        take-profit and stop-loss values, and unloading the risk management model.
    """

    def __init__(self) -> None:
        """
        Constructor method for initializing the RiskManagement instance.

        Parameters:
            None

        Returns:
            None
        """

        ...

    def compute_volume(
        self,
    ) -> float:
        """
        Compute the trading volume based on risk management rules.

        Parameters:
            None

        Returns:
            float: The computed trading volume.
        """

        return 0.1

    def adjust_take_profit(
        self,
    ) -> float:
        """
        Adjust the take-profit value based on risk management rules.

        Parameters:
            None

        Returns:
            float: The adjusted take-profit value.
        """

        return 5.0

    def adjust_stop_loss(
        self,
    ) -> float:
        """
        Adjust the stop-loss value based on risk management rules.

        Parameters:
            None

        Returns:
            float: The adjusted stop-loss value.
        """

        return 5.0

    def unload_model(
        self,
    ) -> None:
        """
        Unload the risk management model.

        Parameters:
            None

        Returns:
            None
        """

        return

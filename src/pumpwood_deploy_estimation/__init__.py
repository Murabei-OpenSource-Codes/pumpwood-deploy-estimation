"""Kubernetes deployment package for the Pumpwood Estimation microservice.

Use ``PumpWoodEstimationMicroservice`` with ``DeployPumpWood`` from
``pumpwood-deploy`` to generate and apply estimation manifests.

Example:
    ```python
    from pumpwood_deploy_estimation import PumpWoodEstimationMicroservice

    estimation = PumpWoodEstimationMicroservice(
        app_version="1.0",
        worker_version="1.0",
    )
    deploy.add_microservice(estimation)
    ```

Cluster prerequisites include ``StandardMicroservices`` (storage
ConfigMap, general secrets, RabbitMQ), ``PumpWoodDatalakeMicroservice``
for datalake credentials, and ``PumpWoodAuthMicroservice`` for
authorization.
"""
from .deploy import PumpWoodEstimationMicroservice

__all__ = [
    PumpWoodEstimationMicroservice
]

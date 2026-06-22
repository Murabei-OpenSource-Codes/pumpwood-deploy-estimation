"""Kubernetes deployment manifests for the Pumpwood Estimation microservice.

This module builds Secret and Deployment YAML files for
``pumpwood-estimation-app``. Manifests are registered with
``DeployPumpWood.add_microservice`` from ``pumpwood-deploy``.

The application reads estimation database credentials from the
``pumpwood-estimation`` secret. Storage bucket and type come from the
cluster ``storage`` ConfigMap deployed by ``StandardMicroservices``.
"""
import base64
from importlib import resources
from pumpwood_deploy.abc import BasePumpwoodDeployMicroservice
from pumpwood_deploy.type import (
    PumpwoodDeploy, PumpwoodDeploySecret, PumpwoodDeployDeployment)


secrets = resources.files('pumpwood_deploy_estimation')\
    .joinpath('resources/secrets.yml')\
    .read_text(encoding='utf-8')
app_deployment = resources.files('pumpwood_deploy_estimation')\
    .joinpath('resources/deploy__app.yml')\
    .read_text(encoding='utf-8')


class PumpWoodEstimationMicroservice(BasePumpwoodDeployMicroservice):
    """Deploy Kubernetes manifests for the Pumpwood Estimation microservice.

    Estimation defines parameters for mathematical models and the
    attributes used as model inputs and outputs.

    The deploy class renders two manifests: estimation secrets and the
    application (``pumpwood-estimation-app``).

    Example:
        ```python
        import os
        from pumpwood_deploy.deploy import DeployPumpWood
        from pumpwood_deploy_estimation import PumpWoodEstimationMicroservice

        deploy.add_microservice(
            PumpWoodEstimationMicroservice(
                app_version=os.getenv("PUMPWOOD_ESTIMATION_APP"),
                db_host="pgbouncer-pumpwood-estimation",
                db_database="pumpwood_estimation",
                microservice_password=secrets["microservice--estimation"],
            ))
        ```
    """

    def __init__(self,
                 app_version: str,
                 microservice_password: str = "microservice--estimation",  # NOQA
                 db_username: str = "pumpwood",
                 db_password: str = "pumpwood",  # NOQA
                 db_host: str = "pgbouncer-pumpwood-estimation",
                 db_port: str = "5432",
                 db_database: str = "pumpwood",
                 repository: str = "gcr.io/repositorio-geral-170012",
                 app_debug: str = "FALSE",
                 app_replicas: int = 1,
                 app_timeout: int = 300,
                 app_workers: int = 10,
                 app_limits_memory: str = "60Gi",
                 app_limits_cpu: str = "12000m",
                 app_requests_memory: str = "20Mi",
                 app_requests_cpu: str = "1m"):
        """Initialize Pumpwood Estimation deployment configuration.

        Args:
            app_version (str):
                Container image tag for ``pumpwood-estimation-app``.
            microservice_password (str):
                Password for the ``microservice--estimation`` service
                user stored in the estimation secret. Defaults to
                ``microservice--estimation``.
            db_username (str):
                Postgres username for the application connection.
                Defaults to ``pumpwood``.
            db_password (str):
                Postgres password stored in the estimation secret.
                Defaults to ``pumpwood``.
            db_host (str):
                Postgres hostname for the application. Defaults to
                ``pgbouncer-pumpwood-estimation``.
            db_port (str):
                Postgres port for the application. Defaults to
                ``5432``.
            db_database (str):
                Postgres database name for the application. Defaults to
                ``pumpwood``.
            repository (str):
                Docker registry for the application image. Defaults to
                ``gcr.io/repositorio-geral-170012``.
            app_debug (str):
                Debug flag for the application. Accepts ``TRUE`` or
                ``FALSE``. Defaults to ``FALSE``.
            app_replicas (int):
                Number of app pod replicas. Defaults to ``1``.
            app_timeout (int):
                Request timeout in seconds for the app. Defaults to
                ``300``.
            app_workers (int):
                Number of Granian workers for the app. Defaults to
                ``10``.
            app_limits_memory (str):
                Memory limit for app pods. Defaults to ``60Gi``.
            app_limits_cpu (str):
                CPU limit for app pods. Defaults to ``12000m``.
            app_requests_memory (str):
                Memory request for app pods. Defaults to ``20Mi``.
            app_requests_cpu (str):
                CPU request for app pods. Defaults to ``1m``.
        """
        self.repository = repository.rstrip("/")
        self._microservice_password = base64.b64encode(
            microservice_password.encode()).decode()

        self._db_password = base64.b64encode(db_password.encode()).decode()
        self.db_username = db_username
        self.db_host = db_host
        self.db_port = db_port
        self.db_database = db_database

        self.app_version = app_version
        self.app_debug = app_debug
        self.app_replicas = app_replicas
        self.app_timeout = app_timeout
        self.app_workers = app_workers
        self.app_limits_memory = app_limits_memory
        self.app_limits_cpu = app_limits_cpu
        self.app_requests_memory = app_requests_memory
        self.app_requests_cpu = app_requests_cpu

    def create_deployment_file(self) -> list[PumpwoodDeploy]:
        """Build Kubernetes manifests for Pumpwood Estimation.

        Returns:
            list[PumpwoodDeploy]:
                Secret ``pumpwood_estimation__secrets`` and application
                deploy ``pumpwood_estimation__deploy``.
        """
        secrets_text_formated = secrets\
            .format(db_password=self._db_password,
                    microservice_password=self._microservice_password)

        app_deployment_formated = \
            app_deployment.format(
                repository=self.repository,
                version=self.app_version,
                replicas=self.app_replicas,
                debug=self.app_debug,
                n_workers=self.app_workers,
                workers_timeout=self.app_timeout,
                db_username=self.db_username,
                db_host=self.db_host,
                db_port=self.db_port,
                db_database=self.db_database,
                limits_memory=self.app_limits_memory,
                limits_cpu=self.app_limits_cpu,
                requests_memory=self.app_requests_memory,
                requests_cpu=self.app_requests_cpu)
        return [
            PumpwoodDeploySecret(
                name='pumpwood_estimation__secrets',
                content=secrets_text_formated),
            PumpwoodDeployDeployment(
                name='pumpwood_estimation__deploy',
                content=app_deployment_formated),
        ]

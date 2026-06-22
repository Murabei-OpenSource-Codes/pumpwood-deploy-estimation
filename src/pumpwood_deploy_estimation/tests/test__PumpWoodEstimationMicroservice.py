"""Tests for Pumpwood Estimation deployment manifests."""
import unittest
from pumpwood_deploy.type import (
    PumpwoodDeployDeployment, PumpwoodDeploySecret)
from pumpwood_deploy_estimation.deploy import (
    PumpWoodEstimationMicroservice)


class TestPumpWoodEstimationMicroservice(unittest.TestCase):
    """Validate generated estimation Kubernetes manifests."""

    def test__create_files(self):
        """Ensure generated manifests include secrets and app deploy."""
        deploy_obj = PumpWoodEstimationMicroservice(
            microservice_password="xxxx",
            app_version="xxxx")
        results = deploy_obj.create_deployment_file()
        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], PumpwoodDeploySecret)
        self.assertEqual(
            results[0].name, 'pumpwood_estimation__secrets')
        self.assertIsInstance(results[1], PumpwoodDeployDeployment)
        self.assertEqual(
            results[1].name, 'pumpwood_estimation__deploy')
        for item in results:
            self.assertTrue(hasattr(item, 'content'))
            self.assertTrue(len(item.content) > 0)
            self.assertIn('apiVersion', item.content)
            self.assertIn('pumpwood-estimation', item.content)

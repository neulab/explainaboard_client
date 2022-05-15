from explainaboard_client.tests.test_utils import TestEndpointsE2E


class TestInfo(TestEndpointsE2E):
    def test_can_get_info(self):
        info = self._client.info_get()
        self.assertIn("api_version", info)
        self.assertIn("env", info)

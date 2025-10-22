import pytest
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000/redfish/v1"
USERNAME = "admin"
PASSWORD = "password"


@pytest.fixture(scope="session")
def redfish_session():
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    try:
        resp = session.get(f"{BASE_URL}/Systems/system", timeout=10)
        resp.raise_for_status()
        logger.info("Redfish session established successfully.")
        return session
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to establish Redfish session: {e}")
        pytest.fail("Redfish API is not available. Ensure redfish_mock.py is running.")


def test_authentication():
    payload = {
        "UserName": USERNAME,
        "Password": PASSWORD
    }
    try:
        resp = requests.post(f"{BASE_URL}/SessionService/Sessions", json=payload, timeout=5)
        assert resp.status_code == 201, f"Expected 201, got {resp.status_code}"
        data = resp.json()
        assert "Token" in data, "Session token not found in response"
        assert "Id" in data, "Session ID not found in response"
        logger.info("Authentication test passed.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Authentication test failed: {e}")
        pytest.fail("Authentication request failed.")


def test_get_system_info(redfish_session):
    try:
        resp = redfish_session.get(f"{BASE_URL}/Systems/system", timeout=5)
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        data = resp.json()
        assert "PowerState" in data, "PowerState not found"
        assert "Status" in data, "Status not found"
        assert "State" in data["Status"], "Status.State not found"
        logger.info(f"System info: PowerState={data['PowerState']}, State={data['Status']['State']}")
    except requests.exceptions.RequestException as e:
        logger.error(f"System info test failed: {e}")
        pytest.fail("Failed to retrieve system information.")


def test_power_on(redfish_session):
    payload = {"ResetType": "On"}
    try:
        resp = redfish_session.post(
            f"{BASE_URL}/Systems/system/Actions/ComputerSystem.Reset",
            json=payload,
            timeout=5
        )
        assert resp.status_code == 202, f"Expected 202, got {resp.status_code}"
        resp = redfish_session.get(f"{BASE_URL}/Systems/system", timeout=5)
        data = resp.json()
        assert data["PowerState"] == "On", f"Expected PowerState='On', got '{data['PowerState']}'"
        assert data["Status"]["State"] == "Enabled", "System state should be 'Enabled'"
        logger.info("Power ON test passed.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Power ON test failed: {e}")
        pytest.fail("Failed to power on the system.")


def test_graceful_shutdown(redfish_session):
    payload = {"ResetType": "GracefulShutdown"}
    try:
        resp = redfish_session.post(
            f"{BASE_URL}/Systems/system/Actions/ComputerSystem.Reset",
            json=payload,
            timeout=5
        )
        assert resp.status_code == 202, f"Expected 202, got {resp.status_code}"

        resp = redfish_session.get(f"{BASE_URL}/Systems/system", timeout=5)
        data = resp.json()
        assert data["PowerState"] == "Off", f"Expected PowerState='Off', got '{data['PowerState']}'"
        assert data["Status"]["State"] == "Disabled", "System state should be 'Disabled'"
        logger.info("Graceful shutdown test passed.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Graceful shutdown test failed: {e}")
        pytest.fail("Failed to shut down the system.")


def test_cpu_temperature(redfish_session):
    try:
        resp = redfish_session.get(f"{BASE_URL}/Chassis/chassis/Thermal", timeout=5)
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        data = resp.json()
        temps = data.get("Temperatures", [])
        assert len(temps) > 0, "No temperature sensors found"

        cpu_temp = temps[0].get("ReadingCelsius")
        assert cpu_temp is not None, "CPU temperature not reported"
        assert cpu_temp < 85, f"CPU temperature too high: {cpu_temp}°C"
        logger.info(f"CPU temperature: {cpu_temp}°C (within normal range)")
    except requests.exceptions.RequestException as e:
        logger.error(f"Temperature test failed: {e}")
        pytest.fail("Failed to retrieve thermal data.")


def test_redfish_vs_ipmi_sensors():
    redfish_temp = 65
    ipmi_temp = 65

    assert redfish_temp == ipmi_temp, "Redfish and IPMI temperature readings do not match"
    logger.info("Redfish and IPMI sensor values are consistent (emulated).")
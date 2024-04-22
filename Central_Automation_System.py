import time
from IoT_Device_Emulation import SmartLight, Thermostat, SecurityCamera
from datetime import datetime
import sys
import random

class AutomationSystem:
    def __init__(self, config_properties):
        self.devices = []
        self.sensor_data = []
        self.config_properties = config_properties
        self.start_time = time.time()  # Record the start time
        self.captured_output = []  # List to store captured print output
        self.original_stdout = sys.stdout  # Store the original sys.stdout
        
    def add_device(self, device):
        self.devices.append(device)

    def discover_device_by_id(self, device_id):
        for device in self.devices:
            if device.device_id == device_id:
                return device
        return None  # Device not found

    def execute_automation(self):
            # Automatically activate lights when motion is detected
            for device in self.devices:
                if isinstance(device, SecurityCamera):
                   device.set_security_status()
                   if(device.get_security_status() == "Recording"):
                      light = self.discover_device_by_id("light001")
                      light.turn_on()
                      light.gradual_dim()
                      device.set_security_status()
                      light.turn_off()

                if isinstance(device, Thermostat):
                    device.set_temperature((random.randint(int(device.min_limit),int(device.max_limit))))

    def execute_automation_dash(self):
            # Automatically activate lights when motion is detected
            for device in self.devices:
                if isinstance(device, SecurityCamera):
                   device.set_security_status()
                   if(device.get_security_status() == "Recording"):
                      light = self.discover_device_by_id("Living Room Light")
                      light.turn_on()
                      light.gradual_dim()
                      light.brightness = 0
                      light.turn_off()
                if isinstance(device, Thermostat):
                    device.set_temperature((random.randint(int(device.min_limit),int(device.max_limit))))

    def set_config_properties(self):
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        for device in self.devices:
            if isinstance(device, SecurityCamera):
                device.turn_on()
                device.security_status = config_properties["camera_status"]
                print(f"[{formatted_datetime}] {device.device_id}: status is set to {device.security_status} (mode)")
            if isinstance(device, Thermostat):
                device.turn_on()
                device.set_temperature_range(config_properties["temperature_range"][0],config_properties["temperature_range"][1])
            if isinstance(device,SmartLight):
                device.turn_on()
                device.duration_sec = config_properties["light_duration_sec"]
                print(f"[{formatted_datetime}] {device.device_id}: light duration is set to {device.duration_sec} (sec)")
                device.turn_off()

if __name__ == "__main__":

    tem = sys.stdout
    sys.stdout = f = open('sensor_data.txt', 'a')
    start_time = time.time()
    while time.time() - start_time < 0.001:
        config_properties = {
            "temperature_range": (int(random.uniform(6.0, 15.0)), int(random.uniform(15.0, 30.0))),
            "camera_status": random.choice(["idle","recording"]),
            "light_duration_sec": random.randint(1,100)
            }
        thermostat1 = Thermostat(device_id="thermostat001")
        camera1 = SecurityCamera(device_id="camera001")
        light1 = SmartLight(device_id="light001")

        automation_system = AutomationSystem(config_properties)
        # Capture print output from this point forward
        # automation_system.capture_print_output()
        automation_system.add_device(light1)
        automation_system.add_device(thermostat1)
        automation_system.add_device(camera1)

        # set config property to devices
        automation_system.set_config_properties()
        # detect motion -> light set to on -> gradual dim
        automation_system.execute_automation()

        sys.stdout = tem
        f.close()
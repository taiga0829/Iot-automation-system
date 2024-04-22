from datetime import datetime
class Device:
    def __init__(self, device_id, device_type):
        self.device_id = device_id
        self.device_type = device_type
        self.status = False  # Initially turned off

    def get_status(self):
        return self.status

    def turn_on(self):
        self.status = True
        # Get the current date and time
        current_datetime = datetime.now()

        # Format the date and time as a string
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{formatted_datetime}] {self.device_id}: turned on")

    def turn_off(self):
        self.status = False
        # Get the current date and time
        current_datetime = datetime.now()

        # Format the date and time as a string
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{formatted_datetime}] {self.device_id}: turned off")

class SmartLight(Device):
    def __init__(self, device_id):
        super().__init__(device_id, device_type="SmartLight")
        self.brightness = 0  # Brightness level (0-100)
        self.duration_sec = 5

    def set_brightness(self, brightness):
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        if self.status:
            prev= self.brightness
            self.brightness = max(0, min(brightness, 100))
            print(f"[{formatted_datetime}] {self.device_id}: brightness is set to {brightness}% from {prev}%")
        else:
                    # Get the current date and time
            print(f"[{formatted_datetime}] {self.device_id}: Cannot set brightness when the light is off.")

    def gradual_dim(self):
        if self.status:
            initial_brightness = self.brightness
            target_brightness = 100  # Always target maximum brightness
            step = (target_brightness - initial_brightness) / self.duration_sec
            for _ in range(self.duration_sec):
                self.brightness += step
                                # Get the current date and time
                current_datetime = datetime.now()

                # Format the date and time as a string
                formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{formatted_datetime}] {self.device_id}: Current brightness: {self.brightness:.2f}")
        else:
                    # Get the current date and time
            current_datetime = datetime.now()

            # Format the date and time as a string
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{formatted_datetime}] {self.device_id}: Cannot dim when the light is off.")

class Thermostat(Device):
    def __init__(self, device_id):
        super().__init__(device_id, device_type="Thermostat")
        self.temperature = 15.0  # Default temperature in Celsius
        self.max_limit = 40.0
        self.min_limit = 10.0

    def set_temperature(self, temperature):
        current_datetime = datetime.now()
        # Format the date and time as a string
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        if self.status:
            if self.max_limit > temperature and self.min_limit < temperature:
                curr_temp = self.get_temperature()
                self.temperature = temperature
                print(f"[{formatted_datetime}] {self.device_id}: temperature is set to {self.get_temperature()} from {curr_temp}")
            else:
                print(f"[{formatted_datetime}] {self.device_id}: temperature is beyond limits")
        else:
            print(f"[{formatted_datetime}] {self.device_id} :Cannot set temperature when the thermostat is off.")

    def set_temperature_range(self, min_temperature, max_temperature):
        if self.status:
            self.min_limit = min_temperature
            self.max_limit = max_temperature
            current_datetime = datetime.now()

            # Format the date and time as a string
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{formatted_datetime}] {self.device_id}: range is set from {self.min_limit}°C to {self.max_limit}°C")
        else:
            current_datetime = datetime.now()

            # Format the date and time as a string
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{formatted_datetime}] {self.device_id}:Cannot set temperature range when the thermostat is off.")

    def modify_properties(self, config_properties):
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        self.set_temperature_range(config_properties["temperature_range"][0], config_properties["temperature_range"][1])
        print(f"[{formatted_datetime}] {self.device_id} temperature range set from {config_properties['temperature_range'][0]}℃ to {config_properties['temperature_range'][1]}℃")

    def get_temperature(self):
        return self.temperature
                
class SecurityCamera(Device):
    def __init__(self, device_id):
        super().__init__(device_id, device_type="SecurityCamera")
        self.security_status = "Recording"  # Security status (e.g., Idle, Recording)

    def set_security_status(self):
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        if self.status:
                if self.security_status == "Recording":
                
                    print(f"[{formatted_datetime}] {self.device_id}: not detect motion")
                    self.security_status ="Idle"
                else:
                   
                    print(f"[{formatted_datetime}] {self.device_id}: detect motion")
                    self.security_status = "Recording"
        else:
            print(f"[{formatted_datetime}] {self.device_id}: Cannot set security status when the camera is off.")

    def get_security_status(self):
        return self.security_status
    
if __name__ == "__main__":

    print("\n")
    light = SmartLight(device_id="light001")
    light.turn_on()
    light.set_brightness(0)
    light.gradual_dim(5)
    light.turn_off()
    print("\n")
    thermostat = Thermostat(device_id="thermostat001")
    thermostat.turn_on()
    thermostat.set_temperature_range(28.0,90.0)
    thermostat.set_temperature(100.0)
    thermostat.set_temperature(80.0)
    thermostat.turn_off()
    print("\n")
    camera = SecurityCamera(device_id="camera001")
    camera.turn_on()
    camera.set_security_status()



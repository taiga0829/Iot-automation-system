import tkinter as tk
import random
from IoT_Device_Emulation import SmartLight, Thermostat, SecurityCamera
from Central_Automation_System import AutomationSystem
import sys
from datetime import datetime
class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.insert("end", text)
        self.text_widget.see("end")


class SmartHomeGUI:
    def __init__(self,root,automationSystem):
        self.root = root 
        self.root.title("Smart Home IoT Simulator")
        #TODO: add automation system to make it possible to search light to make it activated in camera is on
        self.automationSystem = automationSystem
        self.automation_status = True  # Initial automation status
        self.brightness_value = tk.DoubleVar(value=50.0)  # Default brightness value
        self.console_text = tk.Text(root, wrap=tk.WORD)
        sys.stdout = ConsoleRedirector(self.console_text)
        # Create labels to display device status
        self.automation_status_label = tk.Label(root, text="Automation Status: ON")
        # Create a single button for automation on/off
        self.toggle_automation_button = tk.Button(root, text="Automation ON", command=self.toggle_automation)
        # Create a text box to display device status
        self.device_status_box = tk.Text(root, height=10, width=60)  # Wider text box
        self.device_status_box.insert(tk.END, "Device Status:\n")
        # Create a brightness control slider
        self.brightness_slider = tk.Scale(root, from_=0, to=100, variable=self.brightness_value, orient="horizontal")
        self.brightness_label = tk.Label(root, text="Living Room Light Brightness")
        # Create a label to display the current brightness value
        self.current_brightness_label = tk.Label(root, text=f"")

        self.brightness_slider.config(command=self.update_light_brightness)  # Configure slider command

        # Create a toggle button for Living Room Light
        self.light_toggle_button = tk.Button(root, text="ON", command=self.toggle_light)

        # Create a label to display Thermostat information
        self.thermostat_info_label = tk.Label(root)

        # Create a button to toggle the Thermostat
        self.toggle_thermostat_button = tk.Button(root, text="ON", command=self.toggle_thermostat)

        # Create a label to display SecurityCamera information
        self.security_camera_info_label = tk.Label(root, text="Front Door Camera Motion Detection")

        # Create buttons for motion detection
        self.security_camera_motion_button = tk.Button(root, text="Random Detection Motion", command=self.toggle_security_camera_motion)

        # Create a label to display SecurityCamera information
        self.security_camera_info_label = tk.Label(root, text="Front Door Camera Motion Detection")

        # Create a label to display the motion detection status
        self.security_camera_status_label = tk.Label(root, text="Front Door Camera - Motion: Loading")

        # Create buttons for motion detection
        self.security_camera_motion_button = tk.Button(root, text="Random Detection Motion", command=self.toggle_security_camera_motion)

        # Create a label for the automation rule
        self.automation_rule_label = tk.Label(root, text="Automation Rule: Turn on lights when motion is detected\nBrightness Events")

        # Create a text box with a width of 100%
        self.text_box = tk.Text(root, height=10, width=60)  # Wider text box
        self.text_box.insert(tk.END, "")

                # Create a temperature control slider
        self.temperature_slider = tk.Scale(root, from_=15.0, to=30.0, resolution=0.1, orient="horizontal")
        self.temperature_label = tk.Label(root, text="Living Room Thermostat Temperature")

        self.temperature_slider.config(command=self.update_thermostat_temperature)

        # Organize widgets using grid layout
        self.automation_status_label.grid(row=0, column=0)
        self.toggle_automation_button.grid(row=1, column=0)
        self.device_status_box.grid(row=2, column=0)
        self.brightness_label.grid(row=3, column=0)
        self.brightness_slider.grid(row=4, column=0)
        self.light_toggle_button.grid(row=5, column=0)
        self.current_brightness_label.grid(row=6, column=0)
        # Add the temperature slider to the grid layout
        self.temperature_label.grid(row=7, column=0)
        self.temperature_slider.grid(row=8, column=0)
        self.thermostat_info_label.grid(row=9,column=0)
        self.brightness_slider.config(command=self.update_light_brightness)
        self.thermostat_info_label.grid(row=10, column=0)
        # add slider about temprature like light 
        self.toggle_thermostat_button.grid(row=11, column=0)
        self.security_camera_info_label.grid(row=12, column=0)
        self.security_camera_toggle_button = tk.Button(root, text="ON", command=self.toggle_security_camera)
        self.security_camera_toggle_button.grid(row=13, column=0)  # Adjust the row number as needed
        self.security_camera_motion_button.grid(row=14, column=0)
        self.security_camera_status_label.grid(row=15, column=0)
        self.automation_rule_label.grid(row=16, column=0)
        self.console_text.grid(row=17, columnspan=1)
        self.console_text.config(wrap=tk.WORD)

        # Start the automation loop
        self.update_data()
        self.update_device_status()  # Update device status initially
        self.update_automation()
        self.update_thermostat_temperature(None)

    def update_data(self):
        # Simulate data updates
        temperature = random.uniform(18.0, 28.0)
        motion_detection = random.choice(["Yes", "No"])
        brightness = self.brightness_value.get()  # Get brightness from the slider

        # Update the current brightness label for the Living Room Light
        for device in self.automationSystem.devices:
            if isinstance(device, SmartLight):
                self.current_brightness_label.config(text=f"{device.device_id} - {brightness}%")
            if isinstance(device,Thermostat):
                self.thermostat_info_label.config(text=f"{device.device_id} Temperature - {device.get_temperature()}°C")

        # Schedule the next data update after 5 seconds
        self.root.after(5000, self.update_data)

    def toggle_automation(self):
        # Toggle the automation status
        self.automation_status = not self.automation_status
        status_text = "ON" if self.automation_status else "OFF"
        self.automation_status_label.config(text=f"Automation Status: {status_text}")
        self.toggle_automation_button.config(text="OFF" if self.automation_status else "ON")
        if self.automation_status:
                self.automationSystem.execute_automation_dash()
        self.update_automation() 

    def update_automation(self):
        if self.automation_status:
            self.automationSystem.execute_automation_dash()
            self.root.after(5000, self.update_automation)

    def update_device_status(self):
        # Update the device status in the text box
        device_status_text = ""
        for device in self.automationSystem.devices:
            device_status_text += f"{device.device_id}: {device.device_type} Status: {'On' if device.get_status() else 'Off'}\n"
        self.device_status_box.delete(1.0, tk.END)  # Clear the text box
        self.device_status_box.insert(tk.END, device_status_text)
        # Schedule the next update after 5 seconds
        self.root.after(5000, self.update_device_status)

    def update_light_brightness(self, event):
        # This function will be called when the slider's value changes
        brightness = self.brightness_slider.get()
        for device in self.automationSystem.devices:
            if isinstance(device, SmartLight):
                device.set_brightness(brightness)

    def toggle_light(self):
        # Toggle the status of the Living Room Light
        for device in self.automationSystem.devices:
            if isinstance(device, SmartLight):
                current_status = device.get_status()
                if current_status:
                    device.turn_off()
                else:
                    device.turn_on()
                self.update_device_status()
                # Update the button text for the Living Room Light
                self.light_toggle_button.config(text="ON" if current_status else "OFF")

    def toggle_thermostat(self):
        # Toggle the status of the Thermostat
        for device in self.automationSystem.devices:
            if isinstance(device, Thermostat):
                current_status = device.get_status()
                if current_status:
                    device.turn_off()
                else:
                    device.turn_on()
                self.update_device_status()

                # Display Thermostat information after toggling
                thermostat_info = f"{device.device_id} Temperature - {device.get_temperature()}°C"
                self.thermostat_info_label.config(text=thermostat_info)
                self.toggle_thermostat_button.config(text="ON" if current_status else "OFF")

    def update_thermostat_temperature(self, event):
        temperature = self.temperature_slider.get()
        for device in self.automationSystem.devices:
            if isinstance(device, Thermostat):
                device.set_temperature(temperature)
                # Update the thermostat information label
                thermostat_info = f"{device.device_id} Temperature - {device.get_temperature()}°C"
                self.thermostat_info_label.config(text=thermostat_info)
                current_datetime = datetime.now()
                # Format the date and time as a string
                formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{formatted_datetime}] {device.device_id}: {device.get_temperature()}°C")
    

    def toggle_security_camera(self):
        # Toggle the status of the SecurityCamera
        for device in self.automationSystem.devices:
            if isinstance(device, SecurityCamera):
                current_status = device.get_status()
                if current_status:
                    device.turn_off()
                else:
                    device.turn_on()
                self.update_device_status()

                # Update the button text for the SecurityCamera
                self.security_camera_toggle_button.config(text="ON" if current_status else "OFF")

    def toggle_security_camera_motion(self):
            current_datetime = datetime.now()

                # Format the date and time as a string
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            for device in self.automationSystem.devices:
                if isinstance(device, SecurityCamera):
                    device.set_security_status()
                    # Update the button text for motion detection
                    if device.get_security_status() == "Recording":
                        self.security_camera_motion_button.config(text="Random Undetection Motion")
                    else:
                        self.security_camera_motion_button.config(text="Random Detection Motion")
                    print(f"[{formatted_datetime}] {device.device_id}: {device.get_security_status()}")
                    # Update the motion detection status label
                    status_text = "YES" if device.get_security_status() == "Recording" else "NO"
                    self.security_camera_status_label.config(text=f"Front Door Camera - Motion: {status_text}")

    def update_log(self, message):
        self.text_box.insert(tk.END, message + "\n")
        self.text_box.see(tk.END)  # Scroll to the end to show the latest log message

if __name__ == "__main__":
    tem = sys.stdout
    sys.stdout = f = open('sensor_data.txt', 'a')
    root = tk.Tk()
    

    devices = [
        SmartLight(device_id="Living Room Light"),
        Thermostat(device_id="Living Room Thermostat"),
        SecurityCamera(device_id="Front Door Camera"),
    ]
    config_properties = {
        "temperature_range": (15.0, 30.0),
        "light_range": (0, 100),
        "camera_status": "idle"
    }
    automation_system = AutomationSystem(config_properties)
    app = SmartHomeGUI(root, automation_system)
    root.geometry("400x800")  # Adjust the window size

    light1 = devices[0] 
    thermostat1 = devices[1]  
    camera1 = devices[2] 

    app.automationSystem.add_device(light1)
    app.automationSystem.add_device(thermostat1)
    app.automationSystem.add_device(camera1)

    app.toggle_automation()
    app.update_automation()
    root.mainloop()
    sys.stdout = tem
    f.close()





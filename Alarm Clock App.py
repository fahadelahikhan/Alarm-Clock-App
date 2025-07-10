import tkinter as tk
from tkinter import messagebox
import time
import threading
import winsound


class AlarmClock:
    def __init__(self):
        # Create main window
        self.window = tk.Tk()
        self.window.title("Simple Alarm Clock")
        self.window.geometry("300x200")

        # Variables to track alarm state
        self.alarm_set = False
        self.alarm_time = ""
        self.check_thread = None

        # Initialize GUI elements (will be created in create_widgets)
        self.current_time_label = None
        self.time_entry = None
        self.set_button = None
        self.status_label = None

        # Create GUI elements
        self.create_widgets()

        # Start the clock display update
        self.update_clock()

    def create_widgets(self):
        # Current time display
        self.current_time_label = tk.Label(
            self.window,
            text="Current Time: ",
            font=("Arial", 12)
        )
        self.current_time_label.pack(pady=10)

        # Instructions
        instruction_label = tk.Label(
            self.window,
            text="Set your alarm time (24-hour format):"
        )
        instruction_label.pack(pady=5)

        # Time entry field
        self.time_entry = tk.Entry(self.window, font=("Arial", 12))
        self.time_entry.pack(pady=5)
        self.time_entry.insert(0, "07:30")  # Default example

        # Set alarm button
        self.set_button = tk.Button(
            self.window,
            text="Set Alarm",
            command=self.handle_alarm_button,
            font=("Arial", 10),
            bg="lightgreen"
        )
        self.set_button.pack(pady=10)

        # Status label
        self.status_label = tk.Label(
            self.window,
            text="No alarm set",
            font=("Arial", 10),
            fg="gray"
        )
        self.status_label.pack(pady=5)

    def update_clock(self):
        # Update the current time display every second
        current_time = time.strftime("%H:%M:%S")
        self.current_time_label.config(text=f"Current Time: {current_time}")

        # Schedule the next update (after 1000ms = 1 second)
        self.window.after(1000, self.update_clock)

    def handle_alarm_button(self):
        if not self.alarm_set:
            self.activate_alarm()
        else:
            self.cancel_alarm()

    def activate_alarm(self):
        alarm_time_input = self.time_entry.get().strip()

        # Validate the time format
        if not self.is_valid_time(alarm_time_input):
            messagebox.showerror(
                "Invalid Time",
                "Please enter time in HH:MM format (e.g., 07:30)"
            )
            return

        # Set the alarm
        self.alarm_time = alarm_time_input
        self.alarm_set = True

        # Update GUI
        self.set_button.config(text="Cancel Alarm", bg="lightcoral")
        self.status_label.config(text=f"Alarm set for {self.alarm_time}", fg="green")

        # Start checking for alarm time in a separate thread
        self.check_thread = threading.Thread(target=self.check_alarm_time)
        self.check_thread.daemon = True  # Thread will close when main program closes
        self.check_thread.start()

    def cancel_alarm(self):
        self.alarm_set = False
        self.alarm_time = ""

        # Update GUI
        self.set_button.config(text="Set Alarm", bg="lightgreen")
        self.status_label.config(text="No alarm set", fg="gray")

    @staticmethod
    def is_valid_time(time_str):
        """Check if the time string is in valid HH:MM format."""
        try:
            time.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False

    def check_alarm_time(self):
        while self.alarm_set:
            current_time = time.strftime("%H:%M")

            if current_time == self.alarm_time:
                self.trigger_alarm()
                break

            # Check every second
            time.sleep(1)

    def trigger_alarm(self):
        # Show alarm message
        messagebox.showinfo("⏰ ALARM!", f"Wake up! It's {self.alarm_time}")

        # Play alarm sound
        try:
            # Play beep sound 3 times
            for _ in range(3):
                winsound.Beep(1000, 500)  # 1000Hz for 0.5 seconds
                time.sleep(0.2)
        except OSError:
            # If winsound doesn't work (e.g., on non-Windows systems)
            print("Alarm sound not available on this system")

        # Reset alarm after it goes off
        self.cancel_alarm()

    def run(self):
        self.window.mainloop()


# Create and run the alarm clock
if __name__ == "__main__":
    alarm_clock = AlarmClock()
    alarm_clock.run()
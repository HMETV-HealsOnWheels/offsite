import socket
import tkinter as tk
from tkinter import Toplevel, Label, font, messagebox, ttk
import threading
import time
from datetime import datetime
import os

# Robot connection settings
TCP_IP = '192.168.1.55'  # Pi's IP
TCP_PORT = 5001

# Paths for each destination (pre-programmed sequences)
DESTINATIONS = {
    "ICU 1": [
        "forward,2000",
        "left,5000",
        "forward,10000",
        "done,0"
    ],
    "ICU 2": [
        "forward,15000",
        "right,5000",
        "forward,10000",
        "done,0"
    ],
    "Room 1": [
        "forward,8000",
        "left,5000",
        "forward,12000",
        "done,0"
    ],
    "Room 2": [
        "forward,8000",
        "right,5000",
        "forward,12000",
        "done,0"
    ]
}

class ModernHospitalRobotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Heals on Wheels - HMETV Control System")
        self.root.geometry("900x700")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(True, True)
        
        # Set custom theme and styling
        self.set_styles()
        
        # Create main container frame
        self.main_frame = ttk.Frame(root, style="Light.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Create top banner
        self.create_top_banner()
        
        # Create content area with destination selection
        self.create_content_area()
        
        # Create status bar
        self.create_status_bar()
        
        # Initialize connection status
        self.robot_connected = False
        self.check_connection()
        
        # Start periodic connection check
        self.connection_thread = threading.Thread(target=self.periodic_connection_check)
        self.connection_thread.daemon = True
        self.connection_thread.start()
        
        # Create pulse animation for status
        self.pulse_animation()
        
    def set_styles(self):
        """Set up custom styles for the application"""
        # Configure fonts
        self.title_font = ("Segoe UI", 22, "bold")
        self.header_font = ("Segoe UI", 16, "bold")
        self.subheader_font = ("Segoe UI", 14)
        self.body_font = ("Segoe UI", 12)
        self.mono_font = ("Consolas", 10)
        
        # Configure ttk styles
        style = ttk.Style()
        style.configure("TFrame", background="#FFFFFF")
        style.configure("Light.TFrame", background="#F8F9FA")
        style.configure("Banner.TFrame", background="#2C3E50")
        style.configure("TLabel", background="#FFFFFF", font=self.body_font)
        style.configure("Header.TLabel", font=self.header_font)
        style.configure("Title.TLabel", font=self.title_font, foreground="#FFFFFF", background="#2C3E50")
        style.configure("Status.TLabel", font=self.subheader_font)
        style.configure("TButton", font=self.body_font)
        
        # Configure custom ttk button styles
        style.configure("Destination.TButton", font=("Segoe UI", 14, "bold"), padding=10)
        style.configure("Emergency.TButton", 
                        font=("Segoe UI", 15, "bold"), 
                        background="#FF4136", 
                        foreground="#FFFFFF",
                        padding=10)
        style.map("Emergency.TButton",
                 background=[("active", "#D32F2F"), ("pressed", "#B71C1C")])
    
    def create_top_banner(self):
        """Create the top banner with logo and title"""
        banner_frame = ttk.Frame(self.main_frame, style="Banner.TFrame")
        banner_frame.pack(fill=tk.X, pady=0)
        
        # Create a container for the logo and title
        header_container = ttk.Frame(banner_frame, style="Banner.TFrame")
        header_container.pack(fill=tk.X, pady=15, padx=20)
        
        # Create title
        title_label = ttk.Label(
            header_container, 
            text="Heals on Wheels",
            style="Title.TLabel"
        )
        title_label.pack(side=tk.LEFT)
        
        # Create subtitle
        subtitle_label = ttk.Label(
            header_container, 
            text="Hospital Medical Equipment Transport Vehicle",
            font=("Segoe UI", 14),
            foreground="#ECF0F1",
            background="#2C3E50"
        )
        subtitle_label.pack(side=tk.LEFT, padx=15)
        
        # Add a decorative line
        separator = ttk.Separator(self.main_frame, orient="horizontal")
        separator.pack(fill=tk.X, pady=0)
    
    def create_content_area(self):
        """Create the main content area with destination selection"""
        # Create container for main content
        content_frame = ttk.Frame(self.main_frame, style="Light.TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create left panel for destinations
        left_panel = ttk.Frame(content_frame, style="Light.TFrame")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Add section header
        destination_header = ttk.Label(
            left_panel,
            text="Select Destination",
            style="Header.TLabel",
            background="#F8F9FA"
        )
        destination_header.pack(anchor=tk.W, pady=(0, 20))
        
        # Create destination button container
        self.dest_frame = ttk.Frame(left_panel, style="Light.TFrame")
        self.dest_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create styled destination buttons
        destinations = ["ICU 1", "ICU 2", "Room 1", "Room 2"]
        self.destination_buttons = []
        
        # Create card-like frame for each destination
        for i, dest in enumerate(destinations):
            row, col = divmod(i, 2)
            
            # Create a card frame for the button
            card_frame = ttk.Frame(self.dest_frame, style="TFrame")
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Add icon or destination name
            icon_text = dest[0]  # First letter as icon
            icon_label = tk.Label(
                card_frame,
                text=icon_text,
                font=("Segoe UI", 24, "bold"),
                fg="#3498DB",
                bg="#ECF0F1",
                width=2,
                height=1
            )
            icon_label.pack(pady=(10, 5))
            
            # Add destination name
            dest_label = tk.Label(
                card_frame,
                text=dest,
                font=("Segoe UI", 13, "bold"),
                bg="#FFFFFF"
            )
            dest_label.pack(pady=5)
            
            # Add button
            btn = tk.Button(
                card_frame,
                text="Send Robot",
                font=("Segoe UI", 11),
                bg="#3498DB",
                fg="#FFFFFF",
                activebackground="#2980B9",
                relief=tk.FLAT,
                bd=0,
                padx=10,
                pady=5,
                cursor="hand2",
                command=lambda d=dest: self.send_to_destination(d)
            )
            btn.pack(pady=(5, 15))
            self.destination_buttons.append(btn)
        
        # Configure grid weights
        self.dest_frame.columnconfigure(0, weight=1)
        self.dest_frame.columnconfigure(1, weight=1)
        self.dest_frame.rowconfigure(0, weight=1)
        self.dest_frame.rowconfigure(1, weight=1)
        
        # Create emergency stop container
        emergency_container = ttk.Frame(left_panel, style="Light.TFrame")
        emergency_container.pack(fill=tk.X, pady=20)
        
        # Create emergency stop button with modern styling
        self.e_stop_btn = tk.Button(
            emergency_container,
            text="EMERGENCY STOP",
            font=("Segoe UI", 14, "bold"),
            bg="#FF3B30",
            fg="#FFFFFF",
            activebackground="#D32F2F",
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.emergency_stop
        )
        self.e_stop_btn.pack(fill=tk.X)
        
        # Create right panel for log display
        right_panel = ttk.Frame(content_frame, style="Light.TFrame")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
        # Add section header
        log_header = ttk.Label(
            right_panel,
            text="Operation Log",
            style="Header.TLabel",
            background="#F8F9FA"
        )
        log_header.pack(anchor=tk.W, pady=(0, 10))
        
        # Create log frame with border and styling
        log_container = ttk.Frame(right_panel, style="TFrame")
        log_container.pack(fill=tk.BOTH, expand=True)
        
        # Add log display with styling
        self.log_text = tk.Text(
            log_container,
            font=self.mono_font,
            bg="#FAFAFA",
            fg="#333333",
            bd=1,
            relief=tk.SOLID,
            padx=10,
            pady=10,
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar to log
        log_scrollbar = ttk.Scrollbar(self.log_text, orient="vertical", command=self.log_text.yview)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        # Status display
        self.status_container = ttk.Frame(right_panel, style="Light.TFrame")
        self.status_container.pack(fill=tk.X, pady=(10, 0))
        
        # Status indicator
        status_frame = ttk.Frame(self.status_container, style="Light.TFrame")
        status_frame.pack(fill=tk.X)
        
        # Status circle
        self.status_canvas = tk.Canvas(status_frame, width=15, height=15, bg="#F8F9FA", highlightthickness=0)
        self.status_canvas.pack(side=tk.LEFT)
        self.status_indicator = self.status_canvas.create_oval(2, 2, 13, 13, fill="#CCCCCC", outline="")
        
        # Status text
        self.status_label = tk.Label(
            status_frame,
            text="Status: Initializing...",
            font=self.body_font,
            bg="#F8F9FA",
            fg="#555555"
        )
        self.status_label.pack(side=tk.LEFT, padx=10)

    def create_status_bar(self):
        """Create a status bar at the bottom"""
        status_bar = ttk.Frame(self.main_frame)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Add separator
        separator = ttk.Separator(status_bar, orient="horizontal")
        separator.pack(fill=tk.X)
        
        # Status bar content
        status_content = ttk.Frame(status_bar)
        status_content.pack(fill=tk.X)
        
        # Add version info
        version_label = ttk.Label(
            status_content,
            text="HMETV Control v1.0",
            font=("Segoe UI", 9),
        )
        version_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Add current time that updates
        self.time_label = ttk.Label(
            status_content,
            text="",
            font=("Segoe UI", 9),
        )
        self.time_label.pack(side=tk.RIGHT, padx=10, pady=5)
        self.update_time()
    
    def update_time(self):
        """Update the time display in the status bar"""
        current_time = datetime.now().strftime("%I:%M:%S %p - %b %d, %Y")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def pulse_animation(self):
        """Create a pulsing animation for the status indicator"""
        if self.robot_connected:
            current_color = self.status_canvas.itemcget(self.status_indicator, "fill")
            if current_color == "#2ECC71":  # If bright green
                new_color = "#27AE60"  # Slightly darker green
            else:
                new_color = "#2ECC71"  # Bright green
        else:
            current_color = self.status_canvas.itemcget(self.status_indicator, "fill")
            if current_color == "#E74C3C":  # If bright red
                new_color = "#C0392B"  # Slightly darker red
            else:
                new_color = "#E74C3C"  # Bright red
        
        self.status_canvas.itemconfig(self.status_indicator, fill=new_color)
        self.root.after(800, self.pulse_animation)  # Continue animation
    
    def check_connection(self):
        """Check if the robot is reachable"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((TCP_IP, TCP_PORT))
                if not self.robot_connected:
                    self.robot_connected = True
                    self.status_label.config(text="Status: Connected", fg="#2ECC71")
                    self.log("Robot connection established")
                return True
        except Exception:
            if self.robot_connected:
                self.robot_connected = False
                self.status_label.config(text="Status: Disconnected", fg="#E74C3C")
                self.log("Robot connection lost")
            return False
    
    def periodic_connection_check(self):
        """Periodically check the connection status"""
        while True:
            self.check_connection()
            time.sleep(10)  # Check every 10 seconds
    
    def send_instruction(self, instruction):
        """Send an instruction to the robot"""
        if not self.robot_connected and not self.check_connection():
            #messagebox.showerror("Connection Error", "Cannot connect to the robot")
            self.log("Connection Error: Cannot connect to the robot")
            return False
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((TCP_IP, TCP_PORT))
                s.sendall(instruction.encode('utf-8'))
                self.log(f"Sent: {instruction}")
                return True
        except Exception as e:
            error_msg = f"Failed to send: {e}"
            self.log(error_msg)
            messagebox.showerror("Send Error", error_msg)
            return False
    
    def send_to_destination(self, destination):
        """Send the robot to the selected destination"""
        if destination not in DESTINATIONS:
            self.log(f"Error: Unknown destination '{destination}'")
            return
        
        self.status_label.config(text=f"Status: Moving to {destination}", fg="#F39C12")
        self.log(f"Starting route to {destination}")
        
        # Show in-progress notification
        self.show_toast(f"Robot moving to {destination}", "#3498DB")
        
        # Disable all destination buttons during operation
        for button in self.destination_buttons:
            button.config(state=tk.DISABLED)
        
        # Start a separate thread to send the instructions
        threading.Thread(target=self._execute_path, args=(destination,)).start()
    
    def _execute_path(self, destination):
        """Execute the path instructions in a separate thread"""
        path = DESTINATIONS[destination]
        success = True
        
        for instruction in path:
            if not self.send_instruction(instruction):
                success = False
                break
            
            # Extract duration for simulating movement time
            cmd, duration = instruction.split(',')
            if cmd != "done" and duration.isdigit():
                # Wait for a fraction of the actual duration to simulate movement
                time.sleep(int(duration) / 5000)  # Convert ms to seconds with a divisor
        
        # Update status based on success
        if success:
            self.root.after(0, lambda: self.status_label.config(
                text=f"Status: Arrived at {destination}", fg="#2ECC71"))
            self.root.after(0, lambda: self.log(f"Successfully arrived at {destination}"))
            self.root.after(0, lambda: self.show_toast(f"Delivery completed: {destination}", "#2ECC71"))
        else:
            self.root.after(0, lambda: self.status_label.config(
                text=f"Status: Failed!", fg="#FF0000"))
        
        # Re-enable destination buttons
        for button in self.destination_buttons:
            self.root.after(0, lambda b=button: b.config(state=tk.NORMAL))
    
    def emergency_stop(self):
        """Send emergency stop command"""
        self.send_instruction("emergency-stop,0")
        self.status_label.config(text="Status: EMERGENCY STOP ACTIVATED", fg="#E74C3C")
        self.log("EMERGENCY STOP ACTIVATED")
        
        # Show prominent emergency stop notification
        popup = Toplevel(self.root)
        popup.title("EMERGENCY STOP")
        popup.geometry("500x250+400+300")
        popup.configure(bg="#E74C3C")
        popup.attributes("-topmost", True)
        
        # Add animated warning symbol
        warning_canvas = tk.Canvas(popup, width=80, height=80, bg="#E74C3C", highlightthickness=0)
        warning_canvas.pack(pady=(20, 0))
        
        # Draw warning triangle
        warning_canvas.create_polygon(40, 10, 10, 70, 70, 70, fill="#FFFFFF")
        warning_canvas.create_text(40, 45, text="!", font=("Arial", 30, "bold"), fill="#E74C3C")
        
        # Add text
        Label(
            popup, 
            text="EMERGENCY STOP\nACTIVATED", 
            font=("Segoe UI", 24, "bold"),
            fg="white",
            bg="#E74C3C",
            padx=20, 
            pady=10
        ).pack()
        
        # Add additional information
        Label(
            popup, 
            text="The robot has been stopped. Please check the area.", 
            font=("Segoe UI", 12),
            fg="white",
            bg="#E74C3C",
            padx=20
        ).pack()
        
        # Auto-close after 5 seconds
        popup.after(5000, popup.destroy)
    
    def show_toast(self, message, color="#333333"):
        """Show a toast notification"""
        toast = Toplevel(self.root)
        toast.title("")
        toast.geometry(f"300x60+{self.root.winfo_x() + self.root.winfo_width() - 320}+{self.root.winfo_y() + 60}")
        toast.configure(bg="white")
        toast.overrideredirect(True)  # Remove window decorations
        toast.attributes("-topmost", True)
        
        # Create a frame with colored left border
        frame = tk.Frame(toast, bg="white", bd=1, relief=tk.SOLID)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Add colored indicator on the left
        indicator = tk.Frame(frame, width=5, bg=color)
        indicator.pack(side=tk.LEFT, fill=tk.Y)
        
        # Add message
        Label(
            frame, 
            text=message, 
            font=("Segoe UI", 11),
            fg="#333333",
            bg="white",
            padx=10, 
            pady=5,
            anchor="w",
            justify=tk.LEFT
        ).pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Animate entry (slide in from right)
        for i in range(30):
            x = self.root.winfo_x() + self.root.winfo_width() - 320 + (30 - i) * 10
            toast.geometry(f"300x60+{x}+{self.root.winfo_y() + 60}")
            toast.update()
            time.sleep(0.01)
        
        # Auto-close after 3 seconds with fade out
        toast.after(3000, lambda: self.close_toast(toast))
    
    def close_toast(self, toast):
        """Close toast with animation"""
        try:
            # Animate exit (slide out to right)
            for i in range(30):
                x = toast.winfo_x() + i * 10
                toast.geometry(f"300x60+{x}+{toast.winfo_y()}")
                toast.update()
                time.sleep(0.01)
            toast.destroy()
        except:
            # In case the window was already destroyed
            pass
    
    def log(self, message):
        """Add a message to the log with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)  # Scroll to the bottom


def main():
    root = tk.Tk()
    # Set app icon if available
    # try:
    #     if os.path.exists("robot_icon.ico"):
    #         root.iconbitmap("robot_icon.ico")
    # except:
    #     pass
    app = ModernHospitalRobotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

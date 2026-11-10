import tkinter as tk
import psutil
import math
from datetime import datetime


# =====================================================
# A.S.T.R.A FUTURISTIC HUD
# Python 3.14 | Tkinter | PSUtil
# =====================================================

BG = "#020711"
BLUE = "#08A9FF"
CYAN = "#65D5FF"
WHITE = "#C6EFFF"
DIM = "#075080"
GREEN = "#00E6A0"


class AstraHUD:

    def __init__(self, root):

        self.root = root
        self.root.title("A.S.T.R.A - System HUD")

        self.root.configure(bg=BG)
        self.root.geometry("1400x800")
        self.root.minsize(1100, 700)

        self.root.attributes("-fullscreen", False)

        self.canvas = tk.Canvas(
            self.root,
            bg=BG,
            highlightthickness=0
        )

        self.canvas.pack(fill="both", expand=True)

        self.angle = 0

        psutil.cpu_percent(interval=None)

        # Keyboard controls
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Start HUD
        self.root.after(100, self.update_hud)

    # =================================================
    # KEYBOARD CONTROLS
    # =================================================

    def toggle_fullscreen(self, event=None):

        current = self.root.attributes("-fullscreen")

        self.root.attributes(
            "-fullscreen",
            not current
        )

    def exit_fullscreen(self, event=None):

        self.root.attributes("-fullscreen", False)

    # =================================================
    # DRAWING FUNCTIONS
    # =================================================

    def line(self, x1, y1, x2, y2,
             color=BLUE, width=1):

        self.canvas.create_line(
            x1, y1, x2, y2,
            fill=color,
            width=width
        )

    def text(self, x, y, value,
             size=12, color=CYAN,
             anchor="center",
             font="Consolas"):

        self.canvas.create_text(
            x, y,
            text=value,
            fill=color,
            font=(font, size, "bold"),
            anchor=anchor
        )

    def circle(self, x, y, radius,
               color=BLUE, width=2):

        self.canvas.create_oval(
            x-radius, y-radius,
            x+radius, y+radius,
            outline=color,
            width=width
        )

    def panel(self, x1, y1, x2, y2, title):

        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            outline=DIM,
            width=2
        )

        self.text(
            x1+12, y1+14,
            title,
            12, CYAN, "w"
        )

        self.line(
            x1+10, y1+30,
            x2-10, y1+30,
            DIM
        )

    # =================================================
    # CIRCULAR GAUGES
    # =================================================

    def gauge(self, x, y, radius,
              percentage, title):

        percentage = max(0, min(100, percentage))

        self.circle(
            x, y, radius,
            DIM, 5
        )

        # Background ring

        self.canvas.create_arc(
            x-radius, y-radius,
            x+radius, y+radius,
            start=90,
            extent=-359.9,
            style="arc",
            outline="#09233A",
            width=6
        )

        # Active percentage ring

        self.canvas.create_arc(
            x-radius, y-radius,
            x+radius, y+radius,
            start=90,
            extent=-percentage*3.6,
            style="arc",
            outline=BLUE,
            width=6
        )

        self.text(
            x, y-5,
            f"{percentage:.0f}%",
            18, WHITE
        )

        self.text(
            x, y+radius+17,
            title,
            10, CYAN
        )

    # =================================================
    # BACKGROUND
    # =================================================

    def draw_background(self, w, h):

        # Grid

        for x in range(0, w, 30):

            self.line(
                x, 0, x, h,
                "#07182B"
            )

        for y in range(0, h, 30):

            self.line(
                0, y, w, y,
                "#07182B"
            )

        # Background circular graphics

        cx = w*0.51
        cy = h*0.48

        self.circle(
            cx, cy,
            min(w, h)*0.40,
            "#06213A", 2
        )

        self.circle(
            cx, cy,
            min(w, h)*0.32,
            "#082A48", 2
        )

        self.circle(
            cx, cy,
            min(w, h)*0.25,
            "#061B30", 1
        )

    # =================================================
    # TOP INFORMATION
    # =================================================

    def draw_top(self, w):

        now = datetime.now()

        # Top ruler

        for i in range(31):

            x = 25 + i*(w-50)/30

            self.line(
                x, 8, x, 18,
                BLUE, 2
            )

            self.text(
                x, 27,
                f"{i:02}",
                8, CYAN
            )

        # Branding

        self.text(
            w/2, 55,
            "A.S.T.R.A SYSTEM",
            25, BLUE
        )

        self.text(
            w/2, 82,
            "A.S.T.R.A | AUTOMATED TRACKING & RESPONSE",
            11, CYAN
        )

        self.text(
            35, 52,
            now.strftime("%A"),
            11, WHITE, "w"
        )

        self.text(
            35, 72,
            now.strftime("%d %B %Y"),
            10, CYAN, "w"
        )

        self.text(
            w-35, 52,
            now.strftime("%H:%M:%S"),
            15, BLUE, "e"
        )

    # =================================================
    # LEFT PANEL - CPU RAM DISK
    # =================================================

    def draw_left(self, w, h):

        x1 = 35
        x2 = w*0.23

        self.panel(
            x1, 105,
            x2, h*0.76,
            "SYSTEM DIAGNOSTICS"
        )

        now = datetime.now()

        # Date

        self.text(
            (x1+x2)/2,
            160,
            now.strftime("%d"),
            48, BLUE
        )

        self.text(
            (x1+x2)/2,
            200,
            now.strftime("%B %Y").upper(),
            13, CYAN
        )

        self.line(
            x1+15, 225,
            x2-15, 225
        )

        # Hardware readings

        cpu = psutil.cpu_percent(interval=None)

        ram = psutil.virtual_memory()

        disk = psutil.disk_usage("C:\\")

        # Circular gauges

        self.gauge(
            x1+70, 300,
            43,
            cpu,
            "CPU"
        )

        self.gauge(
            x1+180, 300,
            43,
            ram.percent,
            "RAM"
        )

        self.gauge(
            x1+125, 435,
            43,
            disk.percent,
            "DISK"
        )

        # Processor details

        self.line(
            x1+15, 510,
            x2-15, 510
        )

        self.text(
            x1+15, 535,
            "PROCESSOR",
            10, CYAN, "w"
        )

        self.text(
            x1+15, 555,
            f"{psutil.cpu_count()} LOGICAL CORES",
            9, WHITE, "w"
        )

        # RAM details

        self.text(
            x1+15, 585,
            "MEMORY",
            10, CYAN, "w"
        )

        self.text(
            x1+15, 605,
            f"{ram.used/(1024**3):.1f} GB / "
            f"{ram.total/(1024**3):.1f} GB",
            9, WHITE, "w"
        )

        # Storage details

        self.text(
            x1+15, 635,
            "STORAGE (C:)",
            10, CYAN, "w"
        )

        self.text(
            x1+15, 655,
            f"{disk.free/(1024**3):.1f} GB FREE",
            9, WHITE, "w"
        )

        self.text(
            x1+15, 690,
            "SYSTEM ONLINE",
            11, GREEN, "w"
        )

    # =================================================
    # CENTER - MAIN HUD CORE
    # =================================================

    def draw_center(self, w, h):

        cx = w*0.51
        cy = h*0.48

        # Main heading

        self.text(
            cx, cy-260,
            "A.S.T.R.A OS",
            34, BLUE
        )

        # Circular rings

        for radius in [65, 90, 115, 145, 175, 205]:

            self.circle(
                cx, cy,
                radius,
                DIM, 2
            )

        # Rotating tick marks

        for i in range(60):

            angle = math.radians(
                self.angle+i*6
            )

            if i % 5 == 0:
                length = 18
                width = 2
            else:
                length = 8
                width = 1

            r1 = 180
            r2 = r1+length

            x1 = cx+math.cos(angle)*r1
            y1 = cy+math.sin(angle)*r1

            x2 = cx+math.cos(angle)*r2
            y2 = cy+math.sin(angle)*r2

            self.line(
                x1, y1, x2, y2,
                BLUE, width
            )

        # Rotating indicators

        for i in range(8):

            angle = math.radians(
                -self.angle+i*45
            )

            x = cx+math.cos(angle)*205
            y = cy+math.sin(angle)*205

            self.circle(
                x, y, 5,
                CYAN, 2
            )

        # Center core

        self.circle(
            cx, cy,
            75, BLUE, 4
        )

        self.circle(
            cx, cy,
            60, CYAN, 2
        )

        self.circle(
            cx, cy,
            45, DIM, 3
        )

        self.circle(
            cx, cy,
            30, BLUE, 2
        )

        # Core crosshair

        self.line(
            cx-45, cy,
            cx+45, cy,
            BLUE, 2
        )

        self.line(
            cx, cy-45,
            cx, cy+45,
            BLUE, 2
        )

        # Core text

        self.text(
            cx, cy-10,
            "A.S.T.R.A",
            12, WHITE
        )

        self.text(
            cx, cy+12,
            "ACTIVE",
            9, GREEN
        )

        # Bottom center information

        self.text(
            cx, cy+240,
            "ADVANCED INTERFACE CONTROL",
            11, CYAN
        )

        self.text(
            cx, cy+263,
            datetime.now().strftime("%H:%M:%S"),
            18, WHITE
        )

    # =================================================
    # RIGHT PANEL - NETWORK AND INFORMATION
    # =================================================

    def draw_right(self, w, h):

        x1 = w*0.78
        x2 = w-35

        # NETWORK PANEL

        self.panel(
            x1, 105,
            x2, 290,
            "NETWORK MONITOR"
        )

        net = psutil.net_io_counters()

        self.text(
            x1+15, 165,
            "DATA SENT",
            10, WHITE, "w"
        )

        self.text(
            x2-15, 165,
            f"{net.bytes_sent/(1024**2):.2f} MB",
            10, CYAN, "e"
        )

        self.text(
            x1+15, 205,
            "DATA RECEIVED",
            10, WHITE, "w"
        )

        self.text(
            x2-15, 205,
            f"{net.bytes_recv/(1024**2):.2f} MB",
            10, CYAN, "e"
        )

        self.text(
            x1+15, 255,
            "NETWORK STATUS",
            10, WHITE, "w"
        )

        self.text(
            x2-15, 255,
            "MONITORING",
            10, GREEN, "e"
        )

        # INFORMATION PANEL

        self.panel(
            x1, 325,
            x2, h*0.76,
            "A.S.T.R.A INFORMATION"
        )

        messages = [

            "ALL SYSTEMS OPERATIONAL",

            "MONITORING HARDWARE",

            "A.S.T.R.A CORE ACTIVE",

            "NETWORK MONITOR ACTIVE",

            "SECURE INTERFACE READY",

            "DIAGNOSTICS RUNNING",

            "WAITING FOR COMMAND"

        ]

        for i, message in enumerate(messages):

            self.text(
                x1+15,
                390+i*35,
                "> "+message,
                9, CYAN, "w"
            )

    # =================================================
    # BOTTOM CIRCULAR ICONS
    # =================================================

    def draw_bottom(self, w, h):

        labels = [
            "CORE",
            "POWER",
            "SCAN",
            "AI",
            "CONTROL",
            "DATA",
            "SYSTEM",
            "NETWORK"
        ]

        spacing = w/len(labels)

        for i, label in enumerate(labels):

            x = spacing*(i+0.5)
            y = h*0.88

            # Outer circle

            self.circle(
                x, y,
                32, BLUE, 3
            )

            self.circle(
                x, y,
                24, DIM, 2
            )

            # Animated pointer

            angle = math.radians(
                self.angle+i*45
            )

            self.line(
                x, y,
                x+17*math.cos(angle),
                y+17*math.sin(angle),
                CYAN, 3
            )

            self.text(
                x, y+48,
                label,
                9, WHITE
            )

        # Bottom line

        self.line(
            0, h-25,
            w, h-25,
            BLUE, 2
        )

        self.text(
            20, h-12,
            "A.S.T.R.A v1.0",
            9, CYAN, "w"
        )

        # The Stark Industries logo text has been completely removed from this corner.

    # =================================================
    # MAIN UPDATE LOOP
    # =================================================

    def update_hud(self):

        self.canvas.delete("all")

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        if w < 100 or h < 100:

            self.root.after(
                100,
                self.update_hud
            )

            return

        # Draw all HUD components

        self.draw_background(w, h)

        self.draw_top(w)

        self.draw_left(w, h)

        self.draw_center(w, h)

        self.draw_right(w, h)

        self.draw_bottom(w, h)

        # Animation speed

        self.angle = (self.angle+2) % 360

        # Refresh every 100 milliseconds

        self.root.after(
            100,
            self.update_hud
        )


# =====================================================
# START A.S.T.R.A
# =====================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = AstraHUD(root)

    root.mainloop()
'''
Authors - Pranava & Yamitha

Last Edited - 19:15,13-09-2024 (dd-mm-yyyy)

'''

from random import randrange
import customtkinter as ctk

class DraggableCircle:
    def __init__(self, canvas, x, y, label, radius=25):
        self.canvas = canvas
        self.radius = radius
        self.label = label
        self.connections = []  # Store the lines connected to this circle

        # Draw the circle
        self.circle = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="skyblue")
        # Draw the label
        self.text = canvas.create_text(x, y, text=label, font=("Arial", 12))

        # Bind mouse events to the circle and label
        self.canvas.tag_bind(self.circle, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.text, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.circle, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.text, "<B1-Motion>", self.on_drag)

        self._drag_data = {"x": 0, "y": 0}

    def on_press(self, event):
        """Handle the click event to initiate drag."""
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_drag(self, event):
        """Handle the drag event to move the circle and label."""
        # Compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Move the circle and text
        if (self._drag_data["y"] < (canvas_height-25)) and (self._drag_data["x"] < (canvas_width-25)) and (self._drag_data["x"] > 25) and (self._drag_data["y"] >25): 
            self.canvas.move(self.circle, delta_x, delta_y)
            self.canvas.move(self.text, delta_x, delta_y)

        # Update the positions of all lines connected to this circle
        for line, circle1, circle2 in self.connections:
            if circle1 == self:
                self.canvas.coords(line, event.x, event.y,
                                   self.canvas.coords(circle2.circle)[0] + self.radius,
                                   self.canvas.coords(circle2.circle)[1] + self.radius)
            else:
                self.canvas.coords(line,
                                   self.canvas.coords(circle1.circle)[0] + self.radius,
                                   self.canvas.coords(circle1.circle)[1] + self.radius,
                                   event.x, event.y)

        # Update drag data
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def add_connection(self, line, other_circle):
        """Store a reference to a line connecting this circle to another."""
        self.connections.append((line, self, other_circle))
        other_circle.connections.append((line, self, other_circle))


class Lines(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.circles = {}

    def draw_edge(self, canvas, circle1, circle2):
        """Draw a line between two circles and store the connection."""
        try:
            # Check if circles exist and get coordinates
            if circle1 and circle2 and canvas.coords(circle1.circle) and canvas.coords(circle2.circle):
                x1, y1 = canvas.coords(circle1.circle)[:2]
                x2, y2 = canvas.coords(circle2.circle)[:2]

                x1 += circle1.radius
                y1 += circle1.radius
                x2 += circle2.radius
                y2 += circle2.radius

                # Draw the connecting line
                line = canvas.create_line(x1, y1, x2, y2, fill="black")

                # Ensure the line is drawn beneath the circles
                canvas.tag_lower(line, circle1.circle)
                # Add the connection
                circle1.add_connection(line, circle2)
            else:
                raise ValueError("One or both of the circle coordinates are None.")
        except Exception as e:
            print(f"Error drawing edge: {e}")


class App(ctk.CTk):
    def __init__(self,canvas):
        super().__init__()

        # self.title("Draggable Circles with Lines")
        # self.geometry("800x600")

        self.lines_manager = Lines()

        # # Create a CTkFrame
        # self.frame = ctk.CTkFrame(self)
        # self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Add a Canvas to the CTkFrame
        self.canvas = canvas#tk.Canvas(self.frame, bg="white", highlightthickness=0)
        # self.canvas.pack(fill="both", expand=True)

        # Entry fields for adding circles
        # self.label_entry = ctk.CTkEntry(self, placeholder_text="Label")
        # self.label_entry.pack(pady=5)

        # self.x_entry = ctk.CTkEntry(self, placeholder_text="X-coordinate")
        # self.x_entry.pack(pady=5)

        # self.y_entry = ctk.CTkEntry(self, placeholder_text="Y-coordinate")
        # self.y_entry.pack(pady=5)

        # self.add_circle_button = ctk.CTkButton(self, text="Add Circle", command=self.add_circle)
        # self.add_circle_button.pack(pady=10)

        # Dropdown menus for adding lines between circles
        # self.circle1_var = ctk.StringVar(value="Circle 1")
        # self.circle2_var = ctk.StringVar(value="Circle 2")
        # self.circle1_dropdown = ctk.CTkOptionMenu(self, variable=self.circle1_var, values=[])
        # self.circle1_dropdown.pack(pady=5)

        # self.circle2_dropdown = ctk.CTkOptionMenu(self, variable=self.circle2_var, values=[])
        # self.circle2_dropdown.pack(pady=5)

        # self.add_line_button = ctk.CTkButton(self, text="Connect Circles", command=self.add_line)
        # self.add_line_button.pack(pady=10)

        # Keep track of circles created
        self.circles = []

    def add_circle(self,label,x,y):
        """Add a new draggable circle to the canvas."""
        # label = self.label_entry.get()
        #x = randrange(25,self.canvas.winfo_width()-25)#int(self.x_entry.get())
        #y = randrange(25,self.canvas.winfo_height()-25)#int(self.y_entry.get())

        circle = DraggableCircle(self.canvas, x, y, label)
        self.circles.append(circle)
    def add_rand_circle(self,label):
        """Add a new draggable circle to the canvas."""
        # label = self.label_entry.get()
        x = randrange(25,self.canvas.winfo_width()-25)#int(self.x_entry.get())
        y = randrange(25,self.canvas.winfo_height()-25)#int(self.y_entry.get())

        circle = DraggableCircle(self.canvas, x, y, label)
        self.circles.append(circle)

        # Update the dropdown menus with the new circle label
        # circle_labels = [circle.label for circle in self.circles]
        # self.circle1_dropdown.configure(values=circle_labels)
        # self.circle2_dropdown.configure(values=circle_labels)

    def add_line(self,circle1_label,circle2_label):
        """Add a line between two circles based on user input."""
        # circle1_label = self.circle1_var.get()
        # circle2_label = self.circle2_var.get()

        # Find circles by their labels
        circle1 = next((circle for circle in self.circles if circle.label == circle1_label), None)
        circle2 = next((circle for circle in self.circles if circle.label == circle2_label), None)

        if circle1 and circle2:
            self.lines_manager.draw_edge(self.canvas, circle1, circle2)


    def clear_canvas(self):
        """Clears all the circles and lines from the canvas."""
        self.canvas.delete("all")  
        self.circles.clear()  
        self.lines_manager = Lines()

    def get_circle_positions(self):
        """Returns a dictionary of circle labels and their (x, y) positions."""
        positions = {}
        for circle in self.circles:
            x1, y1, x2, y2 = self.canvas.coords(circle.circle)
            # Store the center of the circle (average of x1, x2 and y1, y2)
            x = (x1 + x2) / 2
            y = (y1 + y2) / 2
            positions[circle.label] = (x, y)
        return positions

# if __name__ == "__main__":
#     app = App()
#     app.mainloop()

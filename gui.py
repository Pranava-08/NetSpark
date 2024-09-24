'''
Authors - Pranava & Yamitha

Last Edited - 13:18 17-09-2024 (dd-mm-yyyy)

'''
import customtkinter as ctk
import tkinter as tk
import networkx as nx
from draggable_circles import App
import webbrowser

BACKGROUNG_COLOR = "#FFF6EA"
BUTTON_COLOR = "#229799"

# Initialize the main window
window = ctk.CTk()
window.geometry("600x400")
window.configure(bg=BACKGROUNG_COLOR)

# Create the graph
G = nx.Graph()
circle_positions = {}

# Function to handle adding a node
def add_node():
    def on_submit():
        node_name = entry.get()
        if node_name:
            if (node_name not in list(G.nodes())):
                G.add_node(node_name)  # Add the node to the graph
                print(f"Node added: {node_name}")
                visualize.add_rand_circle(node_name)
            else:
                print(f"Node {node_name} alreay exists")
        else:
            print("Enter a node")
            
        node_window.destroy()  # Close the add node window after submission

    # Create a new window for adding a node
    node_window = ctk.CTkToplevel(window)
    node_window.geometry("300x150")
    node_window.title("Add Node")
    node_window.lift()  # Bring the window to the front
    node_window.attributes("-topmost", True)  # Keep it on top of the main window

    label = ctk.CTkLabel(master=node_window, text="Enter Node Name:")
    label.pack(pady=10)
    
    entry = ctk.CTkEntry(master=node_window, width=200)
    entry.pack(pady=5)
    
    submit_button = ctk.CTkButton(master=node_window, text="Submit", command=on_submit)
    submit_button.pack(pady=10)

# Function to handle adding an edge
def add_edge():
    def on_submit():
        node1_name = entry1.get()
        node2_name = entry2.get()
        if node1_name in G.nodes and node2_name in G.nodes:
            if G.has_edge(node1_name, node2_name):
                print(f"Edge between {node1_name} and {node2_name} already exists.")
            else:
                G.add_edge(node1_name, node2_name)  # Add the edge to the graph
                print(f"Edge added between: {node1_name} and {node2_name}")
                visualize.add_line(node1_name,node2_name)
        else:
            print("One or both nodes do not exist in the graph.")
        edge_window.destroy()  # Close the add edge window after submission

    # Create a new window for adding an edge
    edge_window = ctk.CTkToplevel(window)
    edge_window.geometry("300x250")  # Increased height
    edge_window.title("Add Edge")
    edge_window.lift()  # Bring the window to the front
    edge_window.attributes("-topmost", True)  # Keep it on top of the main window
    
    label1 = ctk.CTkLabel(master=edge_window, text="Enter First Node Name:")
    label1.pack(pady=10)
    
    entry1 = ctk.CTkEntry(master=edge_window, width=200)
    entry1.pack(pady=5)
    
    label2 = ctk.CTkLabel(master=edge_window, text="Enter Second Node Name:")
    label2.pack(pady=10)
    
    entry2 = ctk.CTkEntry(master=edge_window, width=200)
    entry2.pack(pady=5)
    
    submit_button = ctk.CTkButton(master=edge_window, text="Submit", command=on_submit)
    submit_button.pack(pady=10)

def reset_graph_button():
    """Opens a confirmation window for resetting the graph and canvas."""
    
    # Create the confirmation window
    confirm_window = ctk.CTkToplevel(window)
    confirm_window.geometry("350x150")
    confirm_window.title("Reset Confirmation")
    confirm_window.lift()  
    confirm_window.attributes("-topmost", True)  
    
    label = ctk.CTkLabel(master=confirm_window, text="Are You Sure?\n\nThis will reset your progress...")
    label.pack(pady=20)

    def on_yes():
        G.clear()
        visualize.clear_canvas()
        print("Graph and visualization have been reset.")
        confirm_window.destroy() 
    def on_no():
        confirm_window.destroy()

    yes_button = ctk.CTkButton(master=confirm_window, text="Yes", command=on_yes)
    yes_button.pack(side="left", padx=20, pady=10)

    no_button = ctk.CTkButton(master=confirm_window, text="No", command=on_no)
    no_button.pack(side="right", padx=20, pady=10)

def analyse_view():
    """Switch to the Analyse view, changing the UI to show 'Analyse Graph' and 'Analyse Node' buttons."""
    global circle_positions
    if visualize.canvas.winfo_exists():
        circle_positions = visualize.get_circle_positions()

    for widget in window.winfo_children():
        widget.destroy()

    # Set the window background to #FFF6EA
    window.configure(bg=BACKGROUNG_COLOR)
    canvas_frame = ctk.CTkFrame(
    master=window,
    fg_color=BACKGROUNG_COLOR,  
    width=1600,
    height=1400,
    corner_radius=0, 
)
    canvas_frame.place(x=0, y=0)

    # Add the "Analyse Graph" and "Analyse Node" buttons in the middle of the window
    analyse_graph_button = ctk.CTkButton(
        master=window,
        text="Analyse Graph",
        fg_color=BUTTON_COLOR,
        bg_color=BACKGROUNG_COLOR,
        width=150,
        height=50,
        corner_radius=20,
        command=analyse_graph_view
    )
    analyse_graph_button.place(relx=0.5, rely=0.4, anchor="center")  # Center the button

    analyse_node_button = ctk.CTkButton(
        master=window,
        text="Analyse Node",
        fg_color=BUTTON_COLOR,
        bg_color=BACKGROUNG_COLOR,
        width=150,
        height=50,
        corner_radius=20,
        command=analyse_node_view
    )
    analyse_node_button.place(relx=0.5, rely=0.6, anchor="center")  # Center the button below

    # Add the "Back" button in the bottom right corner to return to the main view
    back_button = ctk.CTkButton(
        master=window,
        text="Back",
        fg_color=BUTTON_COLOR,
        bg_color=BACKGROUNG_COLOR,
        width=100,
        height=40,
        corner_radius=20,
        command=graph_input_view  # Function to go back to the main view
    )
    back_button.place(relx=0.9, rely=0.9, anchor="center")  # Bottom-right position

def graph_input_view():
    """Restore the initial view with the canvas, nodes, and edges."""
    
    # Clear all widgets from the window
    for widget in window.winfo_children():
        widget.destroy()

    # Set the window background to #FFF6EA
    window.configure(bg=BACKGROUNG_COLOR)

    canvas_frame = ctk.CTkFrame(
    master=window,
    fg_color=BACKGROUNG_COLOR,  
    width=1600,
    height=1400,
    corner_radius=0, 
)
    canvas_frame.place(x=0, y=0)
    
    button_1 = ctk.CTkButton(
        master=window,
        text="Add Node",
        fg_color=BUTTON_COLOR,
        bg_color=BACKGROUNG_COLOR,
        width=122,
        height=46,
        corner_radius=20,
        command=add_node
    )
    # button_1.place(x=10, y=59)

    button_2 = ctk.CTkButton(
        master=window,
        text="Add Edge",
        fg_color=BUTTON_COLOR,
        bg_color=BACKGROUNG_COLOR,
        width=122,
        height=46,
        corner_radius=20,
        command=add_edge
    )
    # button_2.place(x=10, y=148)

    button_3 = ctk.CTkButton(
        master=window,
        text="Reset",
        fg_color=BUTTON_COLOR,
        bg_color=BACKGROUNG_COLOR,
        width=122,
        height=46,
        corner_radius=20,
        command=reset_graph_button
    )
    # button_3.place(x=10, y=244)

    button_4 = ctk.CTkButton(
        master=window,
        text="Analyse",
        fg_color=BUTTON_COLOR,
        bg_color=BACKGROUNG_COLOR,
        width=122,
        height=46,
        corner_radius=20,
        command=analyse_view
    )
    # button_4.place(x=443, y=332)
    button_1.place(relx=0.03, rely=0.1)
    button_2.place(relx=0.03, rely=0.35)
    button_3.place(relx=0.03, rely=0.60)
    button_4.place(relx=0.78, rely=0.85)


    rectangle_frame = ctk.CTkFrame(
        master=window,
        fg_color="#FFFFFF",
        bg_color=BACKGROUNG_COLOR,
        # width=1.7*window.winfo_width(),
        # height=1.3*window.winfo_height(),
        corner_radius=0
    )
    rectangle_frame.place(relx=0.25, rely=0.05, relwidth=0.7, relheight=0.78)
    # rectangle_frame.place(x=143, y=16)
    # rectangle_frame.place(relx=0.25,rely=0.05)

    display_canvas = tk.Canvas(rectangle_frame, bg="white", highlightthickness=0,)
    display_canvas.place(x=0, y=0,relwidth=1, relheight=1)
    
    global visualize
    visualize = App(display_canvas)

    for node in G.nodes():
        visualize.add_circle(node,circle_positions[node][0],circle_positions[node][1])

    for edge in G.edges():
        visualize.add_line(edge[0], edge[1])

def analyse_graph_view():
    # Clear all widgets from the window
    for widget in window.winfo_children():
        widget.destroy()

    # Set the window background to #FFF6EA
    window.configure(bg=BACKGROUNG_COLOR)

    canvas_frame = ctk.CTkFrame(
    master=window,
    fg_color=BACKGROUNG_COLOR,  
    width=1600,
    height=1400,
    corner_radius=0, 
)
    canvas_frame.place(x=0, y=0)

    rectangle_frame = ctk.CTkFrame(
        master=window,
        fg_color="#FFFFFF",
        bg_color=BACKGROUNG_COLOR,
        # width=442,
        # height=304,
        corner_radius=0
    )
    rectangle_frame.place(relx=0.25, rely=0.05, relwidth=0.7, relheight=0.78)

# Create a canvas inside the frame for drawing the graph
    analyse_canvas = tk.Canvas(rectangle_frame, bg="white", highlightthickness=0)
    analyse_canvas.place(x=0, y=0,relwidth=1, relheight=1)

    # Dropdown menu for "Cliques" and "Bridges"
    analysis_option = ctk.StringVar(value="Choose Analysis")
    analysis_dropdown = ctk.CTkOptionMenu(
        master=window,
        values=["Cliques", "Bridges"],
        variable=analysis_option,
        bg_color=BACKGROUNG_COLOR,
        corner_radius=5,
        command=lambda _: analyse_graph(analysis_option.get(), analyse_canvas)  # Call the graph analysis function
    )
    analysis_dropdown.place(relx=0.12, rely=0.1, anchor="center")

    back_button = ctk.CTkButton(
        master=window,
        text="Back",
        fg_color=BUTTON_COLOR,
        bg_color=BACKGROUNG_COLOR,
        width=100,
        height=40,
        corner_radius=20,
        command=analyse_view  # Function to go back to the main view
    )
    back_button.place(relx=0.9, rely=0.9, anchor="center")  # Bottom-right position

def analyse_graph(option, canvas):
    """Function to analyse the graph based on the option chosen."""
    # Clear the canvas
    canvas.delete("all")

    if option == "Bridges":
        # Get the node positions from the stored positions (circle_positions)
        global circle_positions

        if not circle_positions:
            print("No graph available.")
            return

        for widget in window.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.destroy()
        # Find bridges in the graph using NetworkX
        bridges = list(nx.bridges(G))  # List of tuples, each tuple is an edge (node1, node2)
        print(f"Bridges are {bridges}")
        # Color the bridges differently
        # color_palette = ["red", "green", "blue", "purple", "orange"]  # Some colors for bridges
        # color_idx = 0

        for bridge in bridges:
            node1, node2 = bridge
            x1, y1 = circle_positions[node1]
            x2, y2 = circle_positions[node2]

            # Draw the bridge with a different color
            line = canvas.create_line(x1, y1, x2, y2, fill='red', width=3)
            canvas.tag_lower(line)
            # color_idx += 1

        for edge in G.edges():
            if edge not in bridges:
                node1, node2 = edge
                x1, y1 = circle_positions[node1]
                x2, y2 = circle_positions[node2]

                line = canvas.create_line(x1, y1, x2, y2, fill='blue', width=3)
                canvas.tag_lower(line)

         # Draw the nodes using the saved positions
        for node, (x, y) in circle_positions.items():
            radius = 25  # Same radius as in draggable circle
            canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="skyblue")
            canvas.create_text(x, y, text=node, font=("Arial", 12))

        # Show the definition of a bridge below the graph
        bridge_definition = "Bridges are edges in a graph whose removal increases the number of connected components."
        definition_label = ctk.CTkLabel(master=window, text=bridge_definition, wraplength=400, text_color="black",bg_color=BACKGROUNG_COLOR)
        definition_label.place(relx=0.4, rely=0.9, anchor="center")

    if option == "Cliques":
        # global circle_positions

        if not circle_positions:
            print("No graph available.")
            return

        for widget in window.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.destroy()

        # Find cliques in the graph using NetworkX
        cliques = list(nx.find_cliques(G))  # List of tuples, each tuple is an edge (node1, node2)
        print(f"cliques are {cliques}")
        # Color the bridges differently
        color_palette = ["red", "green", "blue", "purple", "orange"]  # Some colors for bridges
        color_idx = 0

        for clique in cliques:
            for node1 in clique:
                for node2 in clique:
                    if node1 != node2:
                        x1, y1 = circle_positions[node1]
                        x2, y2 = circle_positions[node2]

                        line = canvas.create_line(x1, y1, x2, y2, 
                                            fill=color_palette[color_idx%len(color_palette)],
                                            width=3)
                        canvas.tag_lower(line)
            color_idx+=1
            
        # Draw the nodes using the saved positions
        for node, (x, y) in circle_positions.items():
            radius = 25  # Same radius as in draggable circle
            canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="skyblue")
            canvas.create_text(x, y, text=node, font=("Arial", 12))
        
        #clique definition 
        clique_definiton = 'A clique is a subset of vertices in a graph such that each vertex in the subset is directly connected to every other vertex in the same subset.'
        definition_label = ctk.CTkLabel(master=window, text=clique_definiton, wraplength=400, text_color="black",bg_color=BACKGROUNG_COLOR)
        definition_label.place(relx=0.4, rely=0.9, anchor="center")

def analyse_node_view():
    """Analyse Node View with dropdown for different centrality measures."""
    # Clear all widgets from the window
    for widget in window.winfo_children():
        widget.destroy()

    # Set the window background to #FFF6EA
    window.configure(bg=BACKGROUNG_COLOR)

    # Frame for the canvas
    canvas_frame = ctk.CTkFrame(
        master=window,
        fg_color=BACKGROUNG_COLOR,  
        width=1600,
        height=1400,
        corner_radius=0, 
    )
    canvas_frame.place(x=0, y=0)

    # Frame for the graph canvas (to display the graph)
    rectangle_frame = ctk.CTkFrame(
        master=window,
        fg_color="#FFFFFF",
        bg_color=BACKGROUNG_COLOR,
        # width=442,
        # height=304,
        corner_radius=0
    )
    rectangle_frame.place(relx=0.25, rely=0.05, relwidth=0.7, relheight=0.78)

    # Create a canvas for drawing the graph
    analyse_canvas = tk.Canvas(rectangle_frame, bg="white", highlightthickness=0)
    analyse_canvas.place(x=0, y=0,relwidth=1, relheight=1)

    # Dropdown menu for centrality measures
    metric_options = ctk.StringVar(value="Choose Centrality")
    metric_dropdown = ctk.CTkOptionMenu(
        master=window,bg_color=BACKGROUNG_COLOR
        ,values=["Degree Centrality", "Betweennes\n Centrality", "Katz Centrality"],
        variable=metric_options,
        command=lambda _: draw_nodes(analyse_canvas, metric_options.get())  # Call the node drawing and click binding function
    )
    metric_dropdown.place(relx=0.12, rely=0.1, anchor="center")

    # Back button to return to the main view
    back_button = ctk.CTkButton(
        master=window,
        text="Back",
        fg_color=BUTTON_COLOR,
        bg_color=BACKGROUNG_COLOR,
        width=100,
        height=40,
        corner_radius=20,
        command=analyse_view  # Function to go back to the main view
    )
    back_button.place(relx=0.9, rely=0.9, anchor="center")

def draw_nodes(canvas, metric):
    """Draw nodes on the canvas and bind clicks to display centrality based on the selected type."""
    # Clear the canvas
    canvas.delete("all")

    # Get node positions from the global variable circle_positions
    global circle_positions
    if not circle_positions:
        print("No circle positions available.")
        return
    
    for edge in G.edges():
        node1, node2 = edge
        x1, y1 = circle_positions[node1]
        x2, y2 = circle_positions[node2]

        line = canvas.create_line(x1, y1, x2, y2, fill='black', width=3)
        canvas.tag_lower(line)
        
    # Draw the nodes using the saved positions and bind a click event
    for node, (x, y) in circle_positions.items():
        radius = 25  # Same radius as in draggable circle
        node_oval = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="skyblue")
        canvas.create_text(x, y, text=node, font=("Arial", 12))

        # Bind a click event to the node, passing the centrality type and node name
        canvas.tag_bind(node_oval, "<Button-1>", lambda event, n=node: display_info(n, metric))


def display_info(node, metric):
    """Display the information for the clicked node."""
    global G

    # Calculate the centrality based on the selected type
    if metric == "Degree Centrality":
        metric_value = nx.degree_centrality(G)[node]
        metric_definition = "Degree Centrality is the number of edges connected to a node divided by the total possible edges."
        wiki_url = "https://en.wikipedia.org/wiki/Degree_centrality"
    elif metric == "Betweenness Centrality":
        metric_value = nx.betweenness_centrality(G)[node]
        metric_definition = "Betweenness Centrality measures the extent to which a node lies on paths between other nodes."
        wiki_url = "https://en.wikipedia.org/wiki/Betweenness_centrality"
    elif metric == "Katz Centrality":
        metric_value = nx.katz_centrality(G)[node]
        metric_definition = "Katz Centrality measures the influence of a node by considering the number of immediate neighbors and the centrality of those neighbors."
        wiki_url = "https://en.wikipedia.org/wiki/Katz_centrality"

    # Display the centrality value and definition
    metric_value_text = f"{metric} for node {node}: {metric_value:.4f}"
    print(metric_value_text)  # This can be shown in the console, or create a label to show it on the UI

    # Display centrality and definition below the graph
    # Clear any existing labels
    for widget in window.winfo_children():
        if isinstance(widget, ctk.CTkLabel):
            widget.destroy()

    # Create a label to display the centrality value
    centrality_label = ctk.CTkLabel(master=window, text=metric_value_text+"\n"+metric_definition+"\n"+"For a more detailed definition click here", wraplength=400, text_color="black",bg_color=BACKGROUNG_COLOR)
    centrality_label.place(relx=0.4, rely=0.92, anchor="center")
    centrality_label.bind("<Button-1>", lambda e: open_wiki_page(wiki_url))


def open_wiki_page(url):
    """Open the Wikipedia page for the selected centrality measure."""
    webbrowser.open_new_tab(url)

    # Create a label to display the definition
    # definition_label = ctk.CTkLabel(master=window, text=centrality_definition, wraplength=400, text_color="black",bg_color=BACKGROUNG_COLOR)
    # definition_label.place(relx=0.5, rely=0.9, anchor="center")


graph_input_view()

window.resizable(True, True)
window.mainloop()

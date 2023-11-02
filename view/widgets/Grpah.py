def draw_tree_graph(arg):
    G = nx.DiGraph()
    G.add_node("A")
    G.add_edge("A", "B")
    G.add_edge("A", "C")
    G.add_edge("B", "D")
    G.add_edge("B", "E")
    G.add_edge("C", "F")

    pos = nx.spring_layout(G)  # Posizionamento dei nodi nel grafico

    # Creare un frame per il grafo ad albero
    frame_tree = ttk.Frame(arg)
    frame_tree.pack()

    # Creare un oggetto Figure di Matplotlib per il grafo ad albero
    fig_tree = Figure(figsize=(4, 3), dpi=100)
    ax_tree = fig_tree.add_subplot(111)

    # Aggiungi un'etichetta per ciascun nodo
    node_labels = {node: node for node in G.nodes}

    # Aggiungi un evento quando il mouse passa sopra un nodo
    def on_node_hover(event):
        if event.xdata is not None and event.ydata is not None:
            for node in G.nodes:
                
                x, y = pos[node]
                if abs(x - event.xdata) < 0.1 and abs(y - event.ydata) < 0.1:
                    ax_tree.set_title(f"Node: {node}", fontsize=12, color='blue')
                    print(f"{node}")
                else:
                    ax_tree.set_title("")

            tree_canvas.draw()

    tree_canvas = FigureCanvasTkAgg(fig_tree, master=frame_tree)
    tree_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Disegna il grafo ad albero con etichette per i nodi
    nx.draw(G, pos, labels=node_labels, with_labels=True, node_size=50, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", ax=ax_tree)
    tree_canvas.draw()

    tree_canvas.mpl_connect('motion_notify_event', on_node_hover)

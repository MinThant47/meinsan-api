from schema import chatbot

graph = chatbot.get_graph()
png_data = graph.draw_mermaid_png()

# Save to file
with open("graph.png", "wb") as f:
    f.write(png_data)

print("Graph saved as graph.png. Open it to view.")
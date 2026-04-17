# AWS Architecture Diagram Generator

Generate a Python script using the `diagrams` library to create an AWS architecture diagram based on this description:

{{description}}

## Requirements:
- Use Graphviz with these settings:
  - graph_attr["fontsize"] = "32"
  - node_attr["fontsize"] = "16"
  - edge_attr["fontsize"] = "15"
  - graph_attr["dpi"] = "96"
  - direction = "LR"
  - node_attr["width"] = "1.1"
  - node_attr["height"] = "0.6"
  - graph_attr["nodesep"] = "0.6"
  - graph_attr["ranksep"] = "0.8"
  - graph_attr["pad"] = "0.5"

- Cluster titles: fontsize="15", style="bold", margin="30"
- Node labels: Single line, service name only (no technical details)
- Layout: Left to right (landscape)
- Use appropriate AWS service icons from diagrams library
- Group services by functional zones using Clusters

Generate the complete Python code and execute it to create the diagram.

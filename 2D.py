from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_degrees(adj_matrix):
   
    return [sum(row) for row in adj_matrix]

def detect_topology_from_degrees(degree):
    n = len(degree)

    if degree.count(1) == n - 1 and degree.count(n - 1) == 1:
        return "Star Topology", "O(n²) - Checks degree of all nodes in adjacency matrix."
    if all(d == 2 for d in degree):
        return "Ring Topology", "O(n²) - Checks all nodes have degree 2."
    if all(d == n - 1 for d in degree):
        return "Mesh Topology", "O(n²) - Confirms every node connects to every other node."
    if degree.count(1) == 2 and degree.count(2) == n - 2:
        return "Bus Topology", "O(n²) - Checks specific node degrees characteristic of bus."
    return "Unknown or Irregular Topology", "O(n²) - General check without matching known patterns."

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    suggestion = ""
    time_complexity = ""
    matrix_input = ""
    nodes = ""
    steps = []

    if request.method == "POST":
        try:
            nodes = int(request.form["nodes"])
            matrix_input = request.form["matrix"].strip().split("\n")
            adj_matrix = []

            for row in matrix_input:
                nums = list(map(int, row.strip().split()))
                if len(nums) != nodes:
                    result = f"Each row must contain {nodes} numbers."
                    return render_template(
                        "index.html",
                        result=result,
                        suggestion=suggestion,
                        time_complexity=time_complexity,
                        matrix_input=request.form["matrix"],
                        nodes=nodes,
                        steps=steps,
                    )
                adj_matrix.append(nums)

            
            degrees = calculate_degrees(adj_matrix)
            topology, time_complexity = detect_topology_from_degrees(degrees)

            suggestions = {
                "Star Topology": "Suggestion: Upgrade to Mesh for better fault tolerance.",
                "Ring Topology": "Suggestion: Monitor for breaks; consider Mesh for stability.",
                "Mesh Topology": "Suggestion: Already optimal for reliability.",
                "Bus Topology": "Suggestion: Common in older systems; consider upgrading to Ring or Mesh.",
                "Unknown or Irregular Topology": "Suggestion: Network doesn't follow standard topology; review design.",
            }

            result = f"Detected Network Topology: {topology}"
            suggestion = suggestions[topology]

            
            steps = [
                "Step 1: Calculate degrees of each node from adjacency matrix.",
                "Step 2: Determine topology by analyzing degree patterns.",
            ]

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template(
        "index.html",
        result=result,
        suggestion=suggestion,
        time_complexity=time_complexity,
        matrix_input=matrix_input,
        nodes=nodes,
        steps=steps,
    )


if __name__ == "__main__":
    app.run(debug=True)

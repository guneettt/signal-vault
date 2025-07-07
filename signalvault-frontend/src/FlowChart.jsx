import React, { useEffect, useState } from "react";
import { useParams, useSearchParams } from "react-router-dom";
import ReactFlow, { Background, Controls } from "reactflow";
import "reactflow/dist/style.css";

const FlowChart = () => {
  const { filename } = useParams();
  const [searchParams] = useSearchParams();
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [loading, setLoading] = useState(true);

  const query = searchParams.get("query") || "";

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          `http://localhost:5050/api/flow/${encodeURIComponent(filename)}?query=${encodeURIComponent(query)}`
        );
        const data = await response.json();

        if (!data.steps || data.steps.length === 0) {
          setNodes([{ id: "empty", data: { label: "No steps found" }, position: { x: 100, y: 100 } }]);
          setEdges([]);
          return;
        }

        const stepEmojis = ["🧠", "🧼", "🧯", "🩹", "📞", "🛟", "🚑", "✅"];

        const newNodes = data.steps.map((step, i) => ({
            id: `node-${i}`,
            data: { label: `${stepEmojis[i % stepEmojis.length] || "➡️"} Step ${i + 1}: ${step}` },
            position: { x: i * 420, y: 0 }, // precise horizontal line
            style: {
                width: 360,
                padding: "16px",
                borderRadius: 14,
                border: "2px solid #3b82f6",
                background: "#ffffff",
                color: "#1e293b",
                fontSize: "1rem",
                fontWeight: 500,
                textAlign: "left",
                lineHeight: 1.6,
                boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
            }
        }));




        const newEdges = data.steps.slice(1).map((_, i) => ({
            id: `edge-${i}`,
            source: `node-${i}`,
            target: `node-${i + 1}`,
            animated: true,
            type: "smoothstep",
            style: { stroke: "#3b82f6" },
            }));


        setNodes(newNodes);
        setEdges(newEdges);
      } catch (err) {
        console.error("Error loading flow:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [filename, query]);

return (
  <div style={{ height: "100vh", width: "100%", background: "#f9fbff", overflowX: "auto" }}>
    <h2 style={{
      textAlign: "center",
      marginBottom: "1.5rem",
      fontSize: "1.8rem",
      color: "#1d4ed8"
    }}>
      🧠 Emergency Flow Summary
    </h2>

    <div style={{
      minWidth: `${nodes.length * 420}px`,
      height: "70vh",
      paddingBottom: "2rem"
    }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        nodesDraggable={false}
        panOnScroll
        zoomOnScroll
        fitViewOptions={{ padding: 0.5 }}
        defaultEdgeOptions={{
          animated: true,
          type: "smoothstep",
          markerEnd: { type: "arrowclosed" },
          style: { stroke: "#3b82f6" }
        }}
      >
        <Background gap={24} />
        <Controls />
      </ReactFlow>
    </div>

    <div style={{ textAlign: "center", marginTop: "2rem" }}>
      <a
        href="/"
        style={{
          padding: "0.6rem 1.2rem",
          background: "#2563eb",
          color: "#ffffff",
          borderRadius: "8px",
          fontWeight: 500,
          textDecoration: "none",
          boxShadow: "0 2px 6px rgba(0,0,0,0.1)"
        }}
      >
        ← Back to Dashboard
      </a>
    </div>
  </div>
);


};

export default FlowChart;

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

        // ✅ Filter out noisy/unnecessary steps (basic heuristics)
        const importantSteps = (data.steps || [])
          .filter(step =>
            step &&
            step.length < 180 &&
            !step.toLowerCase().includes("note") &&
            !step.toLowerCase().includes("see also") &&
            !step.toLowerCase().includes("copyright")
          )
          .slice(0, 6); // Limit to 6 key steps

        if (!importantSteps.length) {
          setNodes([
            {
              id: "empty",
              data: { label: "No useful steps found" },
              position: { x: 100, y: 100 },
              style: {
                padding: "20px",
                borderRadius: "12px",
                background: "#1e293b",
                color: "#f1f5f9",
                border: "2px dashed #6366f1",
              }
            }
          ]);
          setEdges([]);
          return;
        }

        const emojis = ["🧠", "🧼", "🧯", "🩹", "📞", "🚑", "✅"];

        const newNodes = importantSteps.map((step, i) => ({
          id: `node-${i}`,
          data: {
            label: `${emojis[i % emojis.length]} Step ${i + 1}: ${step}`
          },
          position: { x: i * 420, y: 0 },
          style: {
            width: 360,
            padding: "16px",
            borderRadius: 14,
            border: "2px solid #6366f1",
            background: "#1e293b",
            color: "#f1f5f9",
            fontSize: "1rem",
            fontWeight: 500,
            textAlign: "left",
            lineHeight: 1.6,
            boxShadow: "0 6px 20px rgba(0,0,0,0.3)",
          }
        }));

        const newEdges = importantSteps.slice(1).map((_, i) => ({
          id: `edge-${i}`,
          source: `node-${i}`,
          target: `node-${i + 1}`,
          animated: true,
          type: "smoothstep",
          style: { stroke: "#6366f1" },
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
    <div style={{
      minHeight: "100vh",
      background: "linear-gradient(to bottom right, #0f172a, #1e293b)",
      color: "#f1f5f9",
      padding: "2rem",
      overflowX: "auto"
    }}>
      <h2 style={{
        textAlign: "center",
        marginBottom: "1.5rem",
        fontSize: "2.2rem",
        color: "#a78bfa"
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
            style: { stroke: "#6366f1" }
          }}
        >
          <Background gap={24} color="#334155" />
          <Controls style={{ backgroundColor: "#1e293b", color: "#f1f5f9" }} />
        </ReactFlow>
      </div>

      <div style={{ textAlign: "center", marginTop: "2rem" }}>
        <a
          href="/"
          style={{
            padding: "0.6rem 1.2rem",
            background: "linear-gradient(to right, #8b5cf6, #6366f1)",
            color: "#ffffff",
            borderRadius: "999px",
            fontWeight: 500,
            textDecoration: "none",
            boxShadow: "0 4px 12px rgba(0,0,0,0.2)"
          }}
        >
          ← Back to Dashboard
        </a>
      </div>
    </div>
  );
};

export default FlowChart;

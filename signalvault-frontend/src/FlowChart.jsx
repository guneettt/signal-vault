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

        const newNodes = data.steps.map((step, i) => ({
          id: `node-${i}`,
          data: { label: step },
          position: { x: 250, y: i * 120 },
          style: {
            padding: "10px 14px",
            borderRadius: "10px",
            border: "1px solid #3b82f6",
            background: "#fff",
            color: "#1e293b",
            fontSize: "0.95rem",
          }
        }));

        const newEdges = data.steps.slice(1).map((_, i) => ({
          id: `edge-${i}`,
          source: `node-${i}`,
          target: `node-${i + 1}`,
          animated: true,
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
    <div style={{ height: "100vh", background: "#f1f5f9" }}>
      {loading ? (
        <p style={{ padding: "2rem", textAlign: "center" }}>Loading flow...</p>
      ) : (
        <ReactFlow nodes={nodes} edges={edges} fitView>
          <Background gap={20} />
          <Controls />
        </ReactFlow>
      )}
    </div>
  );
};

export default FlowChart;

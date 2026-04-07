import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from "remotion";
import { THEME } from "../theme";
import React, { useMemo } from "react";

// Generate 3D mesh nodes (matching homepage 7 Z-layers, 75 nodes)
interface Node {
  x: number;
  y: number;
  z: number;
  size: "sm" | "md" | "lg";
  isHub: boolean;
  isTarget: boolean;
}

function generateNodes(seed: number): Node[] {
  const nodes: Node[] = [];
  const layers = 7;
  const nodesPerLayer = [8, 12, 14, 12, 12, 10, 7];
  const zSpacing = 60;

  for (let layer = 0; layer < layers; layer++) {
    const count = nodesPerLayer[layer];
    const z = (layer - 3) * zSpacing;
    for (let i = 0; i < count; i++) {
      const angle = (i / count) * Math.PI * 2 + layer * 0.3;
      const radius = 120 + Math.sin(seed + i * 7) * 80;
      nodes.push({
        x: 300 + Math.cos(angle) * radius,
        y: 300 + Math.sin(angle) * radius,
        z,
        size: i % 5 === 0 ? "lg" : i % 3 === 0 ? "md" : "sm",
        isHub: layer === 3 && i < 3,
        isTarget: layer === 2 && i < 3,
      });
    }
  }
  return nodes;
}

// Generate wire connections
interface Wire {
  from: number;
  to: number;
  bright: boolean;
}

function generateWires(nodes: Node[]): Wire[] {
  const wires: Wire[] = [];
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const dx = nodes[i].x - nodes[j].x;
      const dy = nodes[i].y - nodes[j].y;
      const dz = nodes[i].z - nodes[j].z;
      const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
      if (dist < 160) {
        wires.push({
          from: i,
          to: j,
          bright: Math.random() > 0.7,
        });
      }
    }
  }
  return wires.slice(0, 66); // Match homepage: 66 wires
}

export const MeshScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const totalFrames = 15 * fps;

  const nodes = useMemo(() => generateNodes(42), []);
  const wires = useMemo(() => generateWires(nodes), [nodes]);

  // Orbit rotation
  const rotateY = interpolate(frame, [0, totalFrames], [0, 360]);
  const rotateX = -18;

  // Zoom cycle: normal -> zoom in -> normal
  const zoomCycle = frame % (8 * fps);
  const zoom = interpolate(
    zoomCycle,
    [0, 2 * fps, 4 * fps, 6 * fps, 8 * fps],
    [1, 1.6, 1.6, 1, 1],
    { extrapolateRight: "clamp" }
  );

  // Scene fade in/out
  const fadeIn = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: "clamp",
  });
  const fadeOut = interpolate(frame, [totalFrames - 30, totalFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Scan sphere
  const scanPhase = (frame % (8 * fps)) / fps;
  const scanSize = scanPhase < 3
    ? interpolate(scanPhase, [0, 0.5, 2, 3], [0, 50, 300, 500])
    : 0;
  const scanOpacity = scanPhase < 3
    ? interpolate(scanPhase, [0, 0.5, 2, 3], [0, 0.6, 0.2, 0])
    : 0;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: THEME.bg,
        justifyContent: "center",
        alignItems: "center",
        opacity: fadeIn * fadeOut,
      }}
    >
      {/* Title overlay */}
      <div
        style={{
          position: "absolute",
          top: 80,
          width: "100%",
          textAlign: "center",
          zIndex: 10,
        }}
      >
        <h2
          style={{
            fontFamily: THEME.font,
            fontSize: 48,
            fontWeight: 700,
            color: "#fff",
            margin: 0,
          }}
        >
          Every Connection,{" "}
          <span
            style={{
              background: `linear-gradient(135deg, ${THEME.green}, #22d46a)`,
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
            }}
          >
            Orchestrated
          </span>
        </h2>
      </div>

      {/* 3D Mesh container */}
      <div
        style={{
          width: 600,
          height: 600,
          position: "relative",
          perspective: 1200,
        }}
      >
        <svg
          width={600}
          height={600}
          style={{
            transform: `rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(${zoom})`,
            transformStyle: "preserve-3d",
          }}
        >
          {/* Wires */}
          {wires.map((wire, i) => {
            const a = nodes[wire.from];
            const b = nodes[wire.to];
            const wireOpacity = wire.bright
              ? 0.3 + Math.sin(frame * 0.05 + i) * 0.2
              : 0.08;
            return (
              <line
                key={`w-${i}`}
                x1={a.x}
                y1={a.y}
                x2={b.x}
                y2={b.y}
                stroke={
                  wire.bright
                    ? `rgba(56,189,248,${wireOpacity})`
                    : `rgba(26,183,89,${wireOpacity})`
                }
                strokeWidth={wire.bright ? 1.5 : 1}
              />
            );
          })}

          {/* Nodes */}
          {nodes.map((node, i) => {
            const size =
              node.size === "lg" ? 16 : node.size === "md" ? 12 : 8;
            const pulse = node.isHub
              ? 1 + Math.sin(frame * 0.08 + i) * 0.15
              : 1;
            const nodeOpacity = node.isHub ? 0.9 : node.isTarget ? 0.8 : 0.6;

            // Target nodes flash red then green
            let fillColor = THEME.green;
            if (node.isTarget) {
              const targetPhase = ((frame + i * 30) % (8 * fps)) / fps;
              if (targetPhase > 1.5 && targetPhase < 2.0) {
                fillColor = "rgba(239,68,68,0.8)";
              } else if (targetPhase > 2.0 && targetPhase < 2.5) {
                fillColor = "#fff";
              }
            }

            return (
              <circle
                key={`n-${i}`}
                cx={node.x}
                cy={node.y}
                r={size * pulse * 0.5}
                fill={fillColor}
                opacity={nodeOpacity}
              />
            );
          })}

          {/* Scan sphere */}
          {scanSize > 0 && (
            <circle
              cx={300}
              cy={300}
              r={scanSize * 0.5}
              fill="none"
              stroke={THEME.green}
              strokeWidth={2}
              opacity={scanOpacity}
            />
          )}
        </svg>
      </div>
    </AbsoluteFill>
  );
};

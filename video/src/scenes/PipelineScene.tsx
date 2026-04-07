import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { THEME } from "../theme";

const pipelineSteps = [
  { label: "Assess Needs", icon: "?" },
  { label: "Read Docs", icon: "📄" },
  { label: "Map Schema", icon: "🗺" },
  { label: "Build", icon: "🔧" },
  { label: "Test", icon: "✓" },
  { label: "Handle Errors", icon: "🛡" },
  { label: "Rate Limit", icon: "⏱" },
  { label: "Deploy", icon: "🚀" },
  { label: "Monitor", icon: "📊" },
];

export const PipelineScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const totalFrames = 18 * fps;

  // Title fade in
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: "clamp",
  });

  // Fade out
  const fadeOut = interpolate(frame, [totalFrames - 30, totalFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Pipeline progress: each step takes ~40 frames, starts at frame 40
  const pipeStart = 40;
  const stepDuration = 40;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: THEME.bg,
        justifyContent: "center",
        alignItems: "center",
        opacity: fadeOut,
      }}
    >
      {/* Title */}
      <div
        style={{
          position: "absolute",
          top: 160,
          width: "100%",
          textAlign: "center",
          opacity: titleOpacity,
        }}
      >
        <div
          style={{
            fontSize: 14,
            fontWeight: 700,
            letterSpacing: 2.5,
            textTransform: "uppercase",
            color: THEME.green,
            marginBottom: 16,
            fontFamily: THEME.font,
          }}
        >
          How It Works
        </div>
        <h2
          style={{
            fontFamily: THEME.font,
            fontSize: 48,
            fontWeight: 700,
            color: "#fff",
            margin: 0,
          }}
        >
          AI builds the integration pipeline
        </h2>
      </div>

      {/* Pipeline */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 0,
          marginTop: 80,
        }}
      >
        {pipelineSteps.map((step, i) => {
          const stepStart = pipeStart + i * stepDuration;
          const isActive =
            frame >= stepStart && frame < stepStart + stepDuration;
          const isDone = frame >= stepStart + stepDuration;
          const stepProgress = interpolate(
            frame,
            [stepStart, stepStart + 15],
            [0, 1],
            { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
          );

          // Line fill between nodes
          const lineFill = isDone
            ? 1
            : isActive
            ? interpolate(
                frame,
                [stepStart + 20, stepStart + stepDuration],
                [0, 1],
                { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
              )
            : 0;

          const circleColor = isDone
            ? "rgba(26,183,89,0.06)"
            : isActive
            ? "rgba(26,183,89,0.12)"
            : "rgba(255,255,255,0.03)";

          const borderColor = isDone
            ? "rgba(26,183,89,0.4)"
            : isActive
            ? THEME.green
            : "rgba(255,255,255,0.1)";

          const glowShadow =
            isActive
              ? `0 0 20px ${THEME.greenGlow}, 0 0 40px rgba(26,183,89,0.15)`
              : isDone
              ? `0 0 8px rgba(26,183,89,0.1)`
              : "none";

          const labelColor = isDone
            ? "rgba(26,183,89,0.5)"
            : isActive
            ? THEME.green
            : "rgba(255,255,255,0.3)";

          const nodeScale = isActive
            ? interpolate(
                Math.sin(frame * 0.1),
                [-1, 1],
                [1.0, 1.08]
              )
            : 1;

          return (
            <div key={i} style={{ display: "flex", alignItems: "center" }}>
              {/* Node */}
              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  gap: 10,
                  width: 100,
                }}
              >
                <div
                  style={{
                    width: 56,
                    height: 56,
                    borderRadius: "50%",
                    background: circleColor,
                    border: `1.5px solid ${borderColor}`,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    boxShadow: glowShadow,
                    transform: `scale(${nodeScale})`,
                    transition: "all 0.3s",
                    fontSize: 22,
                  }}
                >
                  {isDone ? (
                    <svg width={20} height={20} viewBox="0 0 24 24" fill="none">
                      <path
                        d="M5 13l4 4L19 7"
                        stroke={THEME.green}
                        strokeWidth={2.5}
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeDasharray={20}
                        strokeDashoffset={interpolate(
                          stepProgress,
                          [0, 1],
                          [20, 0]
                        )}
                      />
                    </svg>
                  ) : (
                    <span style={{ opacity: isActive ? 1 : 0.3 }}>
                      {step.icon}
                    </span>
                  )}
                </div>
                <span
                  style={{
                    fontSize: 12,
                    fontWeight: 600,
                    color: labelColor,
                    fontFamily: THEME.font,
                    whiteSpace: "nowrap",
                  }}
                >
                  {step.label}
                </span>
              </div>

              {/* Connecting line */}
              {i < pipelineSteps.length - 1 && (
                <div
                  style={{
                    width: 48,
                    height: 2,
                    background: "rgba(255,255,255,0.06)",
                    position: "relative",
                    overflow: "hidden",
                  }}
                >
                  <div
                    style={{
                      position: "absolute",
                      top: 0,
                      left: 0,
                      height: "100%",
                      width: `${lineFill * 100}%`,
                      background: THEME.green,
                      borderRadius: 2,
                    }}
                  />
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Progress label */}
      <div
        style={{
          position: "absolute",
          bottom: 180,
          width: "100%",
          textAlign: "center",
        }}
      >
        {(() => {
          const currentStepIdx = Math.floor(
            Math.max(0, frame - pipeStart) / stepDuration
          );
          const clampedIdx = Math.min(
            currentStepIdx,
            pipelineSteps.length - 1
          );
          const showLabel =
            frame >= pipeStart && frame < pipeStart + pipelineSteps.length * stepDuration;
          if (!showLabel) return null;
          return (
            <p
              style={{
                fontFamily: THEME.font,
                fontSize: 20,
                color: THEME.muted,
                margin: 0,
              }}
            >
              {pipelineSteps[clampedIdx].label}...
            </p>
          );
        })()}
      </div>
    </AbsoluteFill>
  );
};

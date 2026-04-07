import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { THEME } from "../theme";

const problems = [
  { icon: "⚡", text: "Fragile point-to-point connections" },
  { icon: "🔄", text: "Months to build each integration" },
  { icon: "🔒", text: "Vendor lock-in with rigid iPaaS tools" },
  { icon: "📉", text: "AI agents blocked by API complexity" },
];

export const ProblemScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Fade in
  const fadeIn = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: "clamp",
  });

  // Title
  const titleProgress = spring({ frame: frame - 10, fps, config: { damping: 15 } });

  // Fade out
  const totalFrames = 15 * fps;
  const fadeOut = interpolate(frame, [totalFrames - 30, totalFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: THEME.bg,
        justifyContent: "center",
        alignItems: "center",
        opacity: fadeIn * fadeOut,
      }}
    >
      {/* Section label */}
      <div style={{ textAlign: "center", zIndex: 1 }}>
        <div
          style={{
            fontSize: 14,
            fontWeight: 700,
            letterSpacing: 2.5,
            textTransform: "uppercase",
            color: THEME.green,
            marginBottom: 20,
            fontFamily: THEME.font,
            opacity: titleProgress,
          }}
        >
          The Problem
        </div>

        <h2
          style={{
            fontFamily: THEME.font,
            fontSize: 52,
            fontWeight: 700,
            color: "#fff",
            lineHeight: 1.2,
            maxWidth: 800,
            margin: "0 auto 60px",
            opacity: titleProgress,
            transform: `translateY(${interpolate(titleProgress, [0, 1], [30, 0])}px)`,
          }}
        >
          Every API is a{" "}
          <span style={{ color: "rgba(239,68,68,0.9)" }}>wall</span>
          <br />
          between your AI and the world
        </h2>

        {/* Problem cards */}
        <div
          style={{
            display: "flex",
            gap: 28,
            justifyContent: "center",
            flexWrap: "wrap",
            maxWidth: 1200,
          }}
        >
          {problems.map((p, i) => {
            const cardProgress = spring({
              frame: frame - 40 - i * 12,
              fps,
              config: { damping: 14 },
            });
            return (
              <div
                key={i}
                style={{
                  background: THEME.cardBg,
                  border: `1px solid ${THEME.border}`,
                  borderRadius: 16,
                  padding: "32px 28px",
                  width: 250,
                  textAlign: "center",
                  opacity: cardProgress,
                  transform: `translateY(${interpolate(cardProgress, [0, 1], [40, 0])}px)`,
                }}
              >
                <div style={{ fontSize: 36, marginBottom: 16 }}>{p.icon}</div>
                <p
                  style={{
                    fontFamily: THEME.font,
                    fontSize: 17,
                    color: THEME.muted,
                    lineHeight: 1.5,
                    margin: 0,
                  }}
                >
                  {p.text}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

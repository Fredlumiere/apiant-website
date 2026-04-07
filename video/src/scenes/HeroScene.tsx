import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { THEME } from "../theme";

export const HeroScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Badge fade in
  const badgeOpacity = interpolate(frame, [10, 25], [0, 1], {
    extrapolateRight: "clamp",
  });
  const badgeY = interpolate(frame, [10, 25], [20, 0], {
    extrapolateRight: "clamp",
  });

  // Title spring
  const titleProgress = spring({ frame: frame - 20, fps, config: { damping: 15 } });
  const titleOpacity = titleProgress;
  const titleY = interpolate(titleProgress, [0, 1], [40, 0]);

  // Subtitle fade
  const subOpacity = interpolate(frame, [50, 70], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const subY = interpolate(frame, [50, 70], [20, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Green radial glow pulse
  const glowScale = interpolate(frame, [0, 180, 360], [0.8, 1.2, 0.8], {
    extrapolateRight: "clamp",
  });

  // Fade out at end
  const fadeOut = interpolate(frame, [300, 360], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: THEME.bg,
        justifyContent: "center",
        alignItems: "center",
        opacity: fadeOut,
      }}
    >
      {/* Background glow */}
      <div
        style={{
          position: "absolute",
          top: "50%",
          left: "50%",
          width: 900,
          height: 900,
          transform: `translate(-50%, -60%) scale(${glowScale})`,
          background:
            "radial-gradient(circle, rgba(26,183,89,0.12) 0%, transparent 70%)",
          pointerEvents: "none",
        }}
      />

      {/* Subtle grid lines */}
      <GridBackground frame={frame} />

      {/* Content */}
      <div style={{ textAlign: "center", zIndex: 1 }}>
        {/* Badge */}
        <div
          style={{
            opacity: badgeOpacity,
            transform: `translateY(${badgeY}px)`,
            display: "inline-block",
            fontSize: 14,
            fontWeight: 700,
            letterSpacing: 3,
            textTransform: "uppercase",
            color: THEME.green,
            background: THEME.greenDim,
            border: `1px solid rgba(26,183,89,0.2)`,
            borderRadius: 100,
            padding: "8px 24px",
            marginBottom: 32,
            fontFamily: THEME.font,
          }}
        >
          Integration Infrastructure for AI
        </div>

        {/* Title */}
        <h1
          style={{
            opacity: titleOpacity,
            transform: `translateY(${titleY}px)`,
            fontFamily: THEME.font,
            fontSize: 72,
            fontWeight: 700,
            lineHeight: 1.1,
            color: "#fff",
            maxWidth: 900,
            margin: "0 auto 32px",
          }}
        >
          The Platform AI Agents
          <br />
          Need to{" "}
          <span
            style={{
              background: `linear-gradient(135deg, ${THEME.green}, #22d46a)`,
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
            }}
          >
            Integrate
          </span>
        </h1>

        {/* Subtitle */}
        <p
          style={{
            opacity: subOpacity,
            transform: `translateY(${subY}px)`,
            fontSize: 22,
            lineHeight: 1.6,
            color: THEME.muted,
            maxWidth: 700,
            margin: "0 auto",
            fontFamily: THEME.font,
          }}
        >
          Build, test, deploy, and monitor integrations with any API.
          <br />
          One platform. Every connection.
        </p>
      </div>
    </AbsoluteFill>
  );
};

// Animated grid background
const GridBackground: React.FC<{ frame: number }> = ({ frame }) => {
  const opacity = interpolate(frame, [0, 60], [0, 0.15], {
    extrapolateRight: "clamp",
  });

  const lines = [];
  const spacing = 80;
  const count = 30;

  for (let i = 0; i < count; i++) {
    // Vertical lines
    lines.push(
      <line
        key={`v-${i}`}
        x1={i * spacing}
        y1={0}
        x2={i * spacing}
        y2={1080}
        stroke={THEME.border}
        strokeWidth={1}
      />
    );
    // Horizontal lines
    lines.push(
      <line
        key={`h-${i}`}
        x1={0}
        y1={i * spacing}
        x2={1920}
        y2={i * spacing}
        stroke={THEME.border}
        strokeWidth={1}
      />
    );
  }

  return (
    <svg
      width={1920}
      height={1080}
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        opacity,
      }}
    >
      {lines}
    </svg>
  );
};

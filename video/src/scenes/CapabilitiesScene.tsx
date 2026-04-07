import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { THEME } from "../theme";

const capabilities = [
  {
    badge: "AI Co-Pilot",
    title: "Describe it. We build it.",
    desc: "The AI reads API documentation, maps schemas, handles authentication, builds error handling, and deploys. You describe what you need in plain English.",
    color: THEME.green,
  },
  {
    badge: "Data Engine",
    title: "Unified data processing engine",
    desc: "Format-agnostic. JSON, XML, CSV, EDI. One engine processes everything using XPath, an open W3C standard. No format conversion overhead.",
    color: "rgba(56,189,248,0.9)",
  },
];

export const CapabilitiesScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const totalFrames = 20 * fps;

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
        opacity: fadeOut,
      }}
    >
      <div
        style={{
          display: "flex",
          gap: 40,
          maxWidth: 1200,
          padding: "0 60px",
        }}
      >
        {capabilities.map((cap, i) => {
          // Stagger cards: first at frame 20, second at frame 60
          const cardDelay = 20 + i * 40;
          const cardProgress = spring({
            frame: frame - cardDelay,
            fps,
            config: { damping: 14 },
          });

          // Animated border glow
          const glowIntensity = interpolate(
            Math.sin(frame * 0.04 + i * 2),
            [-1, 1],
            [0.05, 0.2]
          );

          return (
            <div
              key={i}
              style={{
                flex: 1,
                background: THEME.cardBg,
                border: `1px solid ${THEME.border}`,
                borderRadius: 20,
                padding: "48px 40px",
                opacity: cardProgress,
                transform: `translateY(${interpolate(cardProgress, [0, 1], [60, 0])}px)`,
                boxShadow: `0 0 40px rgba(26,183,89,${glowIntensity}), inset 0 1px 0 rgba(255,255,255,0.04)`,
                position: "relative",
                overflow: "hidden",
              }}
            >
              {/* Gradient accent line at top */}
              <div
                style={{
                  position: "absolute",
                  top: 0,
                  left: 0,
                  right: 0,
                  height: 2,
                  background: `linear-gradient(90deg, transparent, ${cap.color}, transparent)`,
                  opacity: cardProgress,
                }}
              />

              {/* Badge */}
              <div
                style={{
                  display: "inline-block",
                  fontSize: 12,
                  fontWeight: 700,
                  letterSpacing: 2,
                  textTransform: "uppercase",
                  color: cap.color,
                  background: `${cap.color}15`,
                  border: `1px solid ${cap.color}30`,
                  borderRadius: 100,
                  padding: "6px 16px",
                  marginBottom: 24,
                  fontFamily: THEME.font,
                }}
              >
                {cap.badge}
              </div>

              {/* Title */}
              <h3
                style={{
                  fontFamily: THEME.font,
                  fontSize: 32,
                  fontWeight: 700,
                  color: "#fff",
                  lineHeight: 1.3,
                  marginBottom: 18,
                  margin: "0 0 18px",
                }}
              >
                {cap.title}
              </h3>

              {/* Description */}
              <p
                style={{
                  fontFamily: THEME.font,
                  fontSize: 18,
                  lineHeight: 1.7,
                  color: THEME.muted,
                  margin: 0,
                }}
              >
                {cap.desc}
              </p>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { THEME } from "../theme";

export const CTAScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Logo/text spring in
  const titleProgress = spring({
    frame: frame - 10,
    fps,
    config: { damping: 12 },
  });

  const urlProgress = spring({
    frame: frame - 40,
    fps,
    config: { damping: 14 },
  });

  const ctaProgress = spring({
    frame: frame - 60,
    fps,
    config: { damping: 14 },
  });

  // Pulsing glow on CTA
  const glowPulse = interpolate(
    Math.sin(frame * 0.06),
    [-1, 1],
    [0.15, 0.4]
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: THEME.bg,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* Background glow */}
      <div
        style={{
          position: "absolute",
          top: "50%",
          left: "50%",
          width: 1000,
          height: 1000,
          transform: "translate(-50%, -50%)",
          background:
            "radial-gradient(circle, rgba(26,183,89,0.08) 0%, transparent 60%)",
          pointerEvents: "none",
        }}
      />

      <div style={{ textAlign: "center", zIndex: 1 }}>
        {/* APIANT wordmark */}
        <h1
          style={{
            fontFamily: THEME.font,
            fontSize: 80,
            fontWeight: 700,
            color: "#fff",
            letterSpacing: 8,
            margin: "0 0 24px",
            opacity: titleProgress,
            transform: `scale(${interpolate(titleProgress, [0, 1], [0.8, 1])})`,
          }}
        >
          <span
            style={{
              background: `linear-gradient(135deg, ${THEME.green}, #22d46a, ${THEME.green})`,
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
            }}
          >
            APIANT
          </span>
        </h1>

        {/* Tagline */}
        <p
          style={{
            fontFamily: THEME.font,
            fontSize: 24,
            color: THEME.muted,
            margin: "0 0 48px",
            opacity: urlProgress,
            transform: `translateY(${interpolate(urlProgress, [0, 1], [20, 0])}px)`,
          }}
        >
          Integration Infrastructure for AI
        </p>

        {/* CTA button */}
        <div
          style={{
            opacity: ctaProgress,
            transform: `translateY(${interpolate(ctaProgress, [0, 1], [20, 0])}px)`,
          }}
        >
          <div
            style={{
              display: "inline-block",
              padding: "18px 48px",
              background: `linear-gradient(160deg, #22c95e 0%, #1ab759 40%, #128a42 100%)`,
              color: "#fff",
              fontSize: 20,
              fontWeight: 700,
              borderRadius: 10,
              fontFamily: THEME.font,
              boxShadow: `0 0 ${40 * glowPulse}px rgba(26,183,89,${glowPulse}), 0 4px 16px rgba(0,0,0,0.4)`,
              border: "1px solid rgba(255,255,255,0.1)",
              letterSpacing: 0.5,
            }}
          >
            Start Building Free →
          </div>
        </div>

        {/* URL */}
        <p
          style={{
            fontFamily: THEME.font,
            fontSize: 18,
            color: THEME.faint,
            marginTop: 32,
            opacity: ctaProgress,
            letterSpacing: 1,
          }}
        >
          apiant.com
        </p>
      </div>
    </AbsoluteFill>
  );
};

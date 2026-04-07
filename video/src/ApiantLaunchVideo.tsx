import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig } from "remotion";
import { HeroScene } from "./scenes/HeroScene";
import { MeshScene } from "./scenes/MeshScene";
import { PipelineScene } from "./scenes/PipelineScene";
import { ProblemScene } from "./scenes/ProblemScene";
import { CapabilitiesScene } from "./scenes/CapabilitiesScene";
import { CTAScene } from "./scenes/CTAScene";
import { THEME } from "./theme";

export const ApiantLaunchVideo: React.FC = () => {
  const { fps } = useVideoConfig();

  // Scene timing (in seconds, converted to frames)
  const scenes = {
    hero: { from: 0, duration: 12 },         // 0-12s: Hero text + mesh bg
    problem: { from: 12, duration: 15 },      // 12-27s: The problem we solve
    pipeline: { from: 27, duration: 18 },     // 27-45s: Pipeline animation
    capabilities: { from: 45, duration: 20 }, // 45-65s: Two capabilities
    mesh: { from: 65, duration: 15 },         // 65-80s: Full mesh zoom
    cta: { from: 80, duration: 10 },          // 80-90s: CTA
  };

  return (
    <AbsoluteFill style={{ backgroundColor: THEME.bg }}>
      {/* Scene 1: Hero */}
      <Sequence
        from={scenes.hero.from * fps}
        durationInFrames={scenes.hero.duration * fps}
      >
        <HeroScene />
      </Sequence>

      {/* Scene 2: The Problem */}
      <Sequence
        from={scenes.problem.from * fps}
        durationInFrames={scenes.problem.duration * fps}
      >
        <ProblemScene />
      </Sequence>

      {/* Scene 3: Pipeline */}
      <Sequence
        from={scenes.pipeline.from * fps}
        durationInFrames={scenes.pipeline.duration * fps}
      >
        <PipelineScene />
      </Sequence>

      {/* Scene 4: Capabilities */}
      <Sequence
        from={scenes.capabilities.from * fps}
        durationInFrames={scenes.capabilities.duration * fps}
      >
        <CapabilitiesScene />
      </Sequence>

      {/* Scene 5: Mesh zoom */}
      <Sequence
        from={scenes.mesh.from * fps}
        durationInFrames={scenes.mesh.duration * fps}
      >
        <MeshScene />
      </Sequence>

      {/* Scene 6: CTA */}
      <Sequence
        from={scenes.cta.from * fps}
        durationInFrames={scenes.cta.duration * fps}
      >
        <CTAScene />
      </Sequence>
    </AbsoluteFill>
  );
};

import { Composition } from "remotion";
import { ApiantLaunchVideo } from "./ApiantLaunchVideo";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="ApiantLaunch"
        component={ApiantLaunchVideo}
        durationInFrames={90 * 30} // 90 seconds at 30fps
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="ApiantLaunch-Short"
        component={ApiantLaunchVideo}
        durationInFrames={60 * 30} // 60 seconds
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};

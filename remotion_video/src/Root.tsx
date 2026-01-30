import { Composition } from 'remotion';
import { MyComposition } from './MyComposition';

export const RemotionRoot = () => {
  return (
    <Composition
      id="MyComposition"
      component={MyComposition}
      durationInFrames={320}
      fps={30}
      width={1280}
      height={720}
    />
  );
};

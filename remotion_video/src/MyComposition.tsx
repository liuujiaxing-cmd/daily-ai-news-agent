import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { slide } from '@remotion/transitions/slide';
import { fade } from '@remotion/transitions/fade';
import { Intro } from './Scenes/Intro';
import { Problem } from './Scenes/Problem';
import { Solution } from './Scenes/Solution';
import { Features } from './Scenes/Features';
import { Outro } from './Scenes/Outro';

export const MyComposition = () => {
	return (
		<TransitionSeries>
            {/* Scene 1: Intro - 2s */}
			<TransitionSeries.Sequence durationInFrames={60}>
				<Intro />
			</TransitionSeries.Sequence>
			<TransitionSeries.Transition
				presentation={slide({ direction: 'from-right' })}
				timing={linearTiming({ durationInFrames: 10 })}
			/>

            {/* Scene 2: Problem - 2s */}
			<TransitionSeries.Sequence durationInFrames={60}>
				<Problem />
			</TransitionSeries.Sequence>
			<TransitionSeries.Transition
				presentation={slide({ direction: 'from-bottom' })}
				timing={linearTiming({ durationInFrames: 10 })}
			/>

            {/* Scene 3: Solution - 2s */}
			<TransitionSeries.Sequence durationInFrames={60}>
				<Solution />
			</TransitionSeries.Sequence>
			<TransitionSeries.Transition
				presentation={fade()}
				timing={linearTiming({ durationInFrames: 10 })}
			/>

            {/* Scene 4: Features - 3s (enough time to read) */}
			<TransitionSeries.Sequence durationInFrames={90}>
				<Features />
			</TransitionSeries.Sequence>
			<TransitionSeries.Transition
				presentation={slide({ direction: 'from-left' })}
				timing={linearTiming({ durationInFrames: 10 })}
			/>

            {/* Scene 5: Outro - 3s */}
			<TransitionSeries.Sequence durationInFrames={90}>
				<Outro />
			</TransitionSeries.Sequence>
		</TransitionSeries>
	);
};

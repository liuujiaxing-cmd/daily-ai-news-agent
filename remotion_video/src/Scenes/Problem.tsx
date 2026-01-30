import {
	AbsoluteFill,
	interpolate,
	useCurrentFrame,
    useVideoConfig,
    random
} from 'remotion';
import React from 'react';
import { THEME } from '../theme';

export const Problem = () => {
	const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    // Aggressive zoom in
    const scale = interpolate(frame, [0, 10], [0.8, 1.1], {
        extrapolateRight: 'clamp'
    });
    
    // Faster, jittery shake
    const shakeX = (random(frame) - 0.5) * 20;
    const shakeY = (random(frame + 1) - 0.5) * 20;

    const opacity = interpolate(frame, [0, 5], [0, 1]);

	return (
		<AbsoluteFill
			style={{
				backgroundColor: THEME.colors.background, // Dark background
				justifyContent: 'center',
				alignItems: 'center',
			}}
		>
            {/* Background warning flash */}
            <AbsoluteFill style={{
                backgroundColor: THEME.colors.alert,
                opacity: interpolate(frame % 10, [0, 5, 10], [0.05, 0.15, 0.05])
            }} />

			<div
				style={{
					color: THEME.colors.text.main,
					fontSize: 80,
					fontWeight: 900,
					fontFamily: THEME.fonts.main,
                    transform: `scale(${scale}) translate(${shakeX}px, ${shakeY}px)`,
                    textAlign: 'center',
                    lineHeight: 1.2,
                    opacity
				}}
			>
				TOO MUCH <span style={{ color: THEME.colors.alert }}>NOISE</span><br/>
                IN AI NEWS?
			</div>
		</AbsoluteFill>
	);
};

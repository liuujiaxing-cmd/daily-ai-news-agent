import {
	AbsoluteFill,
	interpolate,
	useCurrentFrame,
	spring,
    useVideoConfig
} from 'remotion';
import React from 'react';
import { THEME } from '../theme';

const FULL_TEXT = 'Daily AI News Agent';
const SUBTITLE = 'Intelligence, Curated Daily.';
const CHAR_FRAMES = 2; // Faster typing

export const Intro = () => {
	const frame = useCurrentFrame();
    const { fps } = useVideoConfig();
	
	const typedChars = Math.floor(frame / CHAR_FRAMES);
	const textToShow = FULL_TEXT.slice(0, typedChars);
	
    const cursorOpacity = interpolate(frame % 15, [0, 8, 15], [1, 0, 1]); // Faster blink

    // Subtitle fade in
    const subtitleOpacity = interpolate(
        frame,
        [40, 60],
        [0, 1],
        { extrapolateRight: 'clamp' }
    );
    const subtitleY = interpolate(
        frame,
        [40, 60],
        [20, 0],
        { extrapolateRight: 'clamp' }
    );

	return (
		<AbsoluteFill
			style={{
				backgroundColor: THEME.colors.background,
				justifyContent: 'center',
				alignItems: 'center',
                flexDirection: 'column',
			}}
		>
			<div
				style={{
					color: THEME.colors.primary,
					fontSize: 90,
					fontWeight: 800,
					fontFamily: THEME.fonts.main,
                    letterSpacing: '-2px',
                    marginBottom: 20,
                    textShadow: `0 0 40px ${THEME.colors.primary}40` // Glow effect
				}}
			>
				{textToShow}
                <span style={{ opacity: cursorOpacity, color: THEME.colors.secondary }}>_</span>
			</div>
            <div
                style={{
                    color: THEME.colors.text.muted,
                    fontSize: 40,
                    fontFamily: THEME.fonts.main,
                    fontWeight: 500,
                    opacity: subtitleOpacity,
                    transform: `translateY(${subtitleY}px)`
                }}
            >
                {SUBTITLE}
            </div>
		</AbsoluteFill>
	);
};

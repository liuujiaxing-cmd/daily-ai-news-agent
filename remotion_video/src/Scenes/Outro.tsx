import {
	AbsoluteFill,
	interpolate,
	useCurrentFrame,
} from 'remotion';
import React from 'react';
import { THEME } from '../theme';

export const Outro = () => {
	const frame = useCurrentFrame();

    const scale = interpolate(frame % 40, [0, 20, 40], [1, 1.05, 1]);
    const glow = interpolate(frame % 40, [0, 20, 40], [0, 20, 0]);

	return (
		<AbsoluteFill
			style={{
				backgroundColor: THEME.colors.surface,
				justifyContent: 'center',
				alignItems: 'center',
			}}
		>
			<div
				style={{
					color: THEME.colors.text.main,
					fontSize: 60,
					fontFamily: THEME.fonts.main,
                    marginBottom: 60,
                    fontWeight: 300
				}}
			>
				Start Reading Today
			</div>
            <div
                style={{
                    background: `linear-gradient(135deg, ${THEME.colors.primary}, ${THEME.colors.secondary})`,
                    color: 'white',
                    padding: '25px 80px',
                    fontSize: 50,
                    fontWeight: 'bold',
                    borderRadius: 100,
                    fontFamily: THEME.fonts.main,
                    transform: `scale(${scale})`,
                    boxShadow: `0 10px 40px ${THEME.colors.primary}${Math.round(glow + 20)}`,
                    cursor: 'pointer'
                }}
            >
                SUBSCRIBE
            </div>
		</AbsoluteFill>
	);
};

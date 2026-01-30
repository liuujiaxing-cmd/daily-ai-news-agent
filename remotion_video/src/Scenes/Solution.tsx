import {
	AbsoluteFill,
	interpolate,
	useCurrentFrame,
    spring,
    useVideoConfig
} from 'remotion';
import React from 'react';
import { THEME } from '../theme';

export const Solution = () => {
	const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    const opacity = interpolate(frame, [0, 10], [0, 1]);
    
    // Smooth spring float up
    const translateY = spring({
        frame,
        fps,
        from: 50,
        to: 0,
        config: {
            damping: 12,
        }
    });

	return (
		<AbsoluteFill
			style={{
				backgroundColor: THEME.colors.background,
				justifyContent: 'center',
				alignItems: 'center',
			}}
		>
            {/* Background gradient blob */}
            <div style={{
                position: 'absolute',
                width: 600,
                height: 600,
                borderRadius: '50%',
                background: `radial-gradient(circle, ${THEME.colors.success}20 0%, transparent 70%)`,
                filter: 'blur(40px)',
                zIndex: 0
            }} />

			<div
				style={{
					color: THEME.colors.text.main,
					fontSize: 70,
					fontWeight: 800,
					fontFamily: THEME.fonts.main,
                    opacity,
                    transform: `translateY(${translateY}px)`,
                    textAlign: 'center',
                    padding: 40,
                    zIndex: 1,
                    textShadow: '0 4px 20px rgba(0,0,0,0.5)'
				}}
			>
				WE CURATE<br/>
                <span style={{ 
                    color: THEME.colors.success,
                    backgroundImage: `linear-gradient(45deg, ${THEME.colors.success}, #4ADE80)`,
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                }}>THE SIGNAL</span><br/>
                FOR YOU
			</div>
		</AbsoluteFill>
	);
};

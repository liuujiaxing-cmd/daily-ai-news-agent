import {
	AbsoluteFill,
	interpolate,
	useCurrentFrame,
    useVideoConfig,
    spring
} from 'remotion';
import React from 'react';
import { THEME } from '../theme';

const FeatureItem = ({ text, delay, color, icon }: { text: string, delay: number, color: string, icon: string }) => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    // Spring animation for entrance
    const progress = spring({
        frame: frame - delay,
        fps,
        config: {
            damping: 15,
        }
    });
    
    const opacity = interpolate(progress, [0, 1], [0, 1]);
    const translateX = interpolate(progress, [0, 1], [-100, 0]);

    return (
        <div style={{
            opacity,
            transform: `translateX(${translateX}px)`,
            fontSize: 50,
            fontWeight: 600,
            color: THEME.colors.text.main,
            margin: '15px 0',
            fontFamily: THEME.fonts.main,
            backgroundColor: THEME.colors.surface,
            padding: '20px 40px',
            borderRadius: 16,
            boxShadow: '0 10px 30px rgba(0,0,0,0.3)',
            display: 'flex',
            alignItems: 'center',
            width: 600,
            border: `1px solid ${THEME.colors.text.muted}20`
        }}>
            <span style={{ fontSize: 60, marginRight: 30 }}>{icon}</span>
            <span style={{ 
                background: `linear-gradient(90deg, ${color}, ${color}80)`,
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent', 
                fontWeight: 800
            }}>
                {text}
            </span>
        </div>
    )
}

export const Features = () => {
	return (
		<AbsoluteFill
			style={{
				backgroundColor: THEME.colors.background,
				justifyContent: 'center',
				alignItems: 'center',
			}}
		>
            <FeatureItem text="Deep Research" delay={0} color={THEME.colors.primary} icon="🔍" />
            <FeatureItem text="Smart Summary" delay={10} color={THEME.colors.secondary} icon="📝" />
            <FeatureItem text="Fully Automated" delay={20} color={THEME.colors.accent} icon="🤖" />
		</AbsoluteFill>
	);
};

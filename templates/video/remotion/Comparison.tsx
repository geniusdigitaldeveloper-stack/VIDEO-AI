import React from "react";
import {AbsoluteFill, spring, useCurrentFrame, useVideoConfig} from "remotion";
import {theme} from "./theme";

type Props = {leftTitle: string; rightTitle: string; left: string[]; right: string[]};

// Dua kad bersebelahan: kiri (biasa) vs kanan (cadangan), item muncul berturutan.
export const Comparison: React.FC<Props> = ({leftTitle, rightTitle, left, right}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const Card = ({title, items, color, delay}: {title: string; items: string[]; color: string; delay: number}) => (
    <div style={{flex: 1, background: "#151B30", borderRadius: 40, padding: 48, borderTop: `10px solid ${color}`}}>
      <div style={{fontSize: 56, fontWeight: 900, color, marginBottom: 32}}>{title}</div>
      {items.map((t, i) => {
        const s = spring({frame: frame - delay - i * 8, fps, config: {damping: 14}});
        return <div key={i} style={{fontSize: 44, color: theme.fg, marginBottom: 24, opacity: s, transform: `translateY(${(1 - s) * 30}px)`}}>{t}</div>;
      })}
    </div>
  );
  return (
    <AbsoluteFill style={{justifyContent: "center", padding: 60, fontFamily: theme.font}}>
      <div style={{display: "flex", gap: 32}}>
        <Card title={leftTitle} items={left} color={theme.muted} delay={0} />
        <Card title={rightTitle} items={right} color={theme.accent2} delay={12} />
      </div>
    </AbsoluteFill>
  );
};

import React from "react";
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from "remotion";
import {theme} from "./theme";

type Props = {steps: string[]; stepFrames?: number};

// Langkah bernombor disambung garisan yang "dilukis"; satu langkah setiap stepFrames.
export const StepsDiagram: React.FC<Props> = ({steps, stepFrames = 24}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const gap = 260;
  return (
    <AbsoluteFill style={{justifyContent: "center", alignItems: "center", fontFamily: theme.font}}>
      <div style={{position: "relative", width: 900, height: gap * steps.length}}>
        {steps.map((s, i) => {
          const t = spring({frame: frame - i * stepFrames, fps, config: {damping: 14}});
          const line = interpolate(frame - i * stepFrames, [8, stepFrames], [0, 1], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
          return (
            <div key={i} style={{position: "absolute", top: i * gap, left: 0, opacity: t, transform: `translateX(${(1 - t) * -60}px)`, display: "flex", alignItems: "center", gap: 40}}>
              <div style={{width: 120, height: 120, borderRadius: 60, background: theme.accent, color: theme.bg, fontSize: 64, fontWeight: 900, display: "flex", alignItems: "center", justifyContent: "center"}}>{i + 1}</div>
              <div style={{fontSize: 68, fontWeight: 800, color: theme.fg}}>{s}</div>
              {i < steps.length - 1 && (
                <div style={{position: "absolute", left: 58, top: 120, width: 4, height: (gap - 120) * line, background: theme.muted}} />
              )}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

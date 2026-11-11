import React from "react";
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from "remotion";
import {theme} from "./theme";

type Props = {value: number; prefix?: string; suffix?: string; label: string; durationInFrames?: number};

// Nombor naik dari 0 ke nilai sasaran dengan easing, label di bawah.
export const Counter: React.FC<Props> = ({value, prefix = "", suffix = "", label, durationInFrames = 45}) => {
  const frame = useCurrentFrame();
  const n = interpolate(frame, [0, durationInFrames], [0, value], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  return (
    <AbsoluteFill style={{justifyContent: "center", alignItems: "center", fontFamily: theme.font}}>
      <div style={{fontSize: 240, fontWeight: 900, color: theme.accent}}>
        {prefix}{Math.round(n).toLocaleString("en-US")}{suffix}
      </div>
      <div style={{fontSize: 64, color: theme.fg, marginTop: 20, textAlign: "center", padding: "0 80px"}}>{label}</div>
    </AbsoluteFill>
  );
};

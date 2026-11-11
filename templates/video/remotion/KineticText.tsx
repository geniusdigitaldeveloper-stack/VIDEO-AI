import React from "react";
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from "remotion";
import {theme} from "./theme";

type Props = {text: string; highlight?: string[]};

// Setiap perkataan muncul berturutan dengan spring; perkataan highlight guna warna aksen.
export const KineticText: React.FC<Props> = ({text, highlight = []}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const words = text.split(" ");
  return (
    <AbsoluteFill style={{justifyContent: "center", alignItems: "center", padding: 80}}>
      <div style={{display: "flex", flexWrap: "wrap", gap: 24, justifyContent: "center"}}>
        {words.map((w, i) => {
          const s = spring({frame: frame - i * 4, fps, config: {damping: 12}});
          const op = interpolate(s, [0, 1], [0, 1]);
          const isHi = highlight.some((h) => w.toLowerCase().includes(h.toLowerCase()));
          return (
            <span
              key={i}
              style={{
                fontFamily: theme.font, fontWeight: 900, fontSize: 110,
                color: isHi ? theme.accent : theme.fg,
                opacity: op, transform: `translateY(${(1 - s) * 40}px) scale(${0.8 + 0.2 * s})`,
              }}
            >
              {w}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

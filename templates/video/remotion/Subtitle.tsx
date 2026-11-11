import React from "react";
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from "remotion";
import {loadFont as loadNormal} from "@remotion/google-fonts/Poppins";
import {subtitle} from "./theme";

// Poppins SemiBold (600), tegak untuk BM, italic untuk perkataan Inggeris.
const normal = loadNormal("normal", {weights: ["600"]});
const italic = loadNormal("italic", {weights: ["600"]});

export type Word = {text: string; start: number; end: number; en?: boolean};

// Sokong juga penanda *word* dalam teks untuk italic.
const clean = (w: Word): Word =>
  /^\*.+\*$/.test(w.text) ? {...w, text: w.text.slice(1, -1), en: true} : w;

export const Subtitle: React.FC<{words: Word[]; perLine?: number}> = ({words, perLine = 3}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const ws = words.map(clean);
  const idx = Math.max(0, ws.findIndex((w) => t >= w.start && t < w.end));
  const lineStart = Math.floor(idx / perLine) * perLine;
  const line = ws.slice(lineStart, lineStart + perLine);
  if (!ws.length || t > ws[ws.length - 1].end) return null;
  return (
    <AbsoluteFill style={{justifyContent: "flex-end", alignItems: "center", paddingBottom: subtitle.bottom}}>
      <div style={{textAlign: "center", padding: "0 60px", lineHeight: 1.25}}>
        {line.map((w, i) => (
          <span
            key={lineStart + i}
            style={{
              fontFamily: w.en ? italic.fontFamily : normal.fontFamily,
              fontWeight: subtitle.weight,
              fontStyle: w.en ? "italic" : "normal",
              fontSize: subtitle.size,
              color: subtitle.color,
              WebkitTextStroke: `${subtitle.stroke}px ${subtitle.strokeColor}`,
              paintOrder: "stroke fill",
              marginRight: 16,
            }}
          >
            {w.text}
          </span>
        ))}
      </div>
    </AbsoluteFill>
  );
};

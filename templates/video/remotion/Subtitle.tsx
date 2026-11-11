import React from "react";
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from "remotion";
import {loadFont as loadNormal} from "@remotion/google-fonts/Poppins";
import {loadFont as loadArabic} from "@remotion/google-fonts/Amiri";
import {subtitle} from "./theme";

// Poppins SemiBold (600), tegak untuk BM, italic untuk perkataan Inggeris.
const normal = loadNormal("normal", {weights: ["600"]});
const italic = loadNormal("italic", {weights: ["600"]});
// Traditional Arabic (font Microsoft) dahulu; Amiri hanya fallback jika fail tiada.
const amiri = loadArabic("normal", {weights: ["400"], subsets: ["arabic"]});
const isArabic = (t: string) => /[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]/.test(t);

export type Word = {text: string; start: number; end: number; en?: boolean; ar?: boolean};

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
        {line.map((w, i) => {
          const ar = w.ar || isArabic(w.text);
          return (
          <span
            key={lineStart + i}
            style={{
              fontFamily: ar ? `${subtitle.arabic.family}, ${amiri.fontFamily}, serif` : w.en ? italic.fontFamily : normal.fontFamily,
              fontWeight: ar ? subtitle.arabic.weight : subtitle.weight,
              fontStyle: ar ? "normal" : w.en ? "italic" : "normal",
              direction: ar ? "rtl" : "ltr",
              fontSize: ar ? subtitle.arabic.size : subtitle.size,
              color: subtitle.color,
              WebkitTextStroke: `${subtitle.stroke}px ${subtitle.strokeColor}`,
              paintOrder: "stroke fill",
              marginRight: 16,
            }}
          >
            {w.text}
          </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

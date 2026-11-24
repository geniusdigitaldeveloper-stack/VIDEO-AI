import React, {useLayoutEffect, useRef} from "react";
import {AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from "remotion";
import {loadFont as loadNormal} from "@remotion/google-fonts/Poppins";
import {loadFont as loadArabic} from "@remotion/google-fonts/Amiri";
import {subtitle} from "./theme";

// Poppins SemiBold (600), tegak untuk BM, italic untuk perkataan Inggeris.
const normal = loadNormal("normal", {weights: ["600"]});
const italic = loadNormal("italic", {weights: ["600"]});
// Traditional Arabic (font Microsoft) dahulu; Amiri hanya fallback jika fail tiada.
const amiri = loadArabic("normal", {weights: ["400"], subsets: ["arabic"]});
const isArabic = (t: string) => /[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]/.test(t);

// tone: "pos" = perkataan kunci baik (hijau), "neg" = benda buruk (merah)
export type Word = {text: string; start: number; end: number; en?: boolean; ar?: boolean; tone?: "pos" | "neg"};

// Sokong juga penanda *word* dalam teks untuk italic.
const clean = (w: Word): Word =>
  /^\*.+\*$/.test(w.text) ? {...w, text: w.text.slice(1, -1), en: true} : w;

const toneColor = (w: Word) =>
  w.tone === "pos" ? subtitle.positive : w.tone === "neg" ? subtitle.negative : subtitle.color;

// Kotak kaca silver gaya iOS: satu kotak, meluncur ke perkataan yang sedang disebut.
const PAD_X = 14, PAD_Y = 4, LEAD = 0.06, GLIDE = 0.34;
const glass: React.CSSProperties = {
  position: "absolute", left: 0, top: 0, zIndex: -1, borderRadius: 22,
  background: "linear-gradient(180deg, rgba(236,240,246,.34), rgba(170,178,190,.22))",
  backdropFilter: "blur(14px) saturate(160%)", WebkitBackdropFilter: "blur(14px) saturate(160%)",
  border: "1.5px solid rgba(232,236,244,.78)",
  boxShadow: "inset 0 1.5px 0 rgba(255,255,255,.7), inset 0 -2px 4px rgba(0,0,0,.14), 0 8px 20px rgba(0,0,0,.28)",
};

export const Subtitle: React.FC<{words: Word[]; perLine?: number}> = ({words, perLine = 3}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const ws = words.map(clean);
  const idx = Math.max(0, ws.findIndex((w) => t >= w.start && t < w.end));
  const lineStart = Math.floor(idx / perLine) * perLine;
  const line = ws.slice(lineStart, lineStart + perLine);
  const refs = useRef<(HTMLSpanElement | null)[]>([]);
  const boxRef = useRef<HTMLDivElement>(null);

  // Ukur kedudukan perkataan selepas layout, gerakkan kotak kaca (lerp lancar antara perkataan).
  useLayoutEffect(() => {
    const box = boxRef.current;
    if (!box) return;
    const geo = (i: number) => {
      const el = refs.current[i];
      return el ? {x: el.offsetLeft - PAD_X, y: el.offsetTop - PAD_Y, w: el.offsetWidth + 2 * PAD_X, h: el.offsetHeight + 2 * PAD_Y} : null;
    };
    let k = -1;
    line.forEach((w, i) => { if (t >= w.start - LEAD) k = i; });
    if (k < 0) { box.style.opacity = "0"; return; }
    const cur = geo(k);
    if (!cur) return;
    const prev = k > 0 ? geo(k - 1) : cur;
    const p = interpolate(t, [line[k].start - LEAD, line[k].start - LEAD + GLIDE], [0, 1], {
      extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic),
    });
    const L = (a: number, b: number) => a + (b - a) * (k > 0 ? p : 1);
    const lineEnd = line[line.length - 1].end;
    const fadeIn = interpolate(t, [line[0].start, line[0].start + 0.3], [0, 1], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
    const fadeOut = interpolate(t, [lineEnd - 0.15, lineEnd], [1, 0], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
    box.style.opacity = String(Math.min(fadeIn, fadeOut));
    box.style.transform = `translate(${L(prev!.x, cur.x)}px, ${L(prev!.y, cur.y)}px) scale(${0.85 + 0.15 * fadeIn})`;
    box.style.width = `${L(prev!.w, cur.w)}px`;
    box.style.height = `${L(prev!.h, cur.h)}px`;
  });

  if (!ws.length || t > ws[ws.length - 1].end) return null;
  return (
    <AbsoluteFill style={{justifyContent: "flex-end", alignItems: "center", paddingBottom: subtitle.bottom}}>
      <div style={{position: "relative", isolation: "isolate", textAlign: "center", padding: "0 60px", lineHeight: 1.25}}>
        <div ref={boxRef} style={glass} />
        {line.map((w, i) => {
          const ar = w.ar || isArabic(w.text);
          // Animasi tetap: pop per perkataan (spring) tepat masa disebut
          const f = frame - Math.round(w.start * fps);
          const p = f < 0 ? 0 : spring({frame: f, fps, config: {damping: 12, stiffness: 180, mass: 0.6}});
          return (
          <span
            key={lineStart + i}
            ref={(el) => { refs.current[i] = el; }}
            style={{
              fontFamily: ar ? `${subtitle.arabic.family}, ${amiri.fontFamily}, serif` : w.en ? italic.fontFamily : normal.fontFamily,
              fontWeight: ar ? subtitle.arabic.weight : subtitle.weight,
              fontStyle: ar ? "normal" : w.en ? "italic" : "normal",
              direction: ar ? "rtl" : "ltr",
              fontSize: ar ? subtitle.arabic.size : subtitle.size,
              color: toneColor(w),
              WebkitTextStroke: `${subtitle.stroke}px ${subtitle.strokeColor}`,
              paintOrder: "stroke fill",
              filter: "drop-shadow(0 6px 10px rgba(0,0,0,.45))",
              marginRight: 16,
              display: "inline-block",
              opacity: Math.min(1, p * 1.5),
              transform: `translateY(${(1 - p) * 18}px) scale(${0.6 + 0.4 * p})`,
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

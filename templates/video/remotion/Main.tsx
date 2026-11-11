import React from "react";
import {AbsoluteFill, Audio, Sequence, staticFile} from "remotion";
import {Comparison} from "./Comparison";
import {Counter} from "./Counter";
import {KineticText} from "./KineticText";
import {StepsDiagram} from "./StepsDiagram";
import {FPS, theme} from "./theme";
import beats from "./beats.example.json";

type Beat = {type: string; from: number; duration: number; props: any};

const render = (b: Beat) => {
  switch (b.type) {
    case "kinetic": return <KineticText {...b.props} />;
    case "counter": return <Counter {...b.props} />;
    case "steps": return <StepsDiagram {...b.props} />;
    case "comparison": return <Comparison {...b.props} />;
    default: return null;
  }
};

// Bina Sequence daripada beats.json; letak suara user di public/voice.mp3 (buang komen Audio bila ada).
export const Main: React.FC = () => (
  <AbsoluteFill style={{background: theme.bg}}>
    {/* <Audio src={staticFile("voice.mp3")} /> */}
    {(beats as Beat[]).map((b, i) => (
      <Sequence key={i} from={Math.round(b.from * FPS)} durationInFrames={Math.round(b.duration * FPS)}>
        {render(b)}
      </Sequence>
    ))}
  </AbsoluteFill>
);

export const totalFrames = (bs: Beat[]) => Math.round(Math.max(...bs.map((b) => b.from + b.duration)) * FPS);

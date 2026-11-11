import React from "react";
import {Composition} from "remotion";
import beats from "./beats.example.json";
import {Main, totalFrames} from "./Main";
import {FPS} from "./theme";

export const RemotionRoot: React.FC = () => (
  <Composition id="Main" component={Main} durationInFrames={totalFrames(beats as any)} fps={FPS} width={1080} height={1920} />
);

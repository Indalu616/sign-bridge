export type HandLandmark = {
  x: number;
  y: number;
  z?: number;
};

export type GestureLabel = 'Hello' | 'Help' | null;

function dist(a: HandLandmark, b: HandLandmark) {
  const dx = a.x - b.x;
  const dy = a.y - b.y;
  const dz = (a.z ?? 0) - (b.z ?? 0);
  return Math.sqrt(dx * dx + dy * dy + dz * dz);
}

function isFingerExtended(
  landmarks: HandLandmark[],
  mcpIndex: number,
  pipIndex: number,
  tipIndex: number,
) {
  const wrist = landmarks[0];
  const mcp = landmarks[mcpIndex];
  const pip = landmarks[pipIndex];
  const tip = landmarks[tipIndex];

  const yExtended = tip.y < pip.y;
  const radialExtended = dist(tip, wrist) > dist(mcp, wrist) * 1.15;
  return yExtended && radialExtended;
}

function isThumbExtended(landmarks: HandLandmark[]) {
  const wrist = landmarks[0];
  const mcp = landmarks[2];
  const tip = landmarks[4];

  return dist(tip, wrist) > dist(mcp, wrist) * 1.15;
}

export function recognizeGesture(landmarks: HandLandmark[]): GestureLabel {
  if (!landmarks || landmarks.length < 21) return null;

  const thumb = isThumbExtended(landmarks);
  const index = isFingerExtended(landmarks, 5, 6, 8);
  const middle = isFingerExtended(landmarks, 9, 10, 12);
  const ring = isFingerExtended(landmarks, 13, 14, 16);
  const pinky = isFingerExtended(landmarks, 17, 18, 20);

  const all = thumb && index && middle && ring && pinky;
  if (all) return 'Hello';

  const help = thumb && pinky && !index && !middle && !ring;
  if (help) return 'Help';

  return null;
}

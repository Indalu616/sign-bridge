import { useMemo } from "react";
import { StyleSheet } from "react-native";
import WebView, { WebViewMessageEvent } from "react-native-webview";

import type { HandLandmark } from "@/lib/gesture";

type Props = {
  enabled: boolean;
  onLandmarks: (landmarks: HandLandmark[]) => void;
};

export default function MediaPipeHandsWebView({ enabled, onLandmarks }: Props) {
  const html = useMemo(
    () => `<!doctype html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style>
      html, body { margin: 0; padding: 0; width: 100%; height: 100%; background: transparent; }
      video { position: fixed; inset: 0; width: 100%; height: 100%; object-fit: cover; }
      canvas { display: none; }
    </style>
  </head>
  <body>
    <video id="video" playsinline></video>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js"></script>
    <script>
      (function () {
        const post = (payload) => {
          try {
            window.ReactNativeWebView.postMessage(JSON.stringify(payload));
          } catch (e) {}
        };

        const videoElement = document.getElementById('video');

        const hands = new Hands({
          locateFile: (file) => 'https://cdn.jsdelivr.net/npm/@mediapipe/hands/' + file,
        });

        hands.setOptions({
          maxNumHands: 1,
          modelComplexity: 1,
          minDetectionConfidence: 0.6,
          minTrackingConfidence: 0.6,
        });

        hands.onResults((results) => {
          const lm = results && results.multiHandLandmarks && results.multiHandLandmarks[0];
          if (!lm) return;
          post({ type: 'landmarks', landmarks: lm });
        });

        const camera = new Camera(videoElement, {
          onFrame: async () => {
            await hands.send({ image: videoElement });
          },
          width: 720,
          height: 1280,
        });

        camera.start();
      })();
    </script>
  </body>
</html>`,
    [],
  );

  const handleMessage = (event: WebViewMessageEvent) => {
    if (!enabled) return;

    try {
      const data = JSON.parse(event.nativeEvent.data);
      if (data?.type === "landmarks" && Array.isArray(data.landmarks)) {
        onLandmarks(data.landmarks);
      }
    } catch {
      return;
    }
  };

  if (!enabled) return null;

  return (
    <WebView
      originWhitelist={["*"]}
      onMessage={handleMessage}
      source={{ html }}
      javaScriptEnabled
      allowsInlineMediaPlayback
      mediaPlaybackRequiresUserAction={false}
      style={styles.hidden}
    />
  );
}

const styles = StyleSheet.create({
  hidden: {
    position: "absolute",
    width: 1,
    height: 1,
    opacity: 0,
    left: 0,
    top: 0,
  },
});

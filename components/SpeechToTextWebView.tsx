import { useEffect, useMemo, useRef } from "react";
import { StyleSheet } from "react-native";
import WebView, { WebViewMessageEvent } from "react-native-webview";

type Props = {
  enabled: boolean;
  listening: boolean;
  onText: (text: string, isFinal: boolean) => void;
  onError?: (message: string) => void;
};

type OutgoingMessage =
  | { type: "ready"; supported: boolean }
  | { type: "stt"; text: string; isFinal: boolean }
  | { type: "error"; message: string };

type IncomingMessage = { type: "start" } | { type: "stop" };

export default function SpeechToTextWebView({
  enabled,
  listening,
  onText,
  onError,
}: Props) {
  const webViewRef = useRef<WebView>(null);

  const html = useMemo(
    () => `<!doctype html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style>
      html, body { margin: 0; padding: 0; background: transparent; }
    </style>
  </head>
  <body>
    <script>
      (function () {
        const post = (payload) => {
          try { window.ReactNativeWebView.postMessage(JSON.stringify(payload)); } catch (e) {}
        };

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const supported = !!SpeechRecognition;
        post({ type: 'ready', supported });

        let recognition = null;
        let isListening = false;

        if (supported) {
          recognition = new SpeechRecognition();
          recognition.continuous = true;
          recognition.interimResults = true;
          recognition.lang = 'en-US';

          recognition.onresult = (event) => {
            let interim = '';
            let finalText = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
              const res = event.results[i];
              const t = res && res[0] && res[0].transcript ? res[0].transcript : '';
              if (res.isFinal) finalText += t;
              else interim += t;
            }
            if (interim) post({ type: 'stt', text: interim, isFinal: false });
            if (finalText) post({ type: 'stt', text: finalText, isFinal: true });
          };

          recognition.onerror = (e) => {
            const msg = e && e.error ? String(e.error) : 'speech_error';
            post({ type: 'error', message: msg });
          };

          recognition.onend = () => {
            if (isListening) {
              try { recognition.start(); } catch (e) {}
            }
          };
        }

        const start = () => {
          if (!supported) return post({ type: 'error', message: 'speech_not_supported' });
          isListening = true;
          try { recognition.start(); } catch (e) {}
        };

        const stop = () => {
          isListening = false;
          try { recognition.stop(); } catch (e) {}
        };

        window.document.addEventListener('message', (event) => {
          try {
            const msg = JSON.parse(event.data);
            if (!msg || !msg.type) return;
            if (msg.type === 'start') start();
            if (msg.type === 'stop') stop();
          } catch (e) {}
        });

        window.addEventListener('message', (event) => {
          try {
            const msg = JSON.parse(event.data);
            if (!msg || !msg.type) return;
            if (msg.type === 'start') start();
            if (msg.type === 'stop') stop();
          } catch (e) {}
        });
      })();
    </script>
  </body>
</html>`,
    [],
  );

  useEffect(() => {
    if (!enabled) return;

    const payload: IncomingMessage = listening
      ? { type: "start" }
      : { type: "stop" };
    webViewRef.current?.postMessage(JSON.stringify(payload));
  }, [enabled, listening]);

  const handleMessage = (event: WebViewMessageEvent) => {
    if (!enabled) return;

    try {
      const msg = JSON.parse(event.nativeEvent.data) as OutgoingMessage;
      if (msg.type === "stt") onText(msg.text, msg.isFinal);
      if (msg.type === "error") onError?.(msg.message);
    } catch {
      return;
    }
  };

  if (!enabled) return null;

  return (
    <WebView
      ref={webViewRef}
      originWhitelist={["*"]}
      source={{ html }}
      onMessage={handleMessage}
      javaScriptEnabled
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

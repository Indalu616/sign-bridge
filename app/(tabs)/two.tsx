import { useMemo, useState } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";

import SpeechToTextWebView from "@/components/SpeechToTextWebView";
import { useConversation } from "@/components/ConversationContext";

export default function SpeechModeScreen() {
  const { addMessage } = useConversation();
  const [listening, setListening] = useState(false);
  const [interim, setInterim] = useState("");
  const [finalText, setFinalText] = useState("");
  const [error, setError] = useState<string | null>(null);

  const displayed = useMemo(() => {
    if (interim.trim().length > 0) return interim;
    if (finalText.trim().length > 0) return finalText;
    return "Hold to Speak";
  }, [finalText, interim]);

  return (
    <View style={styles.root} className="flex-1 bg-black">
      <SpeechToTextWebView
        enabled
        listening={listening}
        onText={(text, isFinal) => {
          setError(null);
          if (isFinal) {
            addMessage("voice", text);
            setFinalText((prev) => (prev ? prev + " " + text : text));
            setInterim("");
          } else {
            setInterim(text);
          }
        }}
        onError={(message) => {
          setError(message);
          setListening(false);
        }}
      />

      <View style={styles.content} className="flex-1 px-6 pt-12">
        <View
          style={styles.transcriptCard}
          className="rounded-2xl border border-white/20 bg-white/10 p-4"
        >
          <Text className="text-white text-3xl font-bold leading-snug">
            {displayed}
          </Text>
          {!!error && (
            <Text className="text-red-300 mt-3 text-sm">Error: {error}</Text>
          )}
        </View>
      </View>

      <View style={styles.bottom} className="px-6 pb-10">
        <Pressable
          onPressIn={() => {
            setInterim("");
            setListening(true);
          }}
          onPressOut={() => {
            setListening(false);
          }}
          style={listening ? styles.holdButtonActive : styles.holdButton}
          className={
            listening
              ? "w-full items-center justify-center rounded-3xl bg-red-500 py-6"
              : "w-full items-center justify-center rounded-3xl bg-white py-6"
          }
        >
          <Text
            className={
              listening
                ? "text-white text-xl font-extrabold"
                : "text-black text-xl font-extrabold"
            }
          >
            Hold to Speak
          </Text>
        </Pressable>

        <Pressable
          onPress={() => {
            setListening(false);
            setInterim("");
            setFinalText("");
            setError(null);
          }}
          style={styles.clearButton}
          className="mt-4 w-full items-center justify-center rounded-2xl border border-white/30 bg-black/40 py-4"
        >
          <Text className="text-white text-base font-semibold">Clear</Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  root: {
    flex: 1,
    backgroundColor: "#000",
  },
  content: {
    flex: 1,
    paddingHorizontal: 24,
    paddingTop: 48,
  },
  transcriptCard: {
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.2)",
    backgroundColor: "rgba(255,255,255,0.1)",
    padding: 16,
  },
  bottom: {
    paddingHorizontal: 24,
    paddingBottom: 40,
  },
  holdButton: {
    width: "100%",
    alignItems: "center",
    justifyContent: "center",
    borderRadius: 24,
    backgroundColor: "#fff",
    paddingVertical: 24,
  },
  holdButtonActive: {
    width: "100%",
    alignItems: "center",
    justifyContent: "center",
    borderRadius: 24,
    backgroundColor: "#ef4444",
    paddingVertical: 24,
  },
  clearButton: {
    marginTop: 16,
    width: "100%",
    alignItems: "center",
    justifyContent: "center",
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.3)",
    backgroundColor: "rgba(0,0,0,0.4)",
    paddingVertical: 16,
  },
});

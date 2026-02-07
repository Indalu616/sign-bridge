import { CameraView, useCameraPermissions } from "expo-camera";
import * as Speech from "expo-speech";
import { useEffect, useMemo, useRef, useState } from "react";
import { FlatList, Pressable, StyleSheet, Text, View } from "react-native";

import MediaPipeHandsWebView from "@/components/MediaPipeHandsWebView";
import HandSkeletonOverlay from "@/components/HandSkeletonOverlay";
import { useConversation } from "@/components/ConversationContext";
import {
  recognizeGesture,
  type GestureLabel,
  type HandLandmark,
} from "@/lib/gesture";
import { useRouter } from "expo-router";

type Mode = "TTS" | "STT";

export default function CameraTabScreen() {
  const router = useRouter();
  const { messages, addMessage } = useConversation();

  const [mode, setMode] = useState<Mode>("TTS");
  const [permission, requestPermission] = useCameraPermissions();

  const [gesture, setGesture] = useState<GestureLabel>(null);
  const [stableGesture, setStableGesture] = useState<GestureLabel>(null);
  const stableTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const lastSpokenRef = useRef<GestureLabel>(null);
  const lastLoggedRef = useRef<GestureLabel>(null);

  const nextMode = useMemo<Mode>(
    () => (mode === "TTS" ? "STT" : "TTS"),
    [mode],
  );

  const handleLandmarks = (landmarks: HandLandmark[]) => {
    const label = recognizeGesture(landmarks);
    setGesture(label);
  };

  useEffect(() => {
    if (stableTimerRef.current) {
      clearTimeout(stableTimerRef.current);
      stableTimerRef.current = null;
    }

    stableTimerRef.current = setTimeout(() => {
      setStableGesture(gesture);
    }, 1500);

    return () => {
      if (stableTimerRef.current) {
        clearTimeout(stableTimerRef.current);
        stableTimerRef.current = null;
      }
    };
  }, [gesture]);

  useEffect(() => {
    if (!stableGesture) return;
    if (lastSpokenRef.current === stableGesture) return;

    lastSpokenRef.current = stableGesture;
    Speech.stop();
    Speech.speak(stableGesture);
  }, [stableGesture]);

  useEffect(() => {
    if (!stableGesture) return;
    if (lastLoggedRef.current === stableGesture) return;

    lastLoggedRef.current = stableGesture;
    addMessage("sign", stableGesture);
  }, [addMessage, stableGesture]);

  if (!permission) {
    return (
      <View
        style={{ flex: 1, backgroundColor: "#000" }}
        className="flex-1 bg-black"
      />
    );
  }

  if (!permission.granted) {
    return (
      <View
        style={{
          flex: 1,
          alignItems: "center",
          justifyContent: "center",
          backgroundColor: "#000",
        }}
        className="flex-1 items-center justify-center bg-black px-6"
      >
        <Text className="text-white text-base text-center mb-4">
          Camera permission is required to show the preview.
        </Text>
        <Pressable
          onPress={requestPermission}
          className="bg-white/90 px-5 py-3 rounded-xl"
        >
          <Text className="text-black font-semibold">Grant permission</Text>
        </Pressable>
      </View>
    );
  }

  return (
    <View style={styles.root} className="flex-1 bg-black">
      <View style={styles.topPane} className="flex-[6] overflow-hidden">
        <CameraView
          style={StyleSheet.absoluteFillObject}
          className="absolute inset-0"
          facing="back"
        />
        <MediaPipeHandsWebView enabled onLandmarks={handleLandmarks} />
        <HandSkeletonOverlay />

        <View
          style={styles.topOverlay}
          className="absolute top-0 left-0 right-0 p-4"
        >
          <View
            style={styles.statusPill}
            className="self-start rounded-xl bg-black/60 border border-white/15 px-3 py-2"
          >
            <Text className="text-white text-base font-extrabold">
              {stableGesture ?? gesture ?? "Searching…"}
            </Text>
          </View>
        </View>
      </View>

      <View
        style={styles.bottomPane}
        className="flex-[4] border-t border-white/10"
      >
        <View style={styles.sectionHeader} className="px-4 pt-4 pb-2">
          <Text className="text-white text-lg font-extrabold">
            Conversation Log
          </Text>
        </View>

        <FlatList
          style={styles.list}
          className="flex-1 px-4"
          data={messages}
          keyExtractor={(item) => item.id}
          contentContainerStyle={{ paddingBottom: 12 }}
          renderItem={({ item }) => {
            const label = item.type === "sign" ? "[Sign]" : "[Voice]";
            const chip =
              item.type === "sign"
                ? "bg-indigo-500/25 border-indigo-300/30"
                : "bg-emerald-500/25 border-emerald-300/30";
            return (
              <View className="mb-3 rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
                <View
                  className={`self-start rounded-full border px-2.5 py-1 ${chip}`}
                >
                  <Text className="text-white text-xs font-extrabold">
                    {label}
                  </Text>
                </View>
                <Text className="text-white text-base font-semibold mt-2">
                  {item.text}
                </Text>
              </View>
            );
          }}
        />

        <View style={styles.bottomBar} className="px-4 pb-4 pt-2">
          <View className="flex-row gap-3">
            <Pressable
              onPress={() => {
                if (stableGesture) addMessage("sign", stableGesture);
              }}
              style={{
                flex: 1,
                alignItems: "center",
                justifyContent: "center",
                borderRadius: 16,
                backgroundColor: "#fff",
                paddingVertical: 16,
              }}
              className="flex-1 items-center justify-center rounded-2xl bg-white py-4"
            >
              <Text className="text-black text-base font-extrabold">Sign</Text>
            </Pressable>

            <Pressable
              onPress={() => {
                router.push("/(tabs)/two");
              }}
              style={{
                flex: 1,
                alignItems: "center",
                justifyContent: "center",
                borderRadius: 16,
                backgroundColor: "#ef4444",
                paddingVertical: 16,
              }}
              className="flex-1 items-center justify-center rounded-2xl bg-red-500 py-4"
            >
              <Text className="text-white text-base font-extrabold">Speak</Text>
            </Pressable>
          </View>

          <Pressable
            onPress={() => setMode(nextMode)}
            style={styles.switchMode}
            className="mt-3 w-full items-center justify-center rounded-2xl bg-black/60 border border-white/15 py-3"
          >
            <Text className="text-white text-sm font-semibold">
              Switch Mode (Now: {mode})
            </Text>
          </Pressable>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  root: {
    flex: 1,
    backgroundColor: "#000",
  },
  topPane: {
    flex: 6,
    overflow: "hidden",
    backgroundColor: "#000",
  },
  topOverlay: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    padding: 16,
  },
  statusPill: {
    alignSelf: "flex-start",
    borderRadius: 12,
    backgroundColor: "rgba(0,0,0,0.6)",
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.15)",
    paddingHorizontal: 12,
    paddingVertical: 8,
  },
  bottomPane: {
    flex: 4,
    borderTopWidth: 1,
    borderTopColor: "rgba(255,255,255,0.1)",
    backgroundColor: "#000",
  },
  sectionHeader: {
    paddingHorizontal: 16,
    paddingTop: 16,
    paddingBottom: 8,
  },
  list: {
    flex: 1,
    paddingHorizontal: 16,
  },
  bottomBar: {
    paddingHorizontal: 16,
    paddingBottom: 16,
    paddingTop: 8,
  },
  switchMode: {
    marginTop: 12,
    width: "100%",
    alignItems: "center",
    justifyContent: "center",
    borderRadius: 16,
    backgroundColor: "rgba(0,0,0,0.6)",
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.15)",
    paddingVertical: 12,
  },
});

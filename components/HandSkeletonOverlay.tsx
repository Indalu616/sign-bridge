import { View } from 'react-native';

export default function HandSkeletonOverlay() {
  return (
    <View pointerEvents="none" className="absolute inset-0 items-center justify-center">
      <View className="w-[78%] h-[78%] border border-white/20 rounded-3xl" />

      <View className="absolute w-3 h-3 rounded-full bg-white/30" style={{ top: '50%', left: '50%', marginLeft: -6, marginTop: -6 }} />
      <View className="absolute w-2.5 h-2.5 rounded-full bg-white/25" style={{ top: '32%', left: '42%' }} />
      <View className="absolute w-2.5 h-2.5 rounded-full bg-white/25" style={{ top: '27%', left: '50%' }} />
      <View className="absolute w-2.5 h-2.5 rounded-full bg-white/25" style={{ top: '30%', left: '58%' }} />
      <View className="absolute w-2.5 h-2.5 rounded-full bg-white/25" style={{ top: '40%', left: '36%' }} />
      <View className="absolute w-2.5 h-2.5 rounded-full bg-white/25" style={{ top: '40%', left: '64%' }} />

      <View className="absolute border border-white/10 rounded-2xl" style={{ width: '56%', height: '38%', top: '30%', left: '22%' }} />
    </View>
  );
}

import { createContext, useContext, useMemo, useState, type ReactNode } from 'react';

export type ConversationMessage = {
  id: string;
  type: 'sign' | 'voice';
  text: string;
  createdAt: number;
};

type ConversationContextValue = {
  messages: ConversationMessage[];
  addMessage: (type: ConversationMessage['type'], text: string) => void;
  clear: () => void;
};

const ConversationContext = createContext<ConversationContextValue | null>(null);

export function ConversationProvider({ children }: { children: ReactNode }) {
  const [messages, setMessages] = useState<ConversationMessage[]>([]);

  const value = useMemo<ConversationContextValue>(() => {
    return {
      messages,
      addMessage: (type, text) => {
        const trimmed = text.trim();
        if (!trimmed) return;

        setMessages((prev) => [
          {
            id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
            type,
            text: trimmed,
            createdAt: Date.now(),
          },
          ...prev,
        ]);
      },
      clear: () => setMessages([]),
    };
  }, [messages]);

  return (
    <ConversationContext.Provider value={value}>
      {children}
    </ConversationContext.Provider>
  );
}

export function useConversation() {
  const ctx = useContext(ConversationContext);
  if (!ctx) {
    throw new Error('useConversation must be used within ConversationProvider');
  }
  return ctx;
}

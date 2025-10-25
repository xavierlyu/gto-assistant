import { useState, useRef, useEffect } from "react";

export interface Message {
  id: string;
  content: string;
  role: "user" | "assistant";
  timestamp: Date;
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      content:
        "Hello! I'm your GTO Assistant. Describe a poker hand history and I'll help you analyze it and find the optimal strategy.",
      role: "assistant",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      role: "user",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    // Simulate API call
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: `I've analyzed your hand: "${userMessage.content}"\n\n**Parsed Parameters:**\n- Game Type: 6-max Cash\n- Stack Depth: 100BB\n- Preflop Actions: R3, C\n- Stacks: 100, 100\n\n**GTO Analysis:**\n- UTG should raise 3x with 15% of hands\n- BB should call with 25% of hands\n- Optimal strategy depends on position and stack depth\n\nWould you like me to fetch the detailed GTO solution from the database?`,
        role: "assistant",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 1500);
  };

  return {
    messages,
    input,
    setInput,
    isLoading,
    handleSubmit,
    messagesEndRef,
  };
}

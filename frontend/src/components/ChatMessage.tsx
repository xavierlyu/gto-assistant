import { Bot, User } from "lucide-react";

interface Message {
  id: string;
  content: string;
  role: "user" | "assistant";
  timestamp: Date;
}

interface ChatMessageProps {
  message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  return (
    <div
      className={`flex gap-4 ${
        message.role === "user" ? "justify-end" : "justify-start"
      }`}
    >
      {message.role === "assistant" && (
        <div className="flex-shrink-0 w-8 h-8 bg-gray-800 rounded-lg flex items-center justify-center">
          <Bot className="w-5 h-5 text-purple-400" />
        </div>
      )}

      <div
        className={`max-w-[80%] rounded-2xl px-5 py-4 ${
          message.role === "user"
            ? "bg-gradient-to-br from-blue-600 to-blue-700 text-white"
            : "bg-gray-900 border border-gray-800 text-gray-100"
        }`}
      >
        <div className="whitespace-pre-wrap text-sm leading-relaxed">
          {message.content}
        </div>
        <div className="text-xs text-gray-500 mt-2">
          {message.timestamp.toLocaleTimeString()}
        </div>
      </div>

      {message.role === "user" && (
        <div className="flex-shrink-0 w-8 h-8 bg-gray-800 rounded-lg flex items-center justify-center">
          <User className="w-5 h-5 text-blue-400" />
        </div>
      )}
    </div>
  );
}

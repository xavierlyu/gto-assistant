import { Send } from "lucide-react";

interface ChatInputProps {
  input: string;
  setInput: (value: string) => void;
  onSubmit: (e: React.FormEvent) => void;
  isLoading: boolean;
}

export default function ChatInput({
  input,
  setInput,
  onSubmit,
  isLoading,
}: ChatInputProps) {
  return (
    <form onSubmit={onSubmit} className="flex gap-3">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Describe your poker hand (e.g., '6-max cash, 100BB, UTG raises 3x, BB calls')"
        className="flex-1 px-5 py-4 bg-gray-900 border border-gray-800 rounded-2xl text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-all"
        disabled={isLoading}
      />
      <button
        type="submit"
        disabled={!input.trim() || isLoading}
        className="px-6 py-4 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:from-gray-800 disabled:to-gray-800 disabled:cursor-not-allowed text-white rounded-2xl transition-all flex items-center gap-2 font-medium"
      >
        <Send className="w-5 h-5" />
        Send
      </button>
    </form>
  );
}

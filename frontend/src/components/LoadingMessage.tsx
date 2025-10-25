import { Bot, Loader2 } from "lucide-react";

export default function LoadingMessage() {
  return (
    <div className="flex gap-4">
      <div className="flex-shrink-0 w-8 h-8 bg-gray-800 rounded-lg flex items-center justify-center">
        <Bot className="w-5 h-5 text-purple-400" />
      </div>
      <div className="bg-gray-900 border border-gray-800 rounded-2xl px-5 py-4">
        <div className="flex items-center gap-2">
          <Loader2 className="w-4 h-4 animate-spin text-purple-400" />
          <span className="text-sm text-gray-400">Analyzing...</span>
        </div>
      </div>
    </div>
  );
}

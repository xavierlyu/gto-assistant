import { Sparkles } from "lucide-react";

export default function ChatHeader() {
  return (
    <div className="border-b border-gray-800">
      <div className="max-w-4xl mx-auto px-6 py-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
              GTO Assistant
            </h1>
            <p className="text-sm text-gray-400">
              AI-powered poker hand analysis
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

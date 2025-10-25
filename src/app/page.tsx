"use client";

import { useChat } from "@/hooks/useChat";
import ChatHeader from "@/components/ChatHeader";
import ChatMessage from "@/components/ChatMessage";
import ChatInput from "@/components/ChatInput";
import LoadingMessage from "@/components/LoadingMessage";

export default function Home() {
  const { messages, input, setInput, isLoading, handleSubmit, messagesEndRef } =
    useChat();

  return (
    <div className="min-h-screen bg-black text-white">
      <ChatHeader />

      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="space-y-6 mb-6">
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}

          {isLoading && <LoadingMessage />}

          <div ref={messagesEndRef} />
        </div>

        <ChatInput
          input={input}
          setInput={setInput}
          onSubmit={handleSubmit}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
}

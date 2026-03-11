// import ReactMarkdown from "react-markdown";
// import { Bot, User } from "lucide-react";

// interface ChatMessageProps {
//   role: "user" | "assistant";
//   content: string;
// }

// export default function ChatMessage({ role, content }: ChatMessageProps) {
//   const isUser = role === "user";

//   return (
//     <div className={`flex gap-3 animate-fade-in ${isUser ? "flex-row-reverse" : ""}`}>
//       <div
//         className={`flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center ${
//           isUser ? "bg-secondary/20 border border-secondary/40" : "bg-primary/20 border border-primary/40"
//         }`}
//       >
//         {isUser ? (
//           <User className="w-4 h-4 text-secondary" />
//         ) : (
//           <Bot className="w-4 h-4 text-primary" />
//         )}
//       </div>
//       <div
//         className={`max-w-[75%] rounded-xl px-4 py-3 text-sm font-body ${
//           isUser
//             ? "bg-secondary/15 border border-secondary/30 text-foreground"
//             : "glass-panel text-foreground"
//         }`}
//       >
//         <div className="prose prose-sm prose-invert max-w-none">
//           <ReactMarkdown>{content}</ReactMarkdown>
//         </div>
//       </div>
//     </div>
//   );
// }
import ReactMarkdown from "react-markdown";
import { Bot, User } from "lucide-react";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
}

export default function ChatMessage({ role, content }: ChatMessageProps) {
  const isUser = role === "user";

  return (
    <div className={`flex gap-3 animate-fade-in ${isUser ? "flex-row-reverse" : ""}`}>
      <div
        className={`flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center ${
          isUser ? "bg-secondary/20 border border-secondary/40" : "bg-primary/20 border border-primary/40"
        }`}
      >
        {isUser ? (
          <User className="w-4 h-4 text-secondary" />
        ) : (
          <Bot className="w-4 h-4 text-primary" />
        )}
      </div>

      <div
        className={`max-w-[75%] rounded-xl px-4 py-3 text-sm font-body ${
          isUser
            ? "bg-secondary/15 border border-secondary/30 text-foreground"
            : "glass-panel text-foreground"
        }`}
      >
        <div className="prose prose-sm prose-invert max-w-none">
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
}
// import { useState, useRef, useEffect } from "react";
// import { Send, Upload, MessageSquare, Loader2, Database, BrainCircuit } from "lucide-react";
// import ChatMessage from "./ChatMessage";

// interface Message {
//   role: "user" | "assistant";
//   content: string;
// }

// const API_BASE = "http://127.0.0.1:8000";

// export default function ChatInterface() {
//   const [mode, setMode] = useState<"query" | "ingest">("query");
//   const [messages, setMessages] = useState<Message[]>([]);
//   const [input, setInput] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [sessionId] = useState(() => crypto.randomUUID());
//   const [file, setFile] = useState<File | null>(null);
//   const scrollRef = useRef<HTMLDivElement>(null);
//   const fileRef = useRef<HTMLInputElement>(null);

//   useEffect(() => {
//     scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
//   }, [messages]);

//   const sendQuery = async () => {
//     if (!input.trim()) return;
//     const userMsg = input.trim();
//     setInput("");
//     setMessages((m) => [...m, { role: "user", content: userMsg }]);
//     setLoading(true);

//     try {
//       const res = await fetch(`${API_BASE}/chat`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json", Accept: "application/json" },
//         body: JSON.stringify({ session_id: sessionId, message: userMsg }),
//       });
//       const data = await res.json();
//       setMessages((m) => [...m, { role: "assistant", content: data.response || data.message || JSON.stringify(data) }]);
//     } catch {
//       setMessages((m) => [...m, { role: "assistant", content: "⚠️ Failed to connect to the backend. Make sure your FastAPI server is running." }]);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const sendIngestion = async () => {
//     if (!file) return;
//     setLoading(true);
//     setMessages((m) => [...m, { role: "user", content: `📄 Uploading: ${file.name}` }]);

//     try {
//       const formData = new FormData();
//       formData.append("file", file);
//       const res = await fetch(`${API_BASE}/ingest`, { method: "POST", body: formData });
//       const data = await res.json();
//       setMessages((m) => [...m, { role: "assistant", content: data.message || "✅ File ingested successfully!" }]);
//     } catch {
//       setMessages((m) => [...m, { role: "assistant", content: "⚠️ Ingestion failed. Check your backend." }]);
//     } finally {
//       setLoading(false);
//       setFile(null);
//       if (fileRef.current) fileRef.current.value = "";
//     }
//   };

//   return (
//     <div className="w-full max-w-2xl mx-auto h-[85vh] flex flex-col glass-panel cyber-border rounded-2xl overflow-hidden animate-fade-in">
//       {/* Header */}
//       <div className="px-6 py-4 border-b border-border/50 flex items-center justify-between">
//         <div className="flex items-center gap-3">
//           <BrainCircuit className="w-6 h-6 text-primary animate-pulse-glow" />
//           <h1 className="font-display text-lg tracking-wider text-foreground text-glow-primary">
//             LaunchPAD ALTIMETRIK
//           </h1>
//         </div>

//         {/* Mode Toggle */}
//         <div className="flex bg-muted/50 rounded-lg p-1 gap-1">
//           <button
//             onClick={() => setMode("query")}
//             className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-xs font-display tracking-wide transition-all ${
//               mode === "query"
//                 ? "bg-primary/20 text-primary glow-primary"
//                 : "text-muted-foreground hover:text-foreground"
//             }`}
//           >
//             <MessageSquare className="w-3.5 h-3.5" />
//             QUERY
//           </button>
//           <button
//             onClick={() => setMode("ingest")}
//             className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-xs font-display tracking-wide transition-all ${
//               mode === "ingest"
//                 ? "bg-secondary/20 text-secondary glow-secondary"
//                 : "text-muted-foreground hover:text-foreground"
//             }`}
//           >
//             <Database className="w-3.5 h-3.5" />
//             INGEST
//           </button>
//         </div>
//       </div>

//       {/* Messages */}
//       <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 space-y-4">
//         {messages.length === 0 && (
//           <div className="flex flex-col items-center justify-center h-full text-center gap-4">
//             <div className="w-16 h-16 rounded-2xl bg-primary/10 border border-primary/30 flex items-center justify-center animate-float">
//               {mode === "query" ? (
//                 <MessageSquare className="w-8 h-8 text-primary" />
//               ) : (
//                 <Upload className="w-8 h-8 text-secondary" />
//               )}
//             </div>
//             <div>
//               <p className="font-display text-sm tracking-wider text-muted-foreground">
//                 {mode === "query" ? "ASK ANYTHING" : "UPLOAD FILES"}
//               </p>
//               <p className="text-xs text-muted-foreground/60 mt-1 font-body">
//                 {mode === "query"
//                   ? "Start a conversation with the AI"
//                   : "Ingest documents into the knowledge base"}
//               </p>
//             </div>
//           </div>
//         )}
//         {messages.map((msg, i) => (
//           <ChatMessage key={i} role={msg.role} content={msg.content} />
//         ))}
//         {loading && (
//           <div className="flex gap-3">
//             <div className="w-8 h-8 rounded-lg bg-primary/20 border border-primary/40 flex items-center justify-center">
//               <Loader2 className="w-4 h-4 text-primary animate-spin" />
//             </div>
//             <div className="glass-panel rounded-xl px-4 py-3">
//               <div className="flex gap-1">
//                 <span className="w-2 h-2 rounded-full bg-primary animate-pulse-glow" />
//                 <span className="w-2 h-2 rounded-full bg-primary animate-pulse-glow [animation-delay:0.2s]" />
//                 <span className="w-2 h-2 rounded-full bg-primary animate-pulse-glow [animation-delay:0.4s]" />
//               </div>
//             </div>
//           </div>
//         )}
//       </div>

//       {/* Input */}
//       <div className="px-6 py-4 border-t border-border/50">
//         {mode === "query" ? (
//           <div className="flex gap-3">
//             <input
//               value={input}
//               onChange={(e) => setInput(e.target.value)}
//               onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && sendQuery()}
//               placeholder="Type your message..."
//               className="flex-1 bg-muted/50 border border-border/50 rounded-xl px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:border-primary/50 focus:glow-primary transition-all font-body"
//             />
//             <button
//               onClick={sendQuery}
//               disabled={!input.trim() || loading}
//               className="bg-primary/20 hover:bg-primary/30 border border-primary/40 text-primary rounded-xl px-4 transition-all disabled:opacity-30 disabled:cursor-not-allowed glow-primary"
//             >
//               <Send className="w-4 h-4" />
//             </button>
//           </div>
//         ) : (
//           <div className="flex gap-3 items-center">
//             <input
//               ref={fileRef}
//               type="file"
//               onChange={(e) => setFile(e.target.files?.[0] || null)}
//               className="flex-1 bg-muted/50 border border-border/50 rounded-xl px-4 py-3 text-sm text-foreground file:bg-secondary/20 file:border-0 file:text-secondary file:text-xs file:font-display file:mr-3 file:px-3 file:py-1 file:rounded-md font-body"
//             />
//             <button
//               onClick={sendIngestion}
//               disabled={!file || loading}
//               className="bg-secondary/20 hover:bg-secondary/30 border border-secondary/40 text-secondary rounded-xl px-4 py-3 transition-all disabled:opacity-30 disabled:cursor-not-allowed glow-secondary"
//             >
//               <Upload className="w-4 h-4" />
//             </button>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// }
import { useState, useRef, useEffect } from "react";
import { Send, Upload, MessageSquare, Loader2, Database, BrainCircuit } from "lucide-react";
import ChatMessage from "./ChatMessage";


interface Message {
  role: "user" | "assistant";
  content: string;
}

const API_BASE = "http://127.0.0.1:8000";

export default function ChatInterface() {
  const [mode, setMode] = useState<"query" | "ingest">("query");
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(() => crypto.randomUUID());
  const [file, setFile] = useState<File | null>(null);

  const scrollRef = useRef<HTMLDivElement>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages]);

  /*
  -------------------------
  Typing Animation Function
  -------------------------
  */
  const typeMessage = async (text: string) => {
    let current = "";

    setMessages((m) => [...m, { role: "assistant", content: "" }]);

    for (let i = 0; i < text.length; i++) {
      await new Promise((r) => setTimeout(r, 15));

      current += text[i];

      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          role: "assistant",
          content: current,
        };
        return updated;
      });
    }
  };

  /*
  -------------------------
  QUERY
  -------------------------
  */
  const sendQuery = async () => {
    if (!input.trim()) return;

    const userMsg = input.trim();
    setInput("");

    setMessages((m) => [...m, { role: "user", content: userMsg }]);

    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          session_id: sessionId,
          message: userMsg,
        }),
      });

      const data = await res.json();

      const reply =
        data.answer ||
        data.response ||
        data.message ||
        "No response received.";

      await typeMessage(reply);
    } catch {
      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          content:
            "⚠️ Failed to connect to the backend. Make sure your FastAPI server is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  /*
  -------------------------
  INGESTION
  -------------------------
  */
  const sendIngestion = async () => {
    if (!file) return;

    setLoading(true);

    setMessages((m) => [
      ...m,
      { role: "user", content: `📄 Uploading: ${file.name}` },
    ]);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(`${API_BASE}/ingest`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          content: data.message || "✅ File ingested successfully!",
        },
      ]);
    } catch {
      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          content: "⚠️ Ingestion failed. Check your backend.",
        },
      ]);
    } finally {
      setLoading(false);
      setFile(null);
      if (fileRef.current) fileRef.current.value = "";
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto h-[85vh] flex flex-col glass-panel cyber-border rounded-2xl overflow-hidden animate-fade-in">

      {/* HEADER */}
      <div className="px-6 py-4 border-b border-border/50 flex items-center justify-between">
        <div className="flex items-center gap-3">
          {/* <BrainCircuit className="w-6 h-6 text-primary animate-pulse-glow" /> */}
          <img src="./fav.png" alt="LaunchPAD Logo" className="w-6 h-6 text-primary animate-pulse-glow" />
          <h1 className="font-display text-lg tracking-wider text-foreground text-glow-primary">
            LaunchPAD ALTIMETRIK
          </h1>
        </div>

        {/* MODE SWITCH */}
        <div className="flex bg-muted/50 rounded-lg p-1 gap-1">
          <button
            onClick={() => setMode("query")}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-xs font-display tracking-wide transition-all ${
              mode === "query"
                ? "bg-primary/20 text-primary glow-primary"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <MessageSquare className="w-3.5 h-3.5" />
            QUERY
          </button>

          <button
            onClick={() => setMode("ingest")}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-xs font-display tracking-wide transition-all ${
              mode === "ingest"
                ? "bg-secondary/20 text-secondary glow-secondary"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <Database className="w-3.5 h-3.5" />
            INGEST
          </button>
        </div>
      </div>

      {/* CHAT */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 space-y-4">

        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center gap-4">
            <div className="w-16 h-16 rounded-2xl bg-primary/10 border border-primary/30 flex items-center justify-center animate-float">
              {mode === "query" ? (
                <MessageSquare className="w-8 h-8 text-primary" />
              ) : (
                <Upload className="w-8 h-8 text-secondary" />
              )}
            </div>

            <div>
              <p className="font-display text-sm tracking-wider text-muted-foreground">
                {mode === "query" ? "ASK ANYTHING" : "UPLOAD FILES"}
              </p>
              <p className="text-xs text-muted-foreground/60 mt-1 font-body">
                {mode === "query"
                  ? "Start a conversation with the AI"
                  : "Ingest documents into the knowledge base"}
              </p>
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <ChatMessage key={i} role={msg.role} content={msg.content} />
        ))}

        {loading && (
          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-lg bg-primary/20 border border-primary/40 flex items-center justify-center">
              <Loader2 className="w-4 h-4 text-primary animate-spin" />
            </div>

            <div className="glass-panel rounded-xl px-4 py-3">
              <div className="flex gap-1">
                <span className="w-2 h-2 rounded-full bg-primary animate-pulse-glow" />
                <span className="w-2 h-2 rounded-full bg-primary animate-pulse-glow [animation-delay:0.2s]" />
                <span className="w-2 h-2 rounded-full bg-primary animate-pulse-glow [animation-delay:0.4s]" />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* INPUT */}
      <div className="px-6 py-4 border-t border-border/50">

        {mode === "query" ? (
          <div className="flex gap-3">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && sendQuery()}
              placeholder="Type your message..."
              className="flex-1 bg-muted/50 border border-border/50 rounded-xl px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:border-primary/50 focus:glow-primary transition-all font-body"
            />

            <button
              onClick={sendQuery}
              disabled={!input.trim() || loading}
              className="bg-primary/20 hover:bg-primary/30 border border-primary/40 text-primary rounded-xl px-4 transition-all disabled:opacity-30 disabled:cursor-not-allowed glow-primary"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <div className="flex gap-3 items-center">
            <input
              ref={fileRef}
              type="file"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="flex-1 bg-muted/50 border border-border/50 rounded-xl px-4 py-3 text-sm text-foreground file:bg-secondary/20 file:border-0 file:text-secondary file:text-xs file:font-display file:mr-3 file:px-3 file:py-1 file:rounded-md font-body"
            />

            <button
              onClick={sendIngestion}
              disabled={!file || loading}
              className="bg-secondary/20 hover:bg-secondary/30 border border-secondary/40 text-secondary rounded-xl px-4 py-3 transition-all disabled:opacity-30 disabled:cursor-not-allowed glow-secondary"
            >
              <Upload className="w-4 h-4" />
            </button>
          </div>
        )}

      </div>
    </div>
  );
}
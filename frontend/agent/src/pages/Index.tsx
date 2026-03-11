import Scene3D from "@/components/Scene3D";
import ChatInterface from "@/components/ChatInterface";

const Index = () => {
  return (
    <div className="relative min-h-screen flex items-center justify-center p-4">
      <Scene3D />
      <ChatInterface />
    </div>
  );
};

export default Index;

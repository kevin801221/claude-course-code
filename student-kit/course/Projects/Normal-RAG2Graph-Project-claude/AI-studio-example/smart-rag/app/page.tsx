'use client';

import React, { useState, useRef, useEffect } from 'react';
import {
  Upload,
  Send,
  RefreshCw,
  FileText,
  MessageSquare,
  Database,
  Trash2,
  Search,
  Loader2,
  CheckCircle2,
  File,
  ChevronRight
} from 'lucide-react';

// --- Types ---
type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
};

type Document = {
  id: string;
  name: string;
  time: string;
  status: 'Indexed' | 'Processing' | 'Failed';
};

type RetrievedChunk = {
  id: string;
  source: string;
  score: number;
  text: string;
};

type UploadState = 'idle' | 'parsing' | 'chunking' | 'vectorizing' | 'completed';

// --- Mock Data ---
const MOCK_DOCS: Document[] = [
  { id: '1', name: 'Q3_Financial_Report.pdf', time: '2 hours ago', status: 'Indexed' },
  { id: '2', name: 'Employee_Handbook_2024.docx', time: '1 day ago', status: 'Indexed' },
  { id: '3', name: 'Product_Roadmap_v2.txt', time: '3 days ago', status: 'Indexed' },
];

const MOCK_CHUNKS: RetrievedChunk[] = [
  {
    id: 'c1',
    source: 'Q3_Financial_Report.pdf',
    score: 0.92,
    text: 'The company achieved a record-breaking revenue of $45.2 million in Q3, representing a 24% year-over-year growth. This surge was primarily driven by the successful launch of the new enterprise software suite and expanded market reach in the APAC region. Operating margins also improved by 350 basis points due to cost optimization initiatives implemented earlier this year.'
  },
  {
    id: 'c2',
    source: 'Q3_Financial_Report.pdf',
    score: 0.85,
    text: 'Looking ahead to Q4, we anticipate continued momentum with projected revenues between $48M and $51M. However, we remain cautious regarding potential supply chain disruptions and macroeconomic headwinds that could impact our hardware division. Strategic investments in AI research and development will remain a top priority.'
  },
  {
    id: 'c3',
    source: 'Product_Roadmap_v2.txt',
    score: 0.78,
    text: 'Phase 3 of the roadmap focuses entirely on integrating advanced machine learning capabilities into the core platform. The primary objective is to reduce manual data entry by 80% through automated document parsing and intelligent entity extraction. Expected rollout for beta testers is late November.'
  },
  {
    id: 'c4',
    source: 'Employee_Handbook_2024.docx',
    score: 0.65,
    text: 'All employees are eligible for the annual performance bonus, provided they have been with the company for at least six months prior to the end of the fiscal year. Bonuses are calculated based on a combination of individual performance metrics and overall company profitability.'
  },
  {
    id: 'c5',
    source: 'Q3_Financial_Report.pdf',
    score: 0.61,
    text: 'Capital expenditures for the quarter totaled $4.1 million, primarily allocated to upgrading our cloud infrastructure and expanding the European data center. These investments are crucial for supporting our growing user base and ensuring high availability of our services.'
  }
];

export default function SmartRAG() {
  const [activeTab, setActiveTab] = useState<'chat' | 'documents'>('chat');
  const [messages, setMessages] = useState<Message[]>([
    { id: 'm1', role: 'assistant', content: 'Hello! I am your Smart RAG assistant. I can answer questions based on the documents you have uploaded. What would you like to know?' }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [documents, setDocuments] = useState<Document[]>(MOCK_DOCS);
  const [uploadState, setUploadState] = useState<UploadState>('idle');
  const [retrievedChunks, setRetrievedChunks] = useState<RetrievedChunk[]>([]);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const newUserMsg: Message = { id: Date.now().toString(), role: 'user', content: input };
    setMessages(prev => [...prev, newUserMsg]);
    setInput('');
    setIsTyping(true);
    
    // Simulate RAG retrieval process
    setRetrievedChunks([]); // Clear previous chunks
    
    setTimeout(() => {
      // Show retrieved chunks
      setRetrievedChunks(MOCK_CHUNKS);
      
      // Simulate LLM generation delay
      setTimeout(() => {
        setIsTyping(false);
        setMessages(prev => [...prev, { 
          id: (Date.now() + 1).toString(), 
          role: 'assistant', 
          content: 'Based on the Q3 Financial Report, the company achieved a record-breaking revenue of $45.2 million, which is a 24% year-over-year growth. This was driven by the new enterprise software suite and expansion in the APAC region.' 
        }]);
      }, 1500);
    }, 800);
  };

  const handleUpload = () => {
    if (uploadState !== 'idle') return;
    
    setUploadState('parsing');
    setTimeout(() => setUploadState('chunking'), 1200);
    setTimeout(() => setUploadState('vectorizing'), 2400);
    setTimeout(() => {
      setUploadState('completed');
      setDocuments(prev => [{
        id: Date.now().toString(),
        name: 'Market_Analysis_2025.pdf',
        time: 'Just now',
        status: 'Indexed'
      }, ...prev]);
      
      setTimeout(() => setUploadState('idle'), 2000);
    }, 3600);
  };

  const handleDeleteDoc = (id: string) => {
    setDocuments(prev => prev.filter(doc => doc.id !== id));
  };

  const truncateText = (text: string, maxLength: number) => {
    if (text.length <= maxLength) return text;
    return text.slice(0, maxLength) + '...';
  };

  return (
    <div className="flex h-screen w-full bg-slate-950 text-slate-50 font-sans overflow-hidden selection:bg-indigo-500/30">
      
      {/* LEFT PANEL: Fixed 450px */}
      <div className="w-[450px] flex-shrink-0 flex flex-col border-r border-slate-700/50 bg-slate-900/50 backdrop-blur-xl z-10">
        
        {/* Header */}
        <div className="p-6 border-b border-slate-700/50">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent tracking-tight">
            Smart RAG
          </h1>
          <p className="text-slate-400 text-sm mt-1 font-medium tracking-wide flex items-center gap-2">
            <Database className="w-4 h-4 text-indigo-400" />
            Document Q&A Engine
          </p>
        </div>

        {/* Tabs */}
        <div className="flex px-6 pt-4 border-b border-slate-700/50 gap-6">
          <button
            onClick={() => setActiveTab('chat')}
            className={`pb-3 text-sm font-medium transition-colors relative ${
              activeTab === 'chat' ? 'text-indigo-400' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <div className="flex items-center gap-2">
              <MessageSquare className="w-4 h-4" />
              Chat
            </div>
            {activeTab === 'chat' && (
              <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-500 rounded-t-full shadow-[0_0_8px_rgba(99,102,241,0.8)]" />
            )}
          </button>
          <button
            onClick={() => setActiveTab('documents')}
            className={`pb-3 text-sm font-medium transition-colors relative ${
              activeTab === 'documents' ? 'text-indigo-400' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <div className="flex items-center gap-2">
              <FileText className="w-4 h-4" />
              Documents
              <span className="bg-slate-800 text-xs py-0.5 px-2 rounded-full text-slate-300 border border-slate-700">
                {documents.length}
              </span>
            </div>
            {activeTab === 'documents' && (
              <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-500 rounded-t-full shadow-[0_0_8px_rgba(99,102,241,0.8)]" />
            )}
          </button>
        </div>

        {/* Tab Content Area */}
        <div className="flex-1 overflow-hidden relative">
          
          {/* --- CHAT TAB --- */}
          {activeTab === 'chat' && (
            <div className="absolute inset-0 flex flex-col">
              {/* Messages Area */}
              <div className="flex-1 overflow-y-auto p-6 space-y-6 [&::-webkit-scrollbar]:w-1.5 [&::-webkit-scrollbar-thumb]:bg-slate-700 [&::-webkit-scrollbar-thumb]:rounded-full">
                {messages.map((msg) => (
                  <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div
                      className={`max-w-[85%] p-4 leading-relaxed shadow-lg ${
                        msg.role === 'user'
                          ? 'bg-gradient-to-br from-indigo-500 to-blue-600 text-white rounded-2xl rounded-tr-sm'
                          : 'bg-slate-800/80 backdrop-blur-sm border border-slate-700/50 text-slate-200 rounded-2xl rounded-tl-sm'
                      }`}
                    >
                      {msg.content}
                    </div>
                  </div>
                ))}
                
                {/* Typing Indicator */}
                {isTyping && (
                  <div className="flex justify-start">
                    <div className="bg-slate-800/80 backdrop-blur-sm border border-slate-700/50 p-4 rounded-2xl rounded-tl-sm flex items-center gap-1.5 shadow-lg">
                      <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                      <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                      <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Input Area */}
              <div className="p-4 border-t border-slate-700/50 bg-slate-900/80 backdrop-blur-md">
                <form onSubmit={handleSendMessage} className="relative flex items-center">
                  <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask a question about your documents..."
                    className="w-full bg-slate-950 border border-slate-700/50 rounded-full py-3.5 pl-5 pr-14 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all shadow-inner placeholder:text-slate-500"
                  />
                  <button
                    type="submit"
                    disabled={!input.trim() || isTyping}
                    className="absolute right-2 p-2 bg-indigo-500 hover:bg-indigo-400 text-white rounded-full transition-colors disabled:opacity-50 disabled:hover:bg-indigo-500"
                  >
                    <Send className="w-4 h-4 ml-0.5" />
                  </button>
                </form>
              </div>
            </div>
          )}

          {/* --- DOCUMENTS TAB --- */}
          {activeTab === 'documents' && (
            <div className="absolute inset-0 flex flex-col overflow-y-auto p-6 [&::-webkit-scrollbar]:w-1.5 [&::-webkit-scrollbar-thumb]:bg-slate-700 [&::-webkit-scrollbar-thumb]:rounded-full">
              
              {/* Upload Button */}
              <button 
                onClick={handleUpload}
                disabled={uploadState !== 'idle'}
                className="w-full group relative overflow-hidden rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 p-[1px] transition-all hover:shadow-[0_0_20px_rgba(99,102,241,0.3)] disabled:opacity-70 disabled:cursor-not-allowed"
              >
                <div className="flex items-center justify-center gap-3 bg-slate-900/40 backdrop-blur-sm py-4 rounded-xl group-hover:bg-slate-900/20 transition-colors">
                  <Upload className="w-5 h-5 text-white" />
                  <span className="font-medium text-white tracking-wide">Upload New Document</span>
                </div>
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:animate-[shimmer_1.5s_infinite]" />
              </button>
              <p className="text-center text-xs text-slate-500 mt-3 mb-8">Supported formats: .pdf, .docx, .txt</p>

              {/* Processing State Card */}
              {uploadState !== 'idle' && (
                <div className="mb-8 bg-slate-800/60 border border-indigo-500/30 rounded-xl p-5 shadow-[0_0_15px_rgba(99,102,241,0.1)] backdrop-blur-md">
                  <div className="flex items-center gap-4 mb-4">
                    {uploadState === 'completed' ? (
                      <CheckCircle2 className="w-6 h-6 text-emerald-400" />
                    ) : (
                      <Loader2 className="w-6 h-6 text-indigo-400 animate-spin" />
                    )}
                    <div>
                      <h3 className="text-sm font-medium text-slate-200">Processing Document</h3>
                      <p className="text-xs text-slate-400">Extracting and indexing contents...</p>
                    </div>
                  </div>
                  
                  {/* Progress Steps */}
                  <div className="space-y-3 pl-2">
                    {[
                      { id: 'parsing', label: 'Parsing text content' },
                      { id: 'chunking', label: 'Chunking document' },
                      { id: 'vectorizing', label: 'Generating embeddings' }
                    ].map((step, idx) => {
                      const states = ['idle', 'parsing', 'chunking', 'vectorizing', 'completed'];
                      const currentIndex = states.indexOf(uploadState);
                      const stepIndex = states.indexOf(step.id);
                      
                      let statusColor = 'text-slate-600';
                      let icon = <div className="w-1.5 h-1.5 rounded-full bg-slate-600" />;
                      
                      if (currentIndex > stepIndex) {
                        statusColor = 'text-emerald-400';
                        icon = <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />;
                      } else if (currentIndex === stepIndex) {
                        statusColor = 'text-indigo-400';
                        icon = <Loader2 className="w-3.5 h-3.5 text-indigo-400 animate-spin" />;
                      }

                      return (
                        <div key={step.id} className={`flex items-center gap-3 text-xs ${statusColor} transition-colors duration-300`}>
                          <div className="w-4 flex justify-center">{icon}</div>
                          <span>{step.label}</span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* Document List */}
              <div className="space-y-3">
                <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-4">Indexed Documents</h3>
                {documents.map((doc) => (
                  <div 
                    key={doc.id} 
                    className="group flex items-center justify-between p-4 rounded-xl bg-slate-800/40 border border-slate-700/50 hover:bg-slate-800/80 hover:border-slate-600 transition-all cursor-default"
                  >
                    <div className="flex items-center gap-3 overflow-hidden">
                      <div className="p-2 bg-slate-900 rounded-lg text-indigo-400 group-hover:text-indigo-300 group-hover:scale-110 transition-all">
                        <File className="w-4 h-4" />
                      </div>
                      <div className="overflow-hidden">
                        <h4 className="text-sm font-medium text-slate-200 truncate">{doc.name}</h4>
                        <div className="flex items-center gap-2 mt-1">
                          <span className="text-[10px] text-slate-500">{doc.time}</span>
                          <span className="w-1 h-1 rounded-full bg-slate-700" />
                          <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                            {doc.status}
                          </span>
                        </div>
                      </div>
                    </div>
                    <button 
                      onClick={() => handleDeleteDoc(doc.id)}
                      className="p-2 text-slate-500 hover:text-red-400 hover:bg-red-400/10 rounded-lg opacity-0 group-hover:opacity-100 transition-all"
                      title="Delete document"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))}
                
                {documents.length === 0 && (
                  <div className="text-center py-10 text-slate-500 text-sm border border-dashed border-slate-700/50 rounded-xl">
                    No documents indexed yet.
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* RIGHT PANEL: Retrieved Context */}
      <div className="flex-1 flex flex-col bg-slate-950 relative overflow-hidden">
        
        {/* Subtle background decoration */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-indigo-500/5 blur-[120px] rounded-full pointer-events-none" />

        <div className="p-6 border-b border-slate-800/50 bg-slate-950/80 backdrop-blur-md z-10 flex items-center justify-between">
          <h2 className="text-lg font-medium text-slate-200 flex items-center gap-2">
            <Search className="w-5 h-5 text-indigo-400" />
            Retrieved Context
          </h2>
          {retrievedChunks.length > 0 && (
            <span className="text-xs font-medium text-slate-400 bg-slate-900 px-3 py-1 rounded-full border border-slate-800">
              Top {retrievedChunks.length} chunks
            </span>
          )}
        </div>

        <div className="flex-1 overflow-y-auto p-8 z-10 [&::-webkit-scrollbar]:w-2 [&::-webkit-scrollbar-thumb]:bg-slate-800 [&::-webkit-scrollbar-thumb]:rounded-full">
          
          {/* Empty State */}
          {retrievedChunks.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-slate-500 animate-in fade-in duration-700">
              <div className="w-20 h-20 mb-6 rounded-2xl bg-slate-900/50 border border-slate-800 flex items-center justify-center shadow-inner">
                <FileText className="w-8 h-8 text-slate-600" />
              </div>
              <p className="text-lg font-medium text-slate-400">Ask a question to see retrieved chunks here</p>
              <p className="text-sm mt-2 max-w-md text-center text-slate-600">
                The system will perform a vector search across your indexed documents and display the most relevant text snippets used to generate the answer.
              </p>
            </div>
          ) : (
            /* Retrieved Chunks List */
            <div className="max-w-4xl mx-auto space-y-6 pb-10">
              {retrievedChunks.map((chunk, idx) => (
                <div 
                  key={chunk.id} 
                  className="group relative bg-slate-800/40 backdrop-blur-md border border-slate-700/50 rounded-2xl p-6 hover:border-indigo-500/40 hover:shadow-[0_0_30px_rgba(99,102,241,0.1)] transition-all duration-500 animate-in slide-in-from-bottom-4 fade-in"
                  style={{ animationFillMode: 'both', animationDelay: `${idx * 100}ms` }}
                >
                  {/* Shimmer border effect on hover */}
                  <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-indigo-500/0 via-indigo-500/10 to-purple-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none" />
                  
                  <div className="relative z-10">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-center gap-2">
                        <div className="p-1.5 bg-slate-900 rounded text-indigo-400 border border-slate-700/50">
                          <FileText className="w-3.5 h-3.5" />
                        </div>
                        <span className="text-sm font-medium text-slate-300">{chunk.source}</span>
                      </div>
                      
                      {/* Relevance Score */}
                      <div className="flex flex-col items-end gap-1.5 w-32">
                        <div className="flex items-center gap-1.5 text-xs font-medium text-indigo-300">
                          <span>Score: {(chunk.score * 100).toFixed(1)}%</span>
                        </div>
                        <div className="w-full h-1.5 bg-slate-900 rounded-full overflow-hidden border border-slate-800">
                          <div 
                            className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full"
                            style={{ width: `${chunk.score * 100}%` }}
                          />
                        </div>
                      </div>
                    </div>
                    
                    <div className="relative">
                      <ChevronRight className="absolute -left-5 top-1 w-3 h-3 text-slate-600" />
                      <p className="text-slate-300 text-sm leading-relaxed font-light tracking-wide">
                        &quot;{truncateText(chunk.text, 200)}&quot;
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
      
    </div>
  );
}

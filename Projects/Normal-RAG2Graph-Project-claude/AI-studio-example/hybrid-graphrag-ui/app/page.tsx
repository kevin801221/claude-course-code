'use client';

import React, { useState } from 'react';
import { Upload, Send, RefreshCw, FileText, MessageSquare, Database, Trash2, CircleDashed } from 'lucide-react';

export default function HybridGraphRAG() {
  const [activeTab, setActiveTab] = useState<'chat' | 'data'>('chat');
  
  return (
    <div className="flex h-screen w-full bg-slate-950 text-slate-200 font-sans overflow-hidden selection:bg-indigo-500/30">
      {/* Left Panel */}
      <div className="w-[450px] flex flex-col border-r border-slate-700/50 bg-slate-900/40 backdrop-blur-xl z-10 relative shadow-2xl shadow-black/50">
        {/* Header */}
        <div className="p-6 pb-4 border-b border-slate-700/50">
          <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent mb-6">
            Hybrid GraphRAG
          </h1>
          
          {/* Tabs */}
          <div className="flex p-1 bg-slate-800/60 rounded-xl border border-slate-700/50 backdrop-blur-md">
            <button 
              onClick={() => setActiveTab('chat')}
              className={`flex-1 flex items-center justify-center gap-2 py-2.5 px-4 rounded-lg text-sm font-medium transition-all duration-300 ${activeTab === 'chat' ? 'bg-slate-700/80 text-white shadow-sm' : 'text-slate-400 hover:text-slate-100 hover:bg-slate-700/50'}`}
            >
              <MessageSquare size={16} />
              Chat
            </button>
            <button 
              onClick={() => setActiveTab('data')}
              className={`flex-1 flex items-center justify-center gap-2 py-2.5 px-4 rounded-lg text-sm font-medium transition-all duration-300 ${activeTab === 'data' ? 'bg-slate-700/80 text-white shadow-sm' : 'text-slate-400 hover:text-slate-100 hover:bg-slate-700/50'}`}
            >
              <Database size={16} />
              Data Index
            </button>
          </div>
        </div>

        {/* Tab Content */}
        <div className="flex-1 overflow-y-auto overflow-x-hidden relative">
          {activeTab === 'chat' ? <ChatTab /> : <DataIndexTab />}
        </div>
      </div>

      {/* Right Panel */}
      <div className="flex-1 relative bg-slate-950 flex items-center justify-center overflow-hidden">
        {/* Background ambient glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-indigo-900/10 rounded-full blur-[120px] pointer-events-none" />
        
        {/* Top Right Controls */}
        <div className="absolute top-6 right-6 flex items-center gap-3 z-20">
          <button className="group flex items-center gap-2 px-4 py-2 rounded-full bg-red-500/0 hover:bg-red-500/10 border border-transparent hover:border-red-500/30 text-red-400/30 hover:text-red-400 transition-all duration-300">
            <Trash2 size={16} className="opacity-50 group-hover:opacity-100" />
            <span className="text-sm font-medium opacity-0 group-hover:opacity-100 transition-opacity duration-300">Reset Graph</span>
          </button>
          <button className="flex items-center gap-2 px-4 py-2 rounded-full bg-slate-800/50 hover:bg-slate-700/80 border border-slate-700/50 text-slate-300 transition-all duration-300 backdrop-blur-md">
            <RefreshCw size={16} />
            <span className="text-sm font-medium">Refresh Graph</span>
          </button>
        </div>

        {/* Empty State */}
        <div className="flex flex-col items-center justify-center text-center max-w-md z-10 p-8 rounded-3xl bg-slate-900/20 border border-slate-800/50 backdrop-blur-sm">
          <div className="w-24 h-24 mb-6 rounded-full bg-slate-800/50 flex items-center justify-center border border-slate-700/50 relative">
            <CircleDashed size={40} className="text-slate-500 animate-[spin_10s_linear_infinite]" />
            <div className="absolute inset-0 rounded-full bg-indigo-500/10 blur-xl" />
          </div>
          <h2 className="text-2xl font-semibold text-slate-200 mb-3 tracking-wide">Knowledge Graph is Empty</h2>
          <p className="text-slate-400 leading-relaxed text-sm">
            Upload documents in the Data Index tab to start building your semantic knowledge graph. Entities and relationships will appear here.
          </p>
        </div>
      </div>
    </div>
  );
}

function ChatTab() {
  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 p-6 space-y-6 overflow-y-auto">
        {/* Assistant Message */}
        <div className="flex flex-col items-start max-w-[85%]">
          <div className="bg-slate-800/80 border border-slate-700/50 backdrop-blur-md text-slate-200 px-5 py-4 rounded-2xl rounded-tl-sm shadow-sm">
            <p className="text-sm leading-relaxed">Hello! I'm your GraphRAG assistant. I can help you query your indexed documents. What would you like to know?</p>
          </div>
        </div>

        {/* User Message */}
        <div className="flex flex-col items-end self-end ml-auto max-w-[85%]">
          <div className="bg-gradient-to-br from-blue-500 to-indigo-600 text-white px-5 py-4 rounded-2xl rounded-tr-sm shadow-md shadow-indigo-900/20">
            <p className="text-sm leading-relaxed">Can you explain the core concepts of GraphRAG based on the uploaded papers?</p>
          </div>
        </div>

        {/* Typing Indicator */}
        <div className="flex flex-col items-start max-w-[85%]">
          <div className="bg-slate-800/80 border border-slate-700/50 backdrop-blur-md px-5 py-4 rounded-2xl rounded-tl-sm shadow-sm flex items-center gap-1.5 h-[52px]">
            <div className="w-2 h-2 rounded-full bg-slate-500 animate-bounce" style={{ animationDelay: '0ms' }} />
            <div className="w-2 h-2 rounded-full bg-slate-500 animate-bounce" style={{ animationDelay: '150ms' }} />
            <div className="w-2 h-2 rounded-full bg-slate-500 animate-bounce" style={{ animationDelay: '300ms' }} />
          </div>
        </div>
      </div>

      {/* Input Area */}
      <div className="p-6 pt-2 bg-gradient-to-t from-slate-900 via-slate-900 to-transparent">
        <div className="relative flex items-center">
          <input 
            type="text" 
            placeholder="Ask anything about your data..." 
            className="w-full bg-slate-800/80 border border-slate-700/50 text-slate-200 placeholder:text-slate-500 text-sm rounded-full pl-6 pr-14 py-4 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all backdrop-blur-md shadow-lg shadow-black/20"
          />
          <button className="absolute right-2 w-10 h-10 flex items-center justify-center bg-indigo-500 hover:bg-indigo-400 text-white rounded-full transition-colors shadow-md">
            <Send size={18} className="ml-0.5" />
          </button>
        </div>
      </div>
    </div>
  );
}

function DataIndexTab() {
  return (
    <div className="p-6 flex flex-col gap-6">
      {/* Upload Button */}
      <button className="w-full relative group overflow-hidden rounded-2xl p-[1px]">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 opacity-80 group-hover:opacity-100 transition-opacity duration-300" />
        <div className="relative bg-slate-900/90 backdrop-blur-xl px-6 py-8 rounded-[15px] flex flex-col items-center justify-center gap-3 transition-all duration-300 group-hover:bg-slate-900/70">
          <div className="w-12 h-12 rounded-full bg-indigo-500/20 flex items-center justify-center text-indigo-400 group-hover:scale-110 transition-transform duration-300">
            <Upload size={24} />
          </div>
          <div className="text-center">
            <h3 className="text-slate-200 font-medium mb-1">Upload New Document</h3>
            <p className="text-slate-500 text-xs">PDF, TXT, MD up to 50MB</p>
          </div>
        </div>
      </button>

      {/* Processing State */}
      <div className="bg-slate-800/50 border border-indigo-500/30 rounded-xl p-4 flex items-center gap-4 relative overflow-hidden">
        <div className="absolute inset-0 bg-indigo-500/5 animate-pulse" />
        <div className="relative w-10 h-10 flex-shrink-0 flex items-center justify-center">
          <svg className="animate-spin text-indigo-500 w-8 h-8" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
        <div className="relative flex-1 min-w-0">
          <p className="text-sm font-medium text-slate-200 truncate">graphrag_architecture.pdf</p>
          <p className="text-xs text-indigo-400 mt-0.5">Extracting entities and relationships...</p>
        </div>
      </div>

      {/* Document List */}
      <div className="space-y-3">
        <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-4 px-1">Indexed Documents</h3>
        
        {[
          { name: 'attention_is_all_you_need.pdf', status: 'Indexed', date: '2 hours ago' },
          { name: 'knowledge_graphs_survey.md', status: 'Indexed', date: 'Yesterday' },
          { name: 'company_internal_wiki_export.txt', status: 'Indexed', date: '3 days ago' },
        ].map((doc, i) => (
          <div key={i} className="group flex items-center gap-4 p-3 rounded-xl bg-gradient-to-r from-slate-800/30 to-slate-800/10 border border-slate-700/30 hover:from-slate-800/80 hover:to-indigo-900/20 hover:border-slate-600/50 transition-all duration-300 cursor-pointer">
            <div className="w-10 h-10 rounded-lg bg-slate-700/50 flex items-center justify-center text-slate-400 group-hover:text-blue-400 group-hover:bg-blue-500/10 transition-colors">
              <FileText size={20} />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-slate-300 truncate group-hover:text-slate-200">{doc.name}</p>
              <div className="flex items-center gap-2 mt-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                <span className="text-xs text-slate-500">{doc.status} • {doc.date}</span>
              </div>
            </div>
            <button className="p-2 text-slate-500 hover:text-red-400 hover:bg-red-500/10 rounded-lg opacity-0 group-hover:opacity-100 transition-all">
              <Trash2 size={16} />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

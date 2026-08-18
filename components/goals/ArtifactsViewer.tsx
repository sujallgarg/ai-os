"use client";

import React from "react";
import { FileText, Download, Code, ExternalLink, Image as ImageIcon, Database } from "lucide-react";
import { Button } from "@/components/ui/Button";

export interface ArtifactsViewerProps {
  artifacts?: {
    id: string;
    name: string;
    type: 'file' | 'report' | 'code' | 'url' | 'data';
    url?: string;
    content?: string;
    size?: string;
  }[];
}

export function ArtifactsViewer({ artifacts = [] }: ArtifactsViewerProps) {
  if (artifacts.length === 0) {
    return (
      <div className="p-6 text-center text-xs text-slate-400 bg-slate-50 border border-slate-100 rounded-2xl">
        No artifacts or output assets generated yet for this goal.
      </div>
    );
  }

  const getIcon = (type: string) => {
    switch (type) {
      case "code":
        return <Code className="w-4 h-4 text-violet-600" />;
      case "file":
        return <ImageIcon className="w-4 h-4 text-blue-600" />;
      case "data":
        return <Database className="w-4 h-4 text-emerald-600" />;
      case "report":
      default:
        return <FileText className="w-4 h-4 text-primary-600" />;
    }
  };

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
      {artifacts.map((art) => (
        <div
          key={art.id}
          className="flex items-center justify-between p-3.5 bg-white border border-slate-200/80 rounded-2xl shadow-subtle hover:shadow-card transition-all"
        >
          <div className="flex items-center gap-3 min-w-0">
            <div className="w-9 h-9 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-center flex-shrink-0">
              {getIcon(art.type)}
            </div>
            <div className="min-w-0">
              <span className="text-xs font-semibold text-slate-800 truncate block">
                {art.name}
              </span>
              <span className="text-[10px] text-slate-400 font-mono">
                {art.size || "Generated artifact"}
              </span>
            </div>
          </div>
          <Button
            size="sm"
            variant="ghost"
            className="h-8 w-8 p-0 flex-shrink-0"
            title="Download / View Artifact"
            onClick={() => alert(`Viewing artifact ${art.name}`)}
          >
            <Download className="w-3.5 h-3.5 text-slate-400 hover:text-slate-700" />
          </Button>
        </div>
      ))}
    </div>
  );
}

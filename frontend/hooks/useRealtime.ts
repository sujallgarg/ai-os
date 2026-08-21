"use client";

import { useEffect, useState, useRef } from "react";

export interface RealtimeEvent {
  event: string;
  job_id?: string;
  progress?: number;
  data?: any;
  timestamp?: string;
}

export function useRealtime(jobId?: string) {
  const [events, setEvents] = useState<RealtimeEvent[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const wsUrl = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws";

    let ws: WebSocket;

    try {
      ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        setIsConnected(true);
      };

      ws.onmessage = (event) => {
        try {
          const parsed: RealtimeEvent = JSON.parse(event.data);

          if (jobId && parsed.job_id && parsed.job_id !== jobId) {
            return;
          }

          setEvents((prev) => [parsed, ...prev.slice(0, 49)]);
        } catch {
          // Fallback for non-JSON frame
        }
      };

      ws.onclose = () => {
        setIsConnected(false);
      };

      ws.onerror = () => {
        setIsConnected(false);
      };
    } catch (e) {
      setIsConnected(false);
    }

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [jobId]);

  return { events, isConnected };
}

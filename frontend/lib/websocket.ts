import { io, Socket } from "socket.io-client";

const WS_URL =
  process.env.NEXT_PUBLIC_WS_URL?.replace(/\/$/, "") ||
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ||
  "http://localhost:8000";

class WebSocketClient {
  private socket: Socket | null = null;

  connect() {
    if (this.socket?.connected) {
      return;
    }

    this.socket = io(WS_URL, {
      path: "/socket.io",
      transports: ["websocket", "polling"],
    });
  }

  disconnect() {
    this.socket?.disconnect();
    this.socket = null;
  }

  on(event: string, callback: (data: unknown) => void) {
    this.socket?.on(event, callback);
  }
}

export const wsClient = new WebSocketClient();

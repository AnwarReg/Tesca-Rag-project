import { useAuth } from "@clerk/clerk-react";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export interface DocumentOut {
  id: number;
  filename: string;
  created_at: string;
}

export interface QueryResponse {
  answer: string;
  sources: string[];
}

/**
 * Hook that returns API calls pre-wired with the caller's Clerk JWT.
 * Every request attaches `Authorization: Bearer <token>`, which the backend
 * validates to identify the user and scope their data.
 */
export function useApi() {
  const { getToken } = useAuth();

  async function request(path: string, options: RequestInit = {}): Promise<Response> {
    const token = await getToken();
    const res = await fetch(`${API_URL}${path}`, {
      ...options,
      headers: { ...options.headers, Authorization: `Bearer ${token}` },
    });
    if (!res.ok) {
      throw new Error(`${res.status}: ${await res.text()}`);
    }
    return res;
  }

  return {
    listDocuments: async (): Promise<DocumentOut[]> =>
      (await request("/documents")).json(),

    uploadDocument: async (file: File): Promise<DocumentOut> => {
      const form = new FormData();
      form.append("file", file);
      // Note: no Content-Type header — the browser sets the multipart boundary.
      return (await request("/documents", { method: "POST", body: form })).json();
    },

    query: async (question: string): Promise<QueryResponse> =>
      (
        await request("/query", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question }),
        })
      ).json(),
  };
}

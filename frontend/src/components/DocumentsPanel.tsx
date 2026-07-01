import { useEffect, useState } from "react";
import { useApi, type DocumentOut } from "../lib/api";

export default function DocumentsPanel() {
  const api = useApi();
  const [docs, setDocs] = useState<DocumentOut[]>([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function refresh() {
    try {
      setDocs(await api.listDocuments());
    } catch (e) {
      setError(String(e));
    }
  }

  useEffect(() => {
    refresh();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function onUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    setError(null);
    try {
      await api.uploadDocument(file);
      await refresh();
    } catch (e) {
      setError(String(e));
    } finally {
      setUploading(false);
      e.target.value = "";
    }
  }

  return (
    <section className="rounded-lg bg-white p-5 shadow">
      <h2 className="mb-4 text-lg font-semibold text-gray-800">Documents</h2>

      <label className="mb-4 inline-block cursor-pointer rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700">
        {uploading ? "Uploading…" : "Upload PDF"}
        <input
          type="file"
          accept="application/pdf"
          className="hidden"
          onChange={onUpload}
          disabled={uploading}
        />
      </label>

      {error && <p className="mb-3 text-sm text-red-600">{error}</p>}

      {docs.length === 0 ? (
        <p className="text-sm text-gray-500">No documents yet.</p>
      ) : (
        <ul className="divide-y divide-gray-100">
          {docs.map((doc) => (
            <li key={doc.id} className="py-2 text-sm text-gray-700">
              {doc.filename}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

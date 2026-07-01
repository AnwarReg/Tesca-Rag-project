import { UserButton } from "@clerk/clerk-react";
import DocumentsPanel from "../components/DocumentsPanel";
import QueryPanel from "../components/QueryPanel";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="flex items-center justify-between bg-white px-6 py-4 shadow">
        <h1 className="text-xl font-semibold text-gray-800">
          Tesca — Industrial Docs
        </h1>
        <UserButton />
      </header>

      <main className="mx-auto grid max-w-6xl gap-6 p-6 md:grid-cols-2">
        <DocumentsPanel />
        <QueryPanel />
      </main>
    </div>
  );
}

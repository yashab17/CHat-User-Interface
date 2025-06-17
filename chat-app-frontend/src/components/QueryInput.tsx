import React, { useState } from "react";

interface Props {
  videoUrl: string | null;
  setAnswer: (answer: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setAnswerTimestamp: (time: number | null) => void;
}

const QueryInput: React.FC<Props> = ({
  videoUrl,
  setAnswer,
  setLoading,
  setError,
  setAnswerTimestamp,
}) => {
  const [query, setQuery] = useState("");
  const [localLoading, setLocalLoading] = useState(false);
  const [localError, setLocalError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!videoUrl) {
      setLocalError("Please upload a video first.");
      return;
    }

    if (!query.trim()) {
      setLocalError("Please enter a question.");
      return;
    }

    setLoading(true);
    setLocalLoading(true);
    setLocalError(null);
    setError(null);
    setAnswer("");
    setAnswerTimestamp(null);

    try {
      const response = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          video_url: videoUrl,
          question: query,
        }),
      });

      if (!response.ok) {
        throw new Error("API error");
      }

      const data = await response.json();

      setAnswer(data.answer);
      setAnswerTimestamp(data.timestamp);

      // Scroll to answer box
      setTimeout(() => {
        const answerBox = document.getElementById("answer-box");
        if (answerBox) {
          const yOffset = -80;
          const y = answerBox.getBoundingClientRect().top + window.pageYOffset + yOffset;
          window.scrollTo({ top: y, behavior: "smooth" });
        }
      }, 100);
    } catch (err) {
      console.error("API error:", err);
      setLocalError("Something went wrong. Please try again.");
      setError("Something went wrong. Please try again.");
      setAnswerTimestamp(null);
    } finally {
      setLoading(false);
      setLocalLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSubmit();
    }
  };

  return (
    <div className="my-4 max-w-md mx-auto">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask a question"
        className="border px-2 py-1 mb-2 max-w-sm w-full md:w-[74%] text-sm rounded border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-300"
        disabled={localLoading}
      />
      <button
        onClick={handleSubmit}
        disabled={localLoading}
        className={`py-1 text-white font-semibold rounded-md transition text-sm ${
          localLoading ? "bg-gray-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"
        } ml-auto md:ml-4 md:w-[22%]`}
      >
        {localLoading ? "Searching..." : "Search"}
      </button>

      {localError && <p className="text-red-600 mt-2 text-sm">{localError}</p>}
    </div>
  );
};

export default QueryInput;

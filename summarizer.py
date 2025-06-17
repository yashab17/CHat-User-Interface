from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import os

class TranscriptSummarizer:
    def summarize(self, transcript_folder, output_folder, num_keywords=10):
        os.makedirs(output_folder, exist_ok=True)

        for file in os.listdir(transcript_folder):
            if file.endswith(".txt"):
                transcript_path = os.path.join(transcript_folder, file)
                with open(transcript_path, "r", encoding="utf-8") as f:
                    text = f.read()

                # ✅ Simple extractive summary: take first 3 sentences
                sentences = text.split('. ')
                summary = '. '.join(sentences[:3]) + '.' if len(sentences) >= 3 else text

                # ✅ Keyword extraction using TF-IDF
                tfidf = TfidfVectorizer(stop_words='english', max_features=1000)
                X = tfidf.fit_transform([text])
                feature_array = np.array(tfidf.get_feature_names_out())
                tfidf_sorting = np.argsort(X.toarray()).flatten()[::-1]
                top_keywords = feature_array[tfidf_sorting][:num_keywords]

                # ✅ Save summary and keywords
                output_path = os.path.join(output_folder, file.replace(".txt", "_summary_keywords.txt"))
                with open(output_path, "w", encoding="utf-8") as out:
                    out.write(f"Summary:\n{summary}\n\n")
                    out.write("Top Keywords:\n" + ', '.join(top_keywords))

                print(f"✅ Summary and keywords saved: {output_path}")

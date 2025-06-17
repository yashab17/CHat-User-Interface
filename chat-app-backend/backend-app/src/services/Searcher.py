import json
from IPython.display import Image as IPyImage, display
from utils import extract_frame_time_from_filename

class MultimodalSearcher:
    def __init__(self, qdrant_handler, embedder, collection_name):
        self.qdrant = qdrant_handler
        self.embedder = embedder
        self.collection_name = collection_name

    def search(self, query, top_k=5, min_score=0.7):
        """
        Perform a multimodal search:
        - Finds the top text nodes
        - Finds image frames from the same video closest in time
        """
        results_final={}
        valid_images=[]

        query_vec = self.embedder.embed_text(query)
        results = self.qdrant.search(query_vec, top_k=top_k)

        text_results = []
        image_results = []

        for res in results:
            payload = res.payload
            content = json.loads(payload.get("_node_content", "{}"))
            node_type = payload.get("type")

            if node_type == "text":
                text_results.append({
                    "text": content.get("text", ""),
                    "timestamp": float(payload.get("timestamp", 0)),
                    "video_id": payload.get("video_id", "unknown"),
                    "score": res.score
                })

            elif node_type == "image":
                image_path = content.get("image", payload.get("image_path", ""))
                frame = payload.get("source", "")
                ts_guess = extract_frame_time_from_filename(frame)
                image_results.append({
                    "path": image_path,
                    "frame": frame,
                    "video_id": payload.get("video_id", "unknown"),
                    "timestamp_guess": ts_guess
                })

        valid_text = [t for t in text_results if t["score"] >= min_score]
        valid_text = sorted(valid_text, key=lambda x: -x["score"])

        if not valid_text:
            print(f"❌ No relevant results found for: \"{query}\" (score < {min_score})")
            return  

        for text_node in valid_text[:top_k]:
            video_id = text_node["video_id"]
            text_ts = text_node["timestamp"]
            score = text_node["score"]

            # Find closest image in same video
            same_video_images = [img for img in image_results if img["video_id"] == video_id]
            closest_image = min(same_video_images, key=lambda img: abs(img["timestamp_guess"] - text_ts), default=None)

            print(f"[📝 TEXT] (Video: {video_id}, Time: {text_ts:.2f}s, Score: {score:.4f})")
            print(text_node["text"])

        
            

            if closest_image and closest_image["path"]:
                print(f"[🖼️ IMAGE] (~{closest_image['timestamp_guess']:.2f}s): {closest_image['frame']}")
                display(IPyImage(closest_image["path"]))
                valid_images.append(closest_image)
            else:
                print("⚠️ No matching image found or image path missing.")

            print("—" * 60)
        results_final = {"text": valid_text[:top_k], "images": valid_images}

        return results_final
    


#     result_entry = {
        #     "video_id": video_id,
        #     "text_timestamp": text_ts,
        #     "text_score": score,
        #     "text": text_node["text"],
        #     "image_timestamp": closest_image["timestamp_guess"] if closest_image else None,
        #     "image_frame": closest_image["frame"] if closest_image else None,
        #     "image_path": closest_image["path"] if closest_image else None
        # }

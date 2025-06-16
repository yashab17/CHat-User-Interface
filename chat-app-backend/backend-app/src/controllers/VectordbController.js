exports.storeInVectorDB = async (req, res) => {
  const { embeddings } = req.body;
  // Connect to Qdrant/Milvus and upsert vectors
  res.send("Stored in vector database.");
};

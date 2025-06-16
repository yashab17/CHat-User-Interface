exports.generateEmbeddings = async (req, res) => {
  const { textChunks, imagePaths } = req.body;
  // Use CLIP or similar model to embed both
  res.send("Embeddings generated.");
};

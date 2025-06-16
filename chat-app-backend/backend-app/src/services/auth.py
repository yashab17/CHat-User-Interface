from fastapi import Header, HTTPException, status, Depends

API_KEY = "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"
  # Store securely in env/config in production

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
import os
import sys
import uvicorn

if __name__ == "__main__":
    # Debug: Print environment variables
    print("=== DEBUG INFO ===")
    print(f"All environment variables: {dict(os.environ)}")
    print(f"PORT from environment: {os.environ.get('PORT', 'NOT_SET')}")
    
    # Get port with fallback
    try:
        port = int(os.environ.get("PORT", 8000))
        print(f"Using port: {port}")
    except ValueError as e:
        print(f"Error parsing PORT: {e}")
        port = 8000
        print(f"Using default port: {port}")
    
    print("=== STARTING APP ===")
    
    # Start the application
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, log_level="info") 
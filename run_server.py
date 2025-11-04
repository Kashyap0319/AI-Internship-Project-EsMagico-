import uvicorn
import os

if __name__ == "__main__":
    os.chdir(r"C:\Users\Shrey\OneDrive\Desktop\Day 2 Ai Project")
    print("=" * 60)
    print("STARTING BACKEND ON PORT 9000")
    print("=" * 60)
    uvicorn.run(
        "backend:app",
        host="0.0.0.0",
        port=9000,
        reload=False,
        log_level="info"
    )

"""
Debug backend startup to catch hidden errors
"""
import traceback
import sys

try:
    print("=" * 60)
    print("DEBUG: Importing backend module...")
    print("=" * 60)
    
    import backend
    
    print("\n✅ Backend module imported successfully")
    print("=" * 60)
    print("DEBUG: Checking FastAPI app...")
    print("=" * 60)
    
    app = backend.app
    print(f"✅ FastAPI app exists: {app}")
    print(f"✅ App routes: {len(app.routes)} routes")
    
    print("\n" + "=" * 60)
    print("DEBUG: Starting uvicorn server...")
    print("=" * 60)
    
    import uvicorn
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=9000,
        reload=False,
        log_level="debug"
    )
    
except Exception as e:
    print("\n" + "!" * 60)
    print("❌ ERROR CAUGHT:")
    print("!" * 60)
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {str(e)}")
    print("\nFull Traceback:")
    traceback.print_exc()
    print("!" * 60)
    sys.exit(1)

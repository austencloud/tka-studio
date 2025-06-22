# Phase 1: Complete REST API - Unify Desktop and Web

## Objective

Complete your REST API layer so both the PyQt desktop app and SvelteKit web app can share the same backend, eliminating duplicate business logic and enabling real-time features.

## Current State Analysis

### What You Already Have

- **API Foundation**: `modern/src/infrastructure/api/` structure exists
- **API Server**: `modern/main.py` starts API server with `_start_api_server()`
- **API Integration**: `modern/src/infrastructure/api/api_integration.py` handles startup
- **Domain Models**: Immutable dataclasses in `modern/src/domain/models/core_models.py`
- **DI Container**: `modern/src/core/dependency_injection/di_container.py`

### What Needs Completion

- **API Endpoints**: Complete CRUD operations for sequences, beats, settings
- **Desktop Integration**: Desktop saves/loads via API instead of JSON files
- **Web Integration**: SvelteKit connects to API
- **Error Handling**: Proper HTTP responses and fallbacks

## Implementation Tasks

### Task 1: Complete API Endpoints (Week 1-2)

#### 1.1 Sequence Endpoints

```python
# File: modern/src/infrastructure/api/endpoints/sequences.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from modern.src.core.dependency_injection.di_container import get_container
from modern.src.domain.models.core_models import SequenceData, BeatData

router = APIRouter(prefix="/api/sequences", tags=["sequences"])

# Simple request/response models
class CreateSequenceRequest(BaseModel):
    name: str
    beats: List[Dict[str, Any]] = []
    start_position: Optional[str] = None
    metadata: Dict[str, Any] = {}

class SequenceResponse(BaseModel):
    id: str
    name: str
    word: str
    beats: List[Dict[str, Any]]
    length: int
    total_duration: float
    metadata: Dict[str, Any]

def get_json_manager():
    """Get JSON manager from DI container."""
    container = get_container()
    # Use your existing JsonManager interface
    from modern.src.legacy_settings_manager.global_settings.app_context import AppContext
    return AppContext.json_manager

@router.get("/", response_model=List[SequenceResponse])
async def get_sequences() -> List[SequenceResponse]:
    """Get all sequences."""
    try:
        json_manager = get_json_manager()
        # Use your existing method to get sequences
        sequences_data = json_manager.get_all_sequences()  # Implement this

        responses = []
        for seq_data in sequences_data:
            # Convert to response format
            sequence = SequenceData.from_dict(seq_data)
            response = SequenceResponse(
                id=sequence.id,
                name=sequence.name,
                word=sequence.word,
                beats=[beat.to_dict() for beat in sequence.beats],
                length=sequence.length,
                total_duration=sequence.total_duration,
                metadata=sequence.metadata
            )
            responses.append(response)

        return responses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{sequence_id}", response_model=SequenceResponse)
async def get_sequence(sequence_id: str) -> SequenceResponse:
    """Get specific sequence."""
    try:
        json_manager = get_json_manager()
        seq_data = json_manager.load_sequence(sequence_id)  # Use your existing method

        if not seq_data:
            raise HTTPException(status_code=404, detail="Sequence not found")

        sequence = SequenceData.from_dict(seq_data)
        return SequenceResponse(
            id=sequence.id,
            name=sequence.name,
            word=sequence.word,
            beats=[beat.to_dict() for beat in sequence.beats],
            length=sequence.length,
            total_duration=sequence.total_duration,
            metadata=sequence.metadata
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=SequenceResponse)
async def create_sequence(request: CreateSequenceRequest) -> SequenceResponse:
    """Create new sequence."""
    try:
        # Convert request to domain model
        beats = [BeatData.from_dict(beat_dict) for beat_dict in request.beats]
        sequence = SequenceData(
            name=request.name,
            beats=beats,
            start_position=request.start_position,
            metadata=request.metadata
        )

        # Save using existing JSON manager
        json_manager = get_json_manager()
        success = json_manager.save_sequence(sequence.to_dict())

        if not success:
            raise HTTPException(status_code=500, detail="Failed to save sequence")

        return SequenceResponse(
            id=sequence.id,
            name=sequence.name,
            word=sequence.word,
            beats=[beat.to_dict() for beat in sequence.beats],
            length=sequence.length,
            total_duration=sequence.total_duration,
            metadata=sequence.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{sequence_id}", response_model=SequenceResponse)
async def update_sequence(sequence_id: str, request: CreateSequenceRequest) -> SequenceResponse:
    """Update existing sequence."""
    try:
        json_manager = get_json_manager()

        # Check if sequence exists
        existing = json_manager.load_sequence(sequence_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Sequence not found")

        # Create updated sequence
        beats = [BeatData.from_dict(beat_dict) for beat_dict in request.beats]
        sequence = SequenceData(
            id=sequence_id,  # Keep existing ID
            name=request.name,
            beats=beats,
            start_position=request.start_position,
            metadata=request.metadata
        )

        # Save updated sequence
        success = json_manager.save_sequence(sequence.to_dict())
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update sequence")

        return SequenceResponse(
            id=sequence.id,
            name=sequence.name,
            word=sequence.word,
            beats=[beat.to_dict() for beat in sequence.beats],
            length=sequence.length,
            total_duration=sequence.total_duration,
            metadata=sequence.metadata
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{sequence_id}")
async def delete_sequence(sequence_id: str) -> dict:
    """Delete sequence."""
    try:
        json_manager = get_json_manager()
        success = json_manager.delete_sequence(sequence_id)  # Implement this

        if not success:
            raise HTTPException(status_code=404, detail="Sequence not found")

        return {"message": "Sequence deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### 1.2 Settings Endpoints

```python
# File: modern/src/infrastructure/api/endpoints/settings.py
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from pydantic import BaseModel
from modern.src.core.dependency_injection.di_container import get_container

router = APIRouter(prefix="/api/settings", tags=["settings"])

class SettingsResponse(BaseModel):
    settings: Dict[str, Any]

class UpdateSettingsRequest(BaseModel):
    settings: Dict[str, Any]

def get_settings_manager():
    """Get settings manager from DI container."""
    container = get_container()
    from modern.src.core.interfaces.core_services import IUIStateManagementService
    return container.resolve(IUIStateManagementService)

@router.get("/", response_model=SettingsResponse)
async def get_settings() -> SettingsResponse:
    """Get all user settings."""
    try:
        settings_manager = get_settings_manager()
        all_settings = settings_manager.get_all_settings()
        return SettingsResponse(settings=all_settings)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{key}")
async def get_setting(key: str) -> Dict[str, Any]:
    """Get specific setting."""
    try:
        settings_manager = get_settings_manager()
        value = settings_manager.get_setting(key)
        return {"key": key, "value": value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{key}")
async def update_setting(key: str, value: Dict[str, Any]) -> Dict[str, Any]:
    """Update specific setting."""
    try:
        settings_manager = get_settings_manager()
        settings_manager.set_setting(key, value["value"])
        return {"key": key, "value": value["value"], "message": "Setting updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/backgrounds/available")
async def get_available_backgrounds() -> Dict[str, Any]:
    """Get list of available background types."""
    backgrounds = ["Aurora", "Starfield", "Gradient", "Solid"]
    return {"backgrounds": backgrounds}
```

#### 1.3 Health and Info Endpoints

```python
# File: modern/src/infrastructure/api/endpoints/health.py
from fastapi import APIRouter
from datetime import datetime
import platform
import sys

router = APIRouter(prefix="/api", tags=["health"])

@router.get("/health")
async def health_check() -> dict:
    """API health check."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@router.get("/info")
async def system_info() -> dict:
    """Get system information."""
    return {
        "platform": platform.system(),
        "python_version": sys.version,
        "app_name": "TKA Modern",
        "api_version": "1.0.0"
    }
```

### Task 2: Update API Integration (Week 1)

#### 2.1 Complete API Server Setup

```python
# File: modern/src/infrastructure/api/api_server.py (create this)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager

# Import your endpoint routers
from modern.src.infrastructure.api.endpoints.sequences import router as sequences_router
from modern.src.infrastructure.api.endpoints.settings import router as settings_router
from modern.src.infrastructure.api.endpoints.health import router as health_router

def create_app() -> FastAPI:
    """Create FastAPI application."""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup
        print("🚀 TKA API server starting...")
        yield
        # Shutdown
        print("🛑 TKA API server shutting down...")

    app = FastAPI(
        title="TKA API",
        description="The Kinetic Constructor API",
        version="1.0.0",
        lifespan=lifespan
    )

    # CORS middleware for web app
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:3000"],  # SvelteKit dev servers
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal server error: {str(exc)}"}
        )

    # Include routers
    app.include_router(health_router)
    app.include_router(sequences_router)
    app.include_router(settings_router)

    return app

def start_api_server(host: str = "127.0.0.1", port: int = 8000) -> bool:
    """Start the API server."""
    try:
        app = create_app()

        # Try to find available port
        for attempt_port in range(port, port + 10):
            try:
                uvicorn.run(
                    app,
                    host=host,
                    port=attempt_port,
                    log_level="info",
                    access_log=False
                )
                return True
            except OSError as e:
                if "Address already in use" in str(e):
                    continue
                raise

        print(f"❌ Could not start API server on ports {port}-{port+9}")
        return False

    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        return False
```

### Task 3: Desktop API Client (Week 2)

#### 3.1 Simple API Client

```python
# File: modern/src/infrastructure/api/client/api_client.py
import requests
from typing import List, Dict, Any, Optional
import json

class TKAAPIClient:
    """Simple API client for desktop app."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def health_check(self) -> bool:
        """Check if API is available."""
        try:
            response = self.session.get(f"{self.base_url}/api/health", timeout=2)
            return response.status_code == 200
        except:
            return False

    # Sequence operations
    def get_sequences(self) -> List[Dict[str, Any]]:
        """Get all sequences."""
        response = self.session.get(f"{self.base_url}/api/sequences")
        response.raise_for_status()
        return response.json()

    def get_sequence(self, sequence_id: str) -> Optional[Dict[str, Any]]:
        """Get specific sequence."""
        try:
            response = self.session.get(f"{self.base_url}/api/sequences/{sequence_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None

    def create_sequence(self, sequence_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new sequence."""
        response = self.session.post(
            f"{self.base_url}/api/sequences",
            json=sequence_data
        )
        response.raise_for_status()
        return response.json()

    def update_sequence(self, sequence_id: str, sequence_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update sequence."""
        response = self.session.put(
            f"{self.base_url}/api/sequences/{sequence_id}",
            json=sequence_data
        )
        response.raise_for_status()
        return response.json()

    def delete_sequence(self, sequence_id: str) -> bool:
        """Delete sequence."""
        try:
            response = self.session.delete(f"{self.base_url}/api/sequences/{sequence_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False

    # Settings operations
    def get_settings(self) -> Dict[str, Any]:
        """Get all settings."""
        response = self.session.get(f"{self.base_url}/api/settings")
        response.raise_for_status()
        return response.json()

    def update_setting(self, key: str, value: Any) -> bool:
        """Update a setting."""
        try:
            response = self.session.put(
                f"{self.base_url}/api/settings/{key}",
                json={"value": value}
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False
```

#### 3.2 Integrate API Client in Desktop

```python
# File: modern/src/infrastructure/adapters/api_json_bridge.py
from typing import Dict, Any, Optional, List
from modern.src.infrastructure.api.client.api_client import TKAAPIClient
from modern.src.domain.models.core_models import SequenceData

class APIJSONBridge:
    """
    Bridge that makes API calls look like JSON file operations.
    Allows gradual migration without breaking existing code.
    """

    def __init__(self):
        self.api_client = TKAAPIClient()
        self.fallback_to_files = True  # Safety fallback

    def save_sequence(self, sequence_dict: Dict[str, Any]) -> bool:
        """Save sequence via API, fallback to files if API unavailable."""
        try:
            if self.api_client.health_check():
                # Use API
                if "id" in sequence_dict:
                    # Update existing
                    self.api_client.update_sequence(sequence_dict["id"], sequence_dict)
                else:
                    # Create new
                    self.api_client.create_sequence(sequence_dict)
                return True
            elif self.fallback_to_files:
                # Fallback to legacy file saving
                return self._save_to_file_legacy(sequence_dict)
        except Exception as e:
            print(f"API save failed: {e}")
            if self.fallback_to_files:
                return self._save_to_file_legacy(sequence_dict)
        return False

    def load_sequence(self, sequence_id: str) -> Optional[Dict[str, Any]]:
        """Load sequence from API, fallback to files if needed."""
        try:
            if self.api_client.health_check():
                return self.api_client.get_sequence(sequence_id)
            elif self.fallback_to_files:
                return self._load_from_file_legacy(sequence_id)
        except Exception as e:
            print(f"API load failed: {e}")
            if self.fallback_to_files:
                return self._load_from_file_legacy(sequence_id)
        return None

    def get_all_sequences(self) -> List[Dict[str, Any]]:
        """Get all sequences from API."""
        try:
            if self.api_client.health_check():
                return self.api_client.get_sequences()
            elif self.fallback_to_files:
                return self._get_all_from_files_legacy()
        except Exception as e:
            print(f"API get_all failed: {e}")
            if self.fallback_to_files:
                return self._get_all_from_files_legacy()
        return []

    def _save_to_file_legacy(self, sequence_dict: Dict[str, Any]) -> bool:
        """Fallback to legacy file saving."""
        # Use your existing JSON file saving logic
        import json
        import os

        try:
            filename = f"{sequence_dict.get('id', 'unknown')}.json"
            filepath = os.path.join("data", "sequences", filename)  # Your existing path

            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(sequence_dict, f, indent=2)
            return True
        except Exception as e:
            print(f"File fallback failed: {e}")
            return False

    def _load_from_file_legacy(self, sequence_id: str) -> Optional[Dict[str, Any]]:
        """Fallback to legacy file loading."""
        import json
        import os

        try:
            filename = f"{sequence_id}.json"
            filepath = os.path.join("data", "sequences", filename)

            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"File fallback load failed: {e}")
        return None

    def _get_all_from_files_legacy(self) -> List[Dict[str, Any]]:
        """Fallback to loading all files."""
        import json
        import os

        sequences = []
        try:
            sequences_dir = os.path.join("data", "sequences")
            if os.path.exists(sequences_dir):
                for filename in os.listdir(sequences_dir):
                    if filename.endswith('.json'):
                        filepath = os.path.join(sequences_dir, filename)
                        with open(filepath, 'r') as f:
                            sequences.append(json.load(f))
        except Exception as e:
            print(f"File fallback get_all failed: {e}")

        return sequences
```

### Task 4: Web App Integration (Week 2-3)

#### 4.1 SvelteKit API Service

```typescript
// File: tka-web/tka-web-app/src/lib/api/tka-api.ts
export interface SequenceData {
  id: string;
  name: string;
  word: string;
  beats: any[];
  length: number;
  total_duration: number;
  metadata: Record<string, any>;
}

export interface CreateSequenceRequest {
  name: string;
  beats?: any[];
  start_position?: string;
  metadata?: Record<string, any>;
}

export class TKAAPIService {
  private baseUrl: string;

  constructor(baseUrl: string = "http://localhost:8000") {
    this.baseUrl = baseUrl;
  }

  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/api/health`);
      return response.ok;
    } catch {
      return false;
    }
  }

  // Sequence operations
  async getSequences(): Promise<SequenceData[]> {
    const response = await fetch(`${this.baseUrl}/api/sequences`);
    if (!response.ok) {
      throw new Error(`Failed to fetch sequences: ${response.statusText}`);
    }
    return response.json();
  }

  async getSequence(id: string): Promise<SequenceData | null> {
    try {
      const response = await fetch(`${this.baseUrl}/api/sequences/${id}`);
      if (response.status === 404) return null;
      if (!response.ok) throw new Error(response.statusText);
      return response.json();
    } catch (error) {
      console.error("Failed to fetch sequence:", error);
      return null;
    }
  }

  async createSequence(data: CreateSequenceRequest): Promise<SequenceData> {
    const response = await fetch(`${this.baseUrl}/api/sequences`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error(`Failed to create sequence: ${response.statusText}`);
    }
    return response.json();
  }

  async updateSequence(
    id: string,
    data: CreateSequenceRequest,
  ): Promise<SequenceData> {
    const response = await fetch(`${this.baseUrl}/api/sequences/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error(`Failed to update sequence: ${response.statusText}`);
    }
    return response.json();
  }

  async deleteSequence(id: string): Promise<void> {
    const response = await fetch(`${this.baseUrl}/api/sequences/${id}`, {
      method: "DELETE",
    });
    if (!response.ok) {
      throw new Error(`Failed to delete sequence: ${response.statusText}`);
    }
  }

  // Settings operations
  async getSettings(): Promise<Record<string, any>> {
    const response = await fetch(`${this.baseUrl}/api/settings`);
    if (!response.ok) {
      throw new Error(`Failed to fetch settings: ${response.statusText}`);
    }
    const data = await response.json();
    return data.settings;
  }

  async updateSetting(key: string, value: any): Promise<void> {
    const response = await fetch(`${this.baseUrl}/api/settings/${key}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ value }),
    });
    if (!response.ok) {
      throw new Error(`Failed to update setting: ${response.statusText}`);
    }
  }
}

// Global API instance
export const tkaAPI = new TKAAPIService();
```

#### 4.2 Svelte Stores with API

```typescript
// File: tka-web/tka-web-app/src/lib/stores/sequences.ts
import { writable } from "svelte/store";
import {
  tkaAPI,
  type SequenceData,
  type CreateSequenceRequest,
} from "../api/tka-api";

function createSequenceStore() {
  const { subscribe, set, update } = writable<SequenceData[]>([]);

  return {
    subscribe,

    async loadAll() {
      try {
        const sequences = await tkaAPI.getSequences();
        set(sequences);
      } catch (error) {
        console.error("Failed to load sequences:", error);
        set([]);
      }
    },

    async create(data: CreateSequenceRequest) {
      try {
        const newSequence = await tkaAPI.createSequence(data);
        update((sequences) => [...sequences, newSequence]);
        return newSequence;
      } catch (error) {
        console.error("Failed to create sequence:", error);
        throw error;
      }
    },

    async update(id: string, data: CreateSequenceRequest) {
      try {
        const updatedSequence = await tkaAPI.updateSequence(id, data);
        update((sequences) =>
          sequences.map((seq) => (seq.id === id ? updatedSequence : seq)),
        );
        return updatedSequence;
      } catch (error) {
        console.error("Failed to update sequence:", error);
        throw error;
      }
    },

    async delete(id: string) {
      try {
        await tkaAPI.deleteSequence(id);
        update((sequences) => sequences.filter((seq) => seq.id !== id));
      } catch (error) {
        console.error("Failed to delete sequence:", error);
        throw error;
      }
    },
  };
}

export const sequences = createSequenceStore();
```

## Success Criteria

### Validation Steps

1. **API Health**: `curl http://localhost:8000/api/health` returns 200
2. **Desktop Integration**: Desktop can save/load through API with JSON fallback
3. **Web Integration**: SvelteKit app can CRUD sequences
4. **Data Consistency**: Same sequence appears identically in desktop and web
5. **Fallback Works**: Desktop works when API is down

### Test Commands

```bash
# Test API endpoints
curl -X POST http://localhost:8000/api/sequences \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Sequence","beats":[]}'

# Test desktop with API
cd F:\CODE\TKA\tka-desktop\modern
python main.py

# Test web app
cd F:\CODE\TKA\tka-web\tka-web-app
npm run dev
```

## Completion Checklist

- [ ] API endpoints handle all sequence CRUD operations
- [ ] Settings endpoints work for user preferences
- [ ] Desktop saves/loads via API with file fallback
- [ ] Web app performs all operations through API
- [ ] Error handling works properly
- [ ] CORS configured for web app
- [ ] Both apps show consistent data
- [ ] Performance is acceptable (< 100ms API responses)

**Next**: After API unification works, proceed to Phase 2 (Event System) for real-time sync between desktop and web.

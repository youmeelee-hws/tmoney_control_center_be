from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import secrets

from app.mock_data import (
    get_all_stations,
    get_station_by_id,
    get_gates_by_station,
    get_gate_by_id,
    get_streams_by_gate,
    get_stream_by_id,
)

router = APIRouter(tags=["stations"])

# ============================================
# Stations API
# ============================================

class StationResponse(BaseModel):
    stationId: str
    name: str

class StationListResponse(BaseModel):
    stations: List[StationResponse]

@router.get("/stations", response_model=StationListResponse)
def get_stations() -> StationListResponse:
    """Get all stations"""
    stations = get_all_stations()
    return StationListResponse(
        stations=[
            StationResponse(stationId=s.station_id, name=s.name)
            for s in stations
        ]
    )

# ============================================
# Gates API
# ============================================

class GateResponse(BaseModel):
    gateId: str
    stationId: str
    name: str

class GateListResponse(BaseModel):
    gates: List[GateResponse]

@router.get("/stations/{stationId}/gates", response_model=GateListResponse)
def get_station_gates(stationId: str) -> GateListResponse:
    """Get all gates for a specific station"""
    # Verify station exists
    station = get_station_by_id(stationId)
    if not station:
        raise HTTPException(status_code=404, detail=f"Station {stationId} not found")
    
    gates = get_gates_by_station(stationId)
    return GateListResponse(
        gates=[
            GateResponse(gateId=g.gate_id, stationId=g.station_id, name=g.name)
            for g in gates
        ]
    )

# ============================================
# Streams API
# ============================================

class StreamResponse(BaseModel):
    streamId: str
    gateId: str
    name: str
    status: str

class StreamListResponse(BaseModel):
    streams: List[StreamResponse]

@router.get("/gates/{gateId}/streams", response_model=StreamListResponse)
def get_gate_streams(gateId: str) -> StreamListResponse:
    """Get all streams for a specific gate"""
    # Verify gate exists
    gate = get_gate_by_id(gateId)
    if not gate:
        raise HTTPException(status_code=404, detail=f"Gate {gateId} not found")
    
    streams = get_streams_by_gate(gateId)
    return StreamListResponse(
        streams=[
            StreamResponse(
                streamId=s.stream_id,
                gateId=s.gate_id,
                name=s.name,
                status=s.status
            )
            for s in streams
        ]
    )

# ============================================
# Play Ticket API (kept for backward compatibility)
# ============================================

class PlayTicketResponse(BaseModel):
    streamId: str
    playTicket: str
    expiresAt: str  # ISO string
    whepUrl: str

@router.post("/streams/{streamId}/play-ticket", response_model=PlayTicketResponse)
def issue_play_ticket(streamId: str) -> PlayTicketResponse:
    """Issue a play ticket for a stream"""
    # Verify stream exists
    stream = get_stream_by_id(streamId)
    if not stream:
        raise HTTPException(status_code=404, detail=f"Stream {streamId} not found")
    
    expiresAt = (datetime.utcnow() + timedelta(minutes=30)).isoformat() + "Z"
    playTicket = "ptk_abc123"  # TODO: 나중에 실제 티켓 발급 로직으로 대치
    whepUrl = "https://media.stub.local/whep/" + streamId  # TODO: 나중에 실제 미디어 서버 URL로 대치
    
    return PlayTicketResponse(
        streamId=streamId,
        playTicket=playTicket,
        expiresAt=expiresAt,
        whepUrl=whepUrl
    )
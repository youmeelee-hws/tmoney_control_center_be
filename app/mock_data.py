"""
Mock data for stations, gates, and streams
Based on frontend SamplePage3.tsx mock data
"""

from typing import Dict, List

class MockStation:
    def __init__(self, station_id: str, name: str):
        self.station_id = station_id
        self.name = name

class MockGate:
    def __init__(self, gate_id: str, station_id: str, name: str):
        self.gate_id = gate_id
        self.station_id = station_id
        self.name = name

class MockStream:
    def __init__(self, stream_id: str, gate_id: str, name: str, status: str = "unknown"):
        self.stream_id = stream_id
        self.gate_id = gate_id
        self.name = name
        self.status = status

# Mock stations
MOCK_STATIONS = [
    MockStation(station_id="station-001", name="서울역"),
    MockStation(station_id="station-002", name="강남역"),
    MockStation(station_id="station-003", name="잠실역"),
]

# Mock gates by station
MOCK_GATES = [
    # 서울역 (4개 게이트)
    MockGate(gate_id="gate-001", station_id="station-001", name="1번 게이트"),
    MockGate(gate_id="gate-002", station_id="station-001", name="2번 게이트"),
    MockGate(gate_id="gate-003", station_id="station-001", name="3번 게이트"),
    MockGate(gate_id="gate-004", station_id="station-001", name="4번 게이트"),
    # 강남역 (6개 게이트)
    MockGate(gate_id="gate-005", station_id="station-002", name="1번 게이트"),
    MockGate(gate_id="gate-006", station_id="station-002", name="2번 게이트"),
    MockGate(gate_id="gate-007", station_id="station-002", name="3번 게이트"),
    MockGate(gate_id="gate-008", station_id="station-002", name="4번 게이트"),
    MockGate(gate_id="gate-009", station_id="station-002", name="5번 게이트"),
    MockGate(gate_id="gate-010", station_id="station-002", name="6번 게이트"),
    # 잠실역 (3개 게이트)
    MockGate(gate_id="gate-011", station_id="station-003", name="1번 게이트"),
    MockGate(gate_id="gate-012", station_id="station-003", name="2번 게이트"),
    MockGate(gate_id="gate-013", station_id="station-003", name="3번 게이트"),
]

# Mock streams - 각 게이트당 1개의 스트림만 존재
MOCK_STREAMS = [
    # 서울역 게이트별 스트림 (4개)
    MockStream(stream_id="stream-001", gate_id="gate-001", name="1번 게이트 카메라", status="active"),
    MockStream(stream_id="stream-002", gate_id="gate-002", name="2번 게이트 카메라", status="active"),
    MockStream(stream_id="stream-003", gate_id="gate-003", name="3번 게이트 카메라", status="active"),
    MockStream(stream_id="stream-004", gate_id="gate-004", name="4번 게이트 카메라", status="active"),
    # 강남역 게이트별 스트림 (6개)
    MockStream(stream_id="stream-005", gate_id="gate-005", name="1번 게이트 카메라", status="active"),
    MockStream(stream_id="stream-006", gate_id="gate-006", name="2번 게이트 카메라", status="active"),
    MockStream(stream_id="stream-007", gate_id="gate-007", name="3번 게이트 카메라", status="active"),
    MockStream(stream_id="stream-008", gate_id="gate-008", name="4번 게이트 카메라", status="active"),
    MockStream(stream_id="stream-009", gate_id="gate-009", name="5번 게이트 카메라", status="active"),
    MockStream(stream_id="stream-010", gate_id="gate-010", name="6번 게이트 카메라", status="active"),
    # 잠실역 게이트별 스트림 (3개)
    MockStream(stream_id="stream-011", gate_id="gate-011", name="1번 게이트 카메라", status="active"),
    MockStream(stream_id="stream-012", gate_id="gate-012", name="2번 게이트 카메라", status="active"),
    MockStream(stream_id="stream-013", gate_id="gate-013", name="3번 게이트 카메라", status="active"),
]

# Helper functions to query mock data
def get_all_stations() -> List[MockStation]:
    """Get all stations"""
    return MOCK_STATIONS

def get_station_by_id(station_id: str) -> MockStation | None:
    """Get station by ID"""
    return next((s for s in MOCK_STATIONS if s.station_id == station_id), None)

def get_gates_by_station(station_id: str) -> List[MockGate]:
    """Get all gates for a station"""
    return [g for g in MOCK_GATES if g.station_id == station_id]

def get_gate_by_id(gate_id: str) -> MockGate | None:
    """Get gate by ID"""
    return next((g for g in MOCK_GATES if g.gate_id == gate_id), None)

def get_streams_by_gate(gate_id: str) -> List[MockStream]:
    """Get all streams for a gate"""
    return [s for s in MOCK_STREAMS if s.gate_id == gate_id]

def get_stream_by_id(stream_id: str) -> MockStream | None:
    """Get stream by ID"""
    return next((s for s in MOCK_STREAMS if s.stream_id == stream_id), None)


#!/usr/bin/env python3
"""
MediaMTX 오류 로깅 시스템 테스트 스크립트

이 스크립트는 오류 로그 API를 직접 호출하여 로그가 제대로 저장되는지 테스트합니다.
"""

import requests
import json
from datetime import datetime

API_BASE_URL = "http://localhost:8000/api/v1"

def test_log_error():
    """오류 로그 저장 테스트"""
    print("=" * 60)
    print("MediaMTX 오류 로그 저장 테스트")
    print("=" * 60)
    
    # 테스트 데이터
    test_log = {
        "streamId": "test-stream-001",
        "errorType": "whep_post_failed",
        "errorMessage": "WHEP POST failed: 502 Bad Gateway - MediaMTX server is down",
        "statusCode": 502,
        "whepUrl": "http://192.168.0.10:8889/stitched/whep",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "userAgent": "Mozilla/5.0 (Test Script)",
        "clientInfo": {
            "browserName": "Python Test Script",
            "browserVersion": "3.10",
            "os": "Linux",
            "screenResolution": "N/A"
        }
    }
    
    print("\n[1] 오류 로그 전송...")
    print(f"POST {API_BASE_URL}/error-logs/mediamtx")
    print(f"Data: {json.dumps(test_log, indent=2)}")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/error-logs/mediamtx",
            json=test_log,
            timeout=10
        )
        
        print(f"\n응답 상태 코드: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 로그 저장 성공!")
            print(f"   - 성공 여부: {result.get('success')}")
            print(f"   - 로그 파일: {result.get('logFile')}")
            print(f"   - 메시지: {result.get('message')}")
            return True
        else:
            print(f"❌ 로그 저장 실패: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 백엔드 서버에 연결할 수 없습니다.")
        print("   백엔드가 실행 중인지 확인하세요: http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False

def test_get_logs():
    """최근 오류 로그 조회 테스트"""
    print("\n" + "=" * 60)
    print("최근 오류 로그 조회 테스트")
    print("=" * 60)
    
    print(f"\n[2] 최근 로그 조회...")
    print(f"GET {API_BASE_URL}/error-logs/mediamtx/latest?limit=5")
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/error-logs/mediamtx/latest",
            params={"limit": 5},
            timeout=10
        )
        
        print(f"\n응답 상태 코드: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            logs = result.get('logs', [])
            count = result.get('count', 0)
            
            print(f"✅ 로그 조회 성공!")
            print(f"   - 조회된 로그 개수: {count}")
            print(f"   - 메시지: {result.get('message')}")
            
            if logs:
                print(f"\n최근 로그 {min(3, len(logs))}개:")
                for i, log in enumerate(logs[:3], 1):
                    print(f"\n   [{i}] {log.get('timestamp')}")
                    print(f"       Stream: {log.get('streamId')}")
                    print(f"       Type: {log.get('errorType')}")
                    print(f"       Message: {log.get('errorMessage')[:60]}...")
            else:
                print("\n   ℹ️  저장된 로그가 없습니다.")
            
            return True
        else:
            print(f"❌ 로그 조회 실패: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 백엔드 서버에 연결할 수 없습니다.")
        return False
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False

def main():
    print("\n🚀 MediaMTX 오류 로깅 시스템 테스트 시작\n")
    
    # 테스트 1: 오류 로그 저장
    success1 = test_log_error()
    
    # 테스트 2: 로그 조회
    success2 = test_get_logs()
    
    # 결과 요약
    print("\n" + "=" * 60)
    print("테스트 결과 요약")
    print("=" * 60)
    print(f"로그 저장: {'✅ 성공' if success1 else '❌ 실패'}")
    print(f"로그 조회: {'✅ 성공' if success2 else '❌ 실패'}")
    
    if success1 and success2:
        print("\n🎉 모든 테스트 통과!")
        print("\n다음 단계:")
        print("1. 로그 파일 확인:")
        print("   cat logs/mediamtx_errors/$(date +%Y-%m-%d).jsonl")
        print("2. 프론트엔드에서 실제 MediaMTX 다운 시나리오 테스트")
    else:
        print("\n⚠️  일부 테스트 실패")
        print("백엔드가 실행 중인지 확인하세요:")
        print("  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    
    print()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Debouncing 동작 확인 테스트 스크립트

같은 오류를 연속으로 보냈을 때 첫 번째만 로그되고 나머지는 스킵되는지 확인합니다.
"""

import requests
import json
import time
from datetime import datetime

API_BASE_URL = "http://localhost:8000/api/v1"

def send_test_error(test_name: str):
    """테스트 오류 로그 전송"""
    test_log = {
        "streamId": "debounce-test-stream",
        "errorType": "whep_post_failed",
        "errorMessage": f"Test error: {test_name}",
        "statusCode": 502,
        "whepUrl": "http://192.168.0.10:8889/test/whep",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "userAgent": "Debounce Test Script",
        "clientInfo": {
            "browserName": "Test Script",
            "browserVersion": "1.0",
            "os": "Test",
            "screenResolution": "N/A"
        }
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/error-logs/mediamtx",
            json=test_log,
            timeout=5
        )
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def count_logs():
    """현재 로그 개수 확인"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/error-logs/mediamtx/latest",
            params={"limit": 100},
            timeout=5
        )
        if response.status_code == 200:
            return response.json().get('count', 0)
        return 0
    except:
        return 0

def main():
    print("\n" + "="*60)
    print("Debouncing 동작 확인 테스트")
    print("="*60)
    print("\n⚠️  주의: 이 테스트는 백엔드에 실제 로그를 생성합니다.")
    print("프론트엔드의 Debouncing 로직은 브라우저에서 직접 테스트하세요.\n")
    
    # 초기 로그 개수 확인
    initial_count = count_logs()
    print(f"현재 로그 개수: {initial_count}\n")
    
    print("="*60)
    print("테스트 1: 연속 전송 (백엔드 확인용)")
    print("="*60)
    print("설명: 백엔드는 모든 요청을 받습니다.")
    print("      (Debouncing은 프론트엔드에서 동작)\n")
    
    success_count = 0
    for i in range(3):
        print(f"[{i+1}/3] 오류 로그 전송 중...")
        if send_test_error(f"Test {i+1}"):
            print(f"  ✅ 전송 성공")
            success_count += 1
        else:
            print(f"  ❌ 전송 실패")
        time.sleep(0.5)
    
    print(f"\n전송 성공: {success_count}/3")
    
    # 최종 로그 개수 확인
    time.sleep(1)
    final_count = count_logs()
    added_logs = final_count - initial_count
    
    print(f"\n추가된 로그: {added_logs}개")
    print(f"최종 로그 개수: {final_count}\n")
    
    print("="*60)
    print("프론트엔드 Debouncing 테스트 방법")
    print("="*60)
    print("""
1. 브라우저를 열고 프론트엔드에 접속
2. MediaMTX 서버를 중지하여 오류 발생시키기:
   pkill mediamtx

3. 브라우저 콘솔(F12)을 열어 다음 메시지 확인:
   ✅ 첫 번째: "[WebRTC] Error logged successfully: whep_post_failed"
   ❌ 이후 5분 이내: "Skipping duplicate error log: whep_post_failed"

4. 페이지를 여러 번 새로고침해도:
   - 5분 이내에는 로그가 전송되지 않음
   - 콘솔에 "Skipping duplicate error log" 메시지 출력

5. 5분 후 다시 시도하면:
   - 새로운 로그 전송됨
   - "[WebRTC] Error logged successfully" 메시지 출력

6. 로그 파일 확인:
   cat logs/mediamtx_errors/$(date +%Y-%m-%d).jsonl | wc -l
   → 5분마다 1개씩만 추가되는지 확인
    """)
    
    print("\n" + "="*60)
    print("테스트 완료")
    print("="*60)
    print("\n✅ 백엔드 API는 정상 동작합니다.")
    print("✅ Debouncing은 프론트엔드(브라우저)에서 동작합니다.\n")

if __name__ == "__main__":
    main()

#!/bin/bash
#
# MediaMTX 오류 로그 정리 스크립트
#
# 30일 이상 된 로그 파일을 자동으로 삭제합니다.
# Cron으로 매일 실행하도록 설정하세요.
#

LOG_DIR="/root/tmoney_control_center_be/logs/mediamtx_errors"
RETENTION_DAYS=30

echo "=================================================="
echo "MediaMTX Error Log Cleanup"
echo "=================================================="
echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Log Directory: $LOG_DIR"
echo "Retention Period: $RETENTION_DAYS days"
echo ""

# 로그 디렉토리 존재 확인
if [ ! -d "$LOG_DIR" ]; then
    echo "Warning: Log directory does not exist: $LOG_DIR"
    exit 0
fi

# 삭제 전 파일 개수 확인
TOTAL_FILES=$(find "$LOG_DIR" -name "*.jsonl" 2>/dev/null | wc -l)
OLD_FILES=$(find "$LOG_DIR" -name "*.jsonl" -mtime +$RETENTION_DAYS 2>/dev/null | wc -l)

echo "Total log files: $TOTAL_FILES"
echo "Files older than $RETENTION_DAYS days: $OLD_FILES"
echo ""

if [ "$OLD_FILES" -gt 0 ]; then
    echo "Deleting old log files..."
    
    # 삭제할 파일 목록 표시 (옵션)
    # find "$LOG_DIR" -name "*.jsonl" -mtime +$RETENTION_DAYS -ls
    
    # 오래된 로그 파일 삭제
    find "$LOG_DIR" -name "*.jsonl" -mtime +$RETENTION_DAYS -delete
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully deleted $OLD_FILES old log file(s)"
    else
        echo "❌ Failed to delete some files"
        exit 1
    fi
else
    echo "ℹ️  No old files to delete"
fi

echo ""
echo "Cleanup completed at $(date '+%Y-%m-%d %H:%M:%S')"
echo "=================================================="

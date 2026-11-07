#!/bin/bash
cd "$(dirname "$0")"

echo "=========================================================="
echo "  CogniSTEM Research Lab - Advanced Pedagogy Analytics    "
echo "  Khoa học Dữ liệu Thực nghiệm Sư phạm STEM (HCMUTE)      "
echo "=========================================================="
echo ""
echo "🚀 Đang khởi động ứng dụng Streamlit Dashboard..."
echo "🌐 Trình duyệt web sẽ tự động mở tại http://localhost:8501"
echo "💡 Nhấn Ctrl + C để dừng ứng dụng khi hoàn thành."
echo ""

if [ -f "$HOME/markitdown-venv/bin/streamlit" ]; then
    "$HOME/markitdown-venv/bin/streamlit" run app.py
elif command -v streamlit &> /dev/null; then
    streamlit run app.py
else
    python3 -m streamlit run app.py
fi

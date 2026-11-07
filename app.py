"""
================================================================================
CogniSTEM Research Lab: Advanced STEM Edumetrics & Pedagogy Analytics
Doctoral Research Project | HCMUTE
Author: Pham Ba Hong Son (NCS Pham Ba Hong Son)
GitHub: https://github.com/mikepham358/cognistem-analytics
================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import json
import os

# Set page config with Google Material aesthetic
st.set_page_config(
    page_title="CogniSTEM Analytics | Research Lab",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Google Material Design styling
st.markdown(r"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Roboto:wght@300;400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Google Sans', 'Roboto', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1a73e8 0%, #1557b0 100%);
        color: white;
        padding: 24px 32px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(26,115,232,0.15);
    }
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #dadce0;
        box-shadow: 0 1px 3px rgba(60,64,67,0.1);
        transition: all 0.2s ease-in-out;
    }
    .metric-card:hover {
        box-shadow: 0 4px 12px rgba(60,64,67,0.15);
        border-color: #1a73e8;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 24px;
        padding: 8px 18px;
        background-color: #f1f3f4;
        color: #5f6368;
        font-weight: 500;
        font-size: 13px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e8f0fe !important;
        color: #1a73e8 !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA LOADING ENGINE
# -----------------------------------------------------------------------------
@st.cache_data
def load_default_data():
    json_path = os.path.join(os.path.dirname(__file__), 'data_raw_27_sv.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return pd.DataFrame(data['students']), data['metadata']
    return None, None

df_raw, metadata = load_default_data()

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://www.gstatic.com/images/branding/googlelogo/svg/googlelogo_clr_74x24px.svg", width=110)
    st.markdown("### **CogniSTEM Lab**")
    st.caption("Advanced STEM Edumetrics Platform")
    st.markdown("---")
    
    mode = st.radio(
        "Chế độ trình diễn:",
        ["🎓 Bảo vệ Hội đồng (Presentation)", "🔬 Google Research Scientist", "📖 Hướng dẫn trực quan (Beginner)"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("**Thông tin mẫu thực nghiệm:**")
    st.markdown("- **Quy mô:** $N = 27$ sinh viên SPKT")
    st.markdown("- **Công cụ:** BM-01 (Pre), BM-02 (Post), BM-03 (CLT)")
    st.markdown("- **Can thiệp:** 180 phút (30' - 120' - 30')")
    st.markdown("- **Mô hình AI:** Gemini Notebook (LearnLM)")
    
    st.markdown("---")
    st.caption("Tác giả: Phạm Bá Hồng Sơn (HCMUTE)")
    st.caption("GitHub: [mikepham358](https://github.com/mikepham358)")

# -----------------------------------------------------------------------------
# MAIN HEADER
# -----------------------------------------------------------------------------
st.markdown(r"""
<div class="main-header">
    <div style="font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9;">
        HCMUTE Doctoral Research • Quantitative Pedagogy Lab
    </div>
    <h1 style="font-size: 26px; font-weight: 700; margin: 8px 0 4px 0;">
        Hệ Thống Trực Quan Hóa & Phân Tích Dữ Liệu Thực Nghiệm Sư Phạm
    </h1>
    <p style="font-size: 14px; opacity: 0.95; margin: 0; line-height: 1.5;">
        Kiểm định giả thuyết can thiệp sư phạm, tăng trưởng Hake, Thuyết tải nhận thức Sweller và Tâm trắc học cổ điển (CTT).
    </p>
</div>
""", unsafe_allow_html=True)

if df_raw is None:
    st.error("Không tìm thấy tệp dữ liệu data_raw_27_sv.json!")
    st.stop()

# -----------------------------------------------------------------------------
# TOP METRIC CARDS
# -----------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Điểm Pre-test TB (O1)",
        value=f"{df_raw['pre'].mean():.2f}",
        delta=f"SD = {df_raw['pre'].std(ddof=1):.2f}"
    )

with col2:
    st.metric(
        label="Điểm Post-test TB (O2)",
        value=f"{df_raw['post'].mean():.2f}",
        delta=f"+{df_raw['delta'].mean():.2f} đ (+14.7%)",
        delta_color="normal"
    )

with col3:
    t_stat, p_val = stats.ttest_rel(df_raw['post'], df_raw['pre'])
    st.metric(
        label="Kiểm định t từng cặp",
        value=f"t = {t_stat:.3f}",
        delta="p = 0.00672 (p < 0.01)"
    )

with col4:
    cohen_d = df_raw['delta'].mean() / df_raw['delta'].std(ddof=1)
    st.metric(
        label="Cohen's d & Hake g",
        value=f"d = {cohen_d:.3f}",
        delta=f"ḡ = {df_raw['hake_g'].mean():.3f}"
    )

# -----------------------------------------------------------------------------
# NAVIGATION TABS
# -----------------------------------------------------------------------------
tab_overview, tab_data, tab_hypothesis, tab_hake, tab_ctt, tab_sem, tab_clt, tab_corr, tab_council = st.tabs([
    "📊 Tổng quan KPI",
    "📁 Bảng dữ liệu thô",
    "🔬 Kiểm định giả thuyết",
    "📈 Tăng trưởng Hake (g)",
    "🎯 Tâm trắc học CTT",
    "🛡️ Bóc tách 9 ca sụt giảm",
    "🧠 Tải nhận thức CLT & Paas",
    "🔥 Ma trận tương quan",
    "🎓 Bộ câu hỏi Hội đồng"
])

# TAB 1: OVERVIEW
with tab_overview:
    st.subheader("Phân Phối Điểm Số Pre-test vs Post-test (N = 27)")
    chart_df = pd.DataFrame({
        "Sinh viên": [f"SV{s:02d}" for s in df_raw['stt']],
        "Pre-test": df_raw['pre'],
        "Post-test": df_raw['post']
    }).set_index("Sinh viên")
    st.bar_chart(chart_df, color=["#4285F4", "#34A853"], height=350)
    
    st.markdown(r"""
    **Nhận định tổng quan:**
    - Điểm kiểm tra trung bình sau tác động tăng từ **6,36 ± 1,22** lên **7,30 ± 1,94** điểm ($\Delta P = +0,93$, tương đương mức tăng trưởng **+14,7%**).
    - Có **18/27 sinh viên (66,7%)** đạt mức tăng trưởng dương.
    - Phần trắc nghiệm tăng **+13,9%** (từ 4,47 lên 5,09 đ). Phần tự luận ngắn tăng **+16,9%** (từ 1,89 lên 2,21 đ).
    """)

# TAB 2: DATA TABLE
with tab_data:
    st.subheader("Bảng Dữ Liệu Thô 27 Sinh Viên (Zero Formulas)")
    st.caption("Dữ liệu tĩnh nguyên bản, sẵn sàng nhập liệu vào SPSS, R, Python hoặc Jamovi")
    
    col_f1, col_f2 = st.columns([1, 1])
    with col_f1:
        sel_group = st.selectbox("Lọc theo Nhóm thực nghiệm:", ["Tất cả Nhóm"] + list(df_raw['group'].unique()))
    with col_f2:
        sel_gain = st.selectbox("Lọc theo Mức tăng trưởng Hake:", ["Tất cả mức"] + list(df_raw['hake_level'].unique()))
        
    filtered_df = df_raw.copy()
    if sel_group != "Tất cả Nhóm":
        filtered_df = filtered_df[filtered_df['group'] == sel_group]
    if sel_gain != "Tất cả mức":
        filtered_df = filtered_df[filtered_df['hake_level'] == sel_gain]
        
    st.dataframe(
        filtered_df[['stt', 'id', 'name', 'group', 'pre', 'post', 'delta', 'hake_g', 'hake_level', 'paas_r', 'clt_il', 'clt_el', 'clt_gl', 'paas_e', 'paas_level']],
        use_container_width=True,
        height=450
    )

# TAB 3: HYPOTHESIS TESTING
with tab_hypothesis:
    st.subheader("Kiểm Định Giả Thuyết Can Thiệp Sư Phạm")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("#### 1. Paired Student's t-test (Kiểm định tham số)")
        st.latex(r"t = \frac{\bar{D}}{\frac{s_D}{\sqrt{N}}} = \frac{0,9333}{\frac{1,6467}{\sqrt{27}}} = 2,945")
        st.markdown(rf"""
        - **Bậc tự do (df):** $N - 1 = 26$
        - **Mức ý nghĩa $p$ (two-tailed):** `0,00672` ($p < 0,01$)
        - **Kết luận:** Giả thuyết $H_0$ bị bác bỏ ở độ tin cậy $99\%$. Năng lực dạy học STEM của sinh viên có sự tiến bộ thực chất.
        """)
        
    with col_t2:
        st.markdown("#### 2. Wilcoxon Signed-Rank Test (Phi tham số)")
        st.latex(r"z = \frac{W - \frac{N(N+1)}{4}}{\sqrt{\frac{N(N+1)(2N+1)}{24}}} = -2,511")
        st.markdown(rf"""
        - **Tổng thứ hạng có dấu:** $W^+ = 293,5; W^- = 84,5$
        - **Mức ý nghĩa $p$-value:** `0,01203` ($p < 0,05$)
        - **Tính nhất quán:** Cả hai phương pháp kiểm định tham số và phi tham số đều thống nhất khẳng định tác động sư phạm vững chắc.
        """)
        
    st.markdown("---")
    st.markdown("#### Đánh Giá Kích Thước Hiệu Ứng (Effect Size)")
    st.markdown(rf"""
    - **Cohen's $d_z$ cho mẫu cặp:** $d_z = \frac{{\bar{{D}}}}{{s_D}} = \mathbf{{0,567}}$ *(Mức độ tác động Trung bình theo Cohen, 1988)*.
    - **Hedges' $g$ hiệu chỉnh mẫu nhỏ:** $g = d_z \times [1 - \frac{{3}}{{4(26) - 1}}] = \mathbf{{0,550}}$.
    - **So sánh chuẩn giáo dục của Hattie (2009):** Vượt xa ngưỡng kỳ vọng mong muốn can thiệp ($d > 0,40$).
    """)

# TAB 4: HAKE GAIN
with tab_hake:
    st.subheader("Chỉ Số Tăng Trưởng Chuẩn Hóa Hake (g)")
    st.latex(r"g = \frac{P_{\text{post}} - P_{\text{pre}}}{10 - P_{\text{pre}}}")
    st.caption("Trung bình toàn lớp: ḡ = 0,289 ± 0,509")
    
    col_h1, col_h2 = st.columns([1, 1])
    with col_h1:
        hake_counts = df_raw['hake_level'].value_counts()
        st.markdown("**Phân bố 3 mức tăng trưởng Hake:**")
        st.write(hake_counts)
        st.bar_chart(hake_counts, color="#1a73e8")
    with col_h2:
        st.markdown(r"""
        **Quy chuẩn phân loại Hake (1998):**
        1. **Tăng trưởng cao ($g \ge 0,7$):** **8 sinh viên (29,6%)** — đạt điểm xuất sắc từ 8,8 đến 10,0 điểm.
        2. **Tăng trưởng trung bình ($0,3 \le g < 0,7$):** **5 sinh viên (18,5%)** — tiến bộ ổn định (+0,8 đến +2,4 đ).
        3. **Tăng trưởng thấp ($g < 0,3$):** **14 sinh viên (51,9%)** — gồm nhóm tăng nhẹ và 9 em gặp hạn chế tốc độ viết tự luận.
        """)

# TAB 5: CTT PSYCHOMETRICS
with tab_ctt:
    st.subheader("Lý Thuyết Trắc Nghiệm Cổ Điển (Classical Test Theory - CTT)")
    
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        st.metric("KR-20 Trắc nghiệm (30 câu)", "0,7388", "+48,5% so với Pre")
    with col_c2:
        st.metric("Alpha Tự luận ngắn (10 câu)", "0,9255", "+40,4% so với Pre")
    with col_c3:
        st.metric("Alpha Toàn bài (40 câu)", "0,8876", "+26,1% so với Pre")
        
    st.markdown("#### Độ Phân Hóa 10 Câu Tự Luận Ngắn Post-test (CITC rit)")
    saq_citc = pd.DataFrame({
        "Mục hỏi": ["TL01", "TL02", "TL03", "TL04", "TL05", "TL06", "TL07", "TL08", "TL09", "TL10"],
        "CITC (rit)": [0.6354, 0.4899, 0.5084, 0.8748, 0.8354, 0.9076, 0.7040, 0.7481, 0.6921, 0.7279],
        "Alpha if Deleted": [0.9222, 0.9287, 0.9274, 0.9091, 0.9110, 0.9067, 0.9184, 0.9159, 0.9191, 0.9171]
    }).set_index("Mục hỏi")
    st.bar_chart(saq_citc["CITC (rit)"], color="#1a73e8", height=280)
    st.info("✓ 100% các câu hỏi tự luận ngắn đều có r_it ≥ 0,4899, vượt xa ngưỡng chuẩn CTT (r_it ≥ 0,30). Giữ lại 100% mục hỏi.")

# TAB 6: 9 DROPS PROOF
with tab_sem:
    st.subheader("Minh Chứng CTT Cho 9 Ca Sụt Giảm Điểm (ΔP < 0)")
    st.markdown(r"""
    Dưới lăng kính Sai số đo lường chuẩn CTT:
    $$\text{SEM}_{\text{post}} = 0,652 \text{ đ}, \quad \text{SEM}_{\text{pre}} = 0,662 \text{ đ} \implies \text{SE}_{\text{diff}} = \sqrt{\text{SEM}_{\text{post}}^2 + \text{SEM}_{\text{pre}}^2} = \mathbf{0,929 \text{ đ}}$$
    Biên độ dao động ngẫu nhiên $95\%$ tin cậy: $\mathbf{\pm 1,96 \times \text{SE}_{\text{diff}} = \pm 1,82 \text{ đ}}$.
    """)
    
    drops_df = df_raw[df_raw['delta'] < 0].copy()
    drops_df['status_sem'] = drops_df['delta'].apply(lambda d: "✓ Trong biên độ 95% (Đạt)" if abs(d) <= 1.82 else "Ngoài biên độ")
    
    st.table(drops_df[['stt', 'id', 'name', 'pre', 'post', 'delta', 'status_sem']])
    st.success("Khẳng định 100% (9/9) sinh viên đều có |ΔP| ≤ 1,80 đ, hoàn toàn nằm trong biên độ sai số ngẫu nhiên ± 1,82 đ của công cụ đo lường!")

# TAB 7: CLT & PAAS
with tab_clt:
    st.subheader("Thuyết Tải Nhận Thức CLT & Không Gian 2 Chiều Paas (E)")
    st.latex(r"E = \frac{z_P - z_R}{\sqrt{2}}, \quad \text{trong đó } z_P = \frac{P_{\text{post}} - \bar{P}}{s_P}, \quad z_R = \frac{R - \bar{R}}{s_R}")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.metric("Tải nội sinh (IL)", f"{df_raw['clt_il'].mean():.2f} / 5.0", "71.9%")
    with col_p2:
        st.metric("Tải ngoại lai (EL)", f"{df_raw['clt_el'].mean():.2f} / 5.0", "53.0% (Thấp)")
    with col_p3:
        st.metric("Tải hữu ích (GL)", f"{df_raw['clt_gl'].mean():.2f} / 5.0", "75.9% (Cao)")
        
    st.markdown("#### Phân Bố Hiệu Quả Giảng Dạy Paas (E) Theo 4 Góc Phần Tư")
    e_counts = df_raw['paas_level'].value_counts()
    st.write(e_counts)
    st.bar_chart(e_counts, color="#34A853")

# TAB 8: CORRELATION MATRIX
with tab_corr:
    st.subheader("Ma Trận Tương Quan Tuyến Tính Pearson (Bảng 3.8)")
    corr_cols = ['pre', 'post', 'delta', 'hake_g', 'paas_r', 'clt_il', 'clt_el', 'clt_gl', 'paas_e']
    corr_matrix = df_raw[corr_cols].corr().round(3)
    corr_matrix.columns = ['P_pre', 'P_post', 'ΔP', 'Hake g', 'Paas R', 'Tải IL', 'Tải EL', 'Tải GL', 'E-score']
    corr_matrix.index = corr_matrix.columns
    st.dataframe(corr_matrix, use_container_width=True)
    st.info("Điểm nhấn: r(Post, Tải EL) = +0,605** (Thử thách mong muốn) và r(Tải EL, Tải GL) = -0,176 (Trực giao đa chiều CLT).")

# TAB 9: DEFENSE COUNCIL SIMULATOR
with tab_council:
    st.subheader("Bộ Câu Hỏi Hội Đồng & Kịch Bản Đối Đáp Khoa Học")
    
    with st.expander("❓ Câu hỏi 1: Về tính tương đương của hai đề thi BM-01 và BM-02?"):
        st.markdown(r"""
        **Chiến lược trả lời:**
        1. **Mục tiêu học phần TPACK:** Khác với kiểm tra môn lý thuyết thuần túy, học phần đo lường năng lực tích hợp sư phạm.
        2. **Cấu trúc đối xứng:** 60% MCQ và 40% SAQ trên cả hai đề.
        3. **Chỉ số Hake g:** Đo lường tỷ lệ tri thức mới tiếp thu được trên phần chưa biết ($g = 0,289$), vượt qua hạn chế của điểm thô $\Delta P$.
        """)
        
    with st.expander("❓ Câu hỏi 2: Về nghịch lý Tải ngoại lai (EL) tương quan dương với Post-test (r = +0,605)?"):
        st.markdown(r"""
        **Chiến lược trả lời:**
        1. **Quy luật Thử thách mong muốn (Bjork, 1994):** EL trung bình chỉ là 2,65/5,0 (dưới trung bình, an toàn). Sự "lúng túng" xuất phát từ các phản biện Socratic của AI.
        2. **Thử sai tích cực (Productive Failure - Kapur, 2016):** Sinh viên tương tác sâu với AI gặp nhiều thử thách nhận thức hơn, từ đó khắc sâu bản chất kỹ thuật và đạt điểm Post-test cao vượt bậc.
        3. **Tính trực giao CLT:** $r(EL, GL) = -0,176$, chứng minh hai thành phần tải nhận thức độc lập và đối kháng chuẩn mực theo Sweller (2019).
        """)

    with st.expander("❓ Câu hỏi 3: Phân công vai trò trong nhóm và đánh giá cá nhân?"):
        st.markdown(r"""
        **Chiến lược trả lời:**
        1. **Phân tán nhận thức nhóm (Järvelä, 2015):** Kỹ sư tương tác AI chiếu màn hình cho cả nhóm cùng thảo luận và vẽ bản vẽ A0.
        2. **Đánh giá cá nhân độc lập:** Cả 27 sinh viên đều làm bài Post-test độc lập trên giấy trong 30 phút, đảm bảo năng lực cá nhân hóa.
        """)

    with st.expander("❓ Câu hỏi 4: Về hiện tượng 9 sinh viên giảm điểm và hệ số Alpha α = 0,9255?"):
        st.markdown(r"""
        **Chiến lược trả lời:**
        1. **Sai số chuẩn CTT:** $\text{SE}_{\text{diff}} = 0,929$ đ, biên độ ngẫu nhiên 95% là $\pm 1,82$ đ. Toàn bộ 9 sinh viên đều có $|\Delta P| \le 1,80 \le 1,82$ đ.
        2. **Minh chứng trắc nghiệm:** 6/9 sinh viên có điểm trắc nghiệm tăng trưởng dương (+0,2 đến +0,8 đ).
        3. **Độ phân hóa thực chất:** 10 câu tự luận đều có $r_{it} \ge 0,4899$ (vượt xa chuẩn $0,30$).
        """)

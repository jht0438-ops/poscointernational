import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="포스코인터내셔널 성장투자·재무여력 분석",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# 공통 스타일
# -----------------------------
st.markdown("""
<style>
.block-container {padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1500px;}
h1, h2, h3 {letter-spacing: -0.02em;}
[data-testid="stMetric"] {
    background: #f7f8fa;
    border: 1px solid #e6e8eb;
    padding: 14px 16px;
    border-radius: 12px;
}

/* 상단 탭 글자가 세로로 잘리지 않도록 탭 높이와 여백 확보 */
div[data-baseweb="tab-list"] {
    gap: 0.35rem;
    padding-top: 0.35rem;
    padding-bottom: 0.35rem;
    align-items: center;
}
button[data-baseweb="tab"] {
    height: auto !important;
    min-height: 3.25rem !important;
    padding: 0.75rem 0.9rem !important;
    overflow: visible !important;
}
button[data-baseweb="tab"] > div {
    line-height: 1.45 !important;
    overflow: visible !important;
    white-space: nowrap !important;
}
div[data-baseweb="tab-border"] {
    bottom: 0 !important;
}
.info-box {
    background: #f7f9fc;
    border: 1px solid #dfe5ec;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 12px;
}
.conclusion-box {
    background: #f5f7f9;
    border-left: 5px solid #4b5563;
    border-radius: 8px;
    padding: 18px 20px;
    margin: 12px 0 22px 0;
}
.small-note {font-size: 0.88rem; color: #667085;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 데이터
# 단위: 억원
# -----------------------------
balance = pd.DataFrame({
    "기간": ["2023", "2024", "2025", "2026 H1"],
    "현금및현금성자산": [11369, 10572, 11715, 12223],
    "매출채권및기타채권": [44675, 45115, 43239, 53266],
    "재고자산": [19588, 20807, 17362, 17059],
    "관계·공동기업투자": [9706, 7258, 7636, 8095],
    "유형자산": [37049, 42406, 50701, 52594],
    "무형자산": [23319, 25530, 32354, 35630],
    "총자산": [166177, 173363, 187530, 204800],
    "총부채": [99930, 99869, 109404, 124723],
    "자본": [66248, 73495, 78127, 80076],
})

debt = pd.DataFrame({
    "기간": ["2023", "2024", "2025", "2026 H1"],
    "단기차입금": [18305, 20683, 23259, 19472],
    "유동성사채": [8767, 11177, 5966, 4486],
    "장기차입금": [12149, 11406, 13712, 17314],
    "사채": [18641, 15671, 17810, 29028],
})
debt["차입금·사채 합계"] = debt[["단기차입금","유동성사채","장기차입금","사채"]].sum(axis=1)

annual_cf = pd.DataFrame({
    "기간": ["2023", "2024", "2025"],
    "영업활동CF": [10764, 8769, 19415],
    "투자활동CF": [-271, -8461, -13297],
    "재무활동CF": [-12254, -1761, -4653],
})

half_cf = pd.DataFrame({
    "기간": ["2025 H1", "2026 H1"],
    "영업활동CF": [11687, 4692],
    "투자활동CF": [-3087, -4985],
    "재무활동CF": [-6324, 1222],
    "반기순이익": [2943, 5246],
    "운전자본조정": [5462, -5443],
    "이자지급": [-1279, -1618],
})

profit = pd.DataFrame({
    "기간": ["2023", "2024", "2025", "2026 H1"],
    "매출액": [331328, 323408, 323736, 180336],
    "영업이익": [11631, 11169, 11653, 7865],
})
profit["영업이익률"] = profit["영업이익"] / profit["매출액"] * 100

net_debt = pd.DataFrame({
    "기간": ["2023", "2024", "2025", "2026 Q1", "2026 H1"],
    "순차입금비율": [70.2, 65.8, 62.8, 75.1, 72.5],
    "EBITDA": [16950, 16350, 16900, None, None]
})

segment_2024 = pd.DataFrame({
    "사업": ["GAS(E&P)", "터미널·발전", "철강", "친환경소재", "식량·바이오", "투자법인", "트레이딩법인·연결 등"],
    "매출액": [8810, 31600, 110850, 86810, 38090, 24620, 22630],
    "영업이익": [3820, 2310, 1550, 1110, 140, 550, 1690]
})
segment_2025 = pd.DataFrame({
    "사업": ["GAS(E&P)", "터미널·발전", "Senex 등 종속법인", "철강", "소재·바이오", "인니팜 등 종속법인"],
    "매출액": [6510, 28920, 4510, 145470, 88310, 50020],
    "영업이익": [3560, 1720, 980, 2370, 700, 2320]
})
segment_h1_2026 = pd.DataFrame({
    "사업": ["E&P", "철강", "소재·바이오", "트레이딩법인", "투자법인", "인니팜", "발전", "Senex"],
    "영업이익": [2163, 1124, 498, 733, 1463, 1101, 809, 645]
})

investment = pd.DataFrame({
    "기간": ["2025", "2026 H1"],
    "전체": [15617, 8902],
    "에너지": [6890, 3860],
    "식량·바이오": [6989, 4196]
})

investment_cf_detail = pd.DataFrame({
    "항목": ["유형자산 취득", "무형자산 취득", "관계기업투자 취득", "기타 금융자산 등"],
    "2025 H1": [3923, 2076, 0, 1174],
    "2026 H1": [2598, 2531, 80, 801]
})

financing_h1_2026 = pd.DataFrame({
    "항목": ["장기차입금 신규 차입", "사채 발행", "단기차입금 순감소", "장기·유동성차입금 상환", "유동성사채 상환", "배당금 지급"],
    "현금흐름": [5799, 11994, -5010, -2586, -2800, -1704]
})

def top_explanation(why, how, conclusion):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 왜 분석하나요?")
        st.markdown(f'<div class="info-box">{why}</div>', unsafe_allow_html=True)
    with c2:
        st.markdown("### 어떻게 분석하나요?")
        st.markdown(f'<div class="info-box">{how}</div>', unsafe_allow_html=True)
    st.markdown("### 이 탭에서 얻을 수 있는 결론은 무엇인가요?")
    st.markdown(f'<div class="conclusion-box">{conclusion}</div>', unsafe_allow_html=True)

def source_note(text):
    st.markdown(f'<div class="small-note">자료: {text}</div>', unsafe_allow_html=True)


# -----------------------------
# 투자후보 평가용 데이터
# 최신 비교는 2026년 2Q IR의 동일 분기 수치를 우선 사용
# 에너지 매출/영업이익은 미얀마·SENEX·터미널·발전 핵심 세부사업 합계 proxy
# -----------------------------
candidates = pd.DataFrame({
    "후보": ["에너지", "인니팜", "구동모터코아", "철강"],
    "2026Q2 매출": [8192, 2341, 896, 39114],
    "2026Q2 영업이익": [2301, 768, 100.9, 526],
    "2026Q2 영업이익률": [28.1, 32.8, 11.3, 1.3],
    "YoY 영업이익증감률": [36.8, 91.5, 47.3, -37.9],
    # 정성등급은 분석자가 IR을 검토해 사전에 부여하며 자동 추론하지 않음.
    "구조적원인등급": [5, 4, 4, 2],
    "투자성과등급": [5, 4, 4, 2],
})

# ① 현재 수익성 35점: 이익 규모 18점 + 이익률 17점
size_points = {1: 18, 2: 14, 3: 10, 4: 6}
margin_points = {1: 17, 2: 13, 3: 9, 4: 5}
candidates["이익규모점수"] = candidates["2026Q2 영업이익"].rank(ascending=False, method="min").astype(int).map(size_points)
candidates["이익률점수"] = candidates["2026Q2 영업이익률"].rank(ascending=False, method="min").astype(int).map(margin_points)
candidates["수익성점수"] = candidates["이익규모점수"] + candidates["이익률점수"]

# ② 이익 지속가능성 35점: 반복 가능한 이익의 원인만 평가.
# YoY 증가율과 투자 후 성과는 여기서 중복 채점하지 않음.
candidates["지속가능성점수"] = candidates["구조적원인등급"] * 7

# ③ 기존 투자성과 30점: 투자 집행 → 생산/판매 → 이익 연결의 확인 정도.
# 향후 계획은 점수에 포함하지 않음.
candidates["투자성과점수"] = candidates["투자성과등급"] * 6
candidates["총점"] = candidates[["수익성점수", "지속가능성점수", "투자성과점수"]].sum(axis=1)
candidates["순위"] = candidates["총점"].rank(ascending=False, method="min").astype(int)

assessment_reasons = {
    "에너지": {
        "지속가능성": "미얀마 가스전, SENEX, LNG터미널·발전 등 이익원이 다변화되어 있고 생산·운영 기반이 확인됨. 다만 가격·환율 및 지역 위험은 남음.",
        "투자성과": "SENEX 증산투자 이후 2026 Q2 판매량 80→107억cf, 영업이익 99→332억원. 투자와 운영성과의 연결이 비교적 명확함."
    },
    "인니팜": {
        "지속가능성": "농장 확보와 FFB 생산 회복은 반복 가능한 기반이나 CPO 가격 상승과 인수기업 연결 편입 효과도 커 4등급.",
        "투자성과": "PT PAR 인수 후 연결 실적 확대는 확인되지만 관찰기간이 짧고 인수가격 대비 투자수익률은 검증되지 않아 4등급."
    },
    "구동모터코아": {
        "지속가능성": "수율·Loss율 개선에 따른 제조원가 절감은 구조적 개선. 전기차 수요와 가동률 변동 위험이 있어 4등급.",
        "투자성과": "생산거점 확대와 판매·원가 개선 성과가 나타나지만 설비별 투자수익률은 확인되지 않아 4등급."
    },
    "철강": {
        "지속가능성": "매출 규모는 크지만 낮은 이익률과 철강 시황·환율에 따른 이익 변동성이 커 2등급.",
        "투자성과": "최근 성장투자가 생산·판매·이익 증가로 이어졌다는 직접 근거가 상대적으로 약해 2등급."
    },
}

cause_detail = {
    "에너지": [
        "미얀마 가스전: 2025년 판매량 1,663→1,745억cf, 환율 상승과 함께 영업이익 3,710→3,920억원.",
        "SENEX: 증산설비 가동 효과가 본격화. 2026 Q2 판매량 80→107억cf(+33.8%), 영업이익 99→332억원(+235%).",
        "LNG터미널: 2026 Q2 매출은 11% 감소했지만 계약조건 갱신·정비 효율화로 영업이익 100→113억원(+13%).",
        "발전: 2026 Q2 발전 이용률은 하락했지만 발전 포트폴리오 최적화로 영업이익 172→375억원(+118%).",
        "판단: 기존 고수익원인 미얀마에 SENEX 증산성과와 Mid·Downstream 수익성 개선이 더해져 구조적 이익원인이 가장 다양함."
    ],
    "인니팜": [
        "PT PAR 인수: 2026년 2월 지분 98.7% 확보, 취득금액 약 1조 2,447억원. 인도네시아 팜 사업 시너지 확대 목적.",
        "2026 Q2 매출 953→2,341억원(+145.6%), 영업이익 401→768억원(+91.5%).",
        "회사 설명상 FFB 생산량 회복과 CPO 판가 상승이 매출·이익 확대에 기여.",
        "수율 개선에 따른 원가절감도 이익 상승 요인으로 확인되어 가격효과만으로 설명되지 않음.",
        "CPO 판매량은 2024년 19만톤, 2025년 19만톤, 2026년 전망 55만톤(회사 전망). 인수 연결 편입 효과와 기존 농장 생산성 개선을 구분해야 함."
    ],
    "구동모터코아": [
        "2024 Q2 전기차 수요부진과 인도 지연으로 영업이익 -1.2억원.",
        "2025 Q1 해외 판매량 +46.7%, 전체 판매량 +9.0%와 공정개선·Loss율 개선으로 영업이익 27.8억원 흑자전환.",
        "2026 Q2 영업이익 68.5→100.9억원(+47.3%). 소재 수율 개선에 따른 원가절감이 이익 상승에 기여.",
        "2026년 회사의 구동모터코아 판매 확대계획은 참고하되, 미래 계획은 이번 평가점수에 가산하지 않음.",
        "판단: 현재 절대 이익규모는 작지만 판매 확대와 제조원가 개선이 동시에 나타나는 성장후보."
    ],
    "철강": [
        "2025년 매출 14조 5,470억원, 영업이익 2,370억원으로 외형 대비 영업이익률은 낮은 구조.",
        "2026 Q2 매출 3조 9,114억원으로 YoY +6.3%였지만 영업이익은 526억원으로 -37.9%.",
        "2026 Q2 이익 감소에는 EUR 대비 USD 강세에 따른 이종통화 거래이익 감소가 영향을 미침.",
        "2025 Q1에도 철강 시황 하락으로 매출 +3.2%에도 영업이익 -16.2%를 기록.",
        "판단: 대규모 매출·그룹 공급망 역할은 강점이나 제한된 추가 자본은 외형확대보다 수익성·운전자본 개선에 우선 배분."
    ]
}

st.title("포스코인터내셔널 성장투자·재무여력 및 자원배분 분석")
st.caption("재무제표 → 투자여력 → 사업별 이익 원인 → 투자성과 → 점수화 → 투자 우선순위")

# 탭 잘림 문제를 피하고 분석 흐름을 명확히 하기 위해 사이드바 탐색 사용
page = st.sidebar.radio(
    "분석 단계",
    ["개요", "1. 자산구조와 성장투자", "2. 이익과 영업현금흐름", "3. 투자재원과 재무부담",
     "4. 사업별 수익성", "5. 이익 원인분해", "6. 투자성과", "7. 평가기준과 배점",
     "8. 투자후보 자동채점", "최종결론"]
)

if page == "개요":
    st.header("개요")
    st.markdown("### 핵심 질문")
    st.info("성장투자를 확대하는 상황에서 현재 재무여력은 어떠하며, 한정된 자원을 에너지·인니팜·구동모터코아·철강 중 어디에 우선 배분해야 하는가?")
    st.markdown("### 분석 흐름")
    st.write("1. 재무상태표에서 유형·무형자산 증가를 확인해 성장투자 확대를 파악합니다.")
    st.write("2. 손익계산서와 현금흐름표를 연결해 이익이 실제 영업현금으로 전환되는지 확인합니다.")
    st.write("3. 투자활동CF와 차입금·사채를 연결해 투자재원의 조달구조와 재무부담을 확인합니다.")
    st.write("4. 네 투자후보의 매출·영업이익·영업이익률을 비교하고, IR의 생산·판매·가격·원가 요인으로 이익의 원인을 분해합니다.")
    st.write("5. 동일한 평가기준을 적용해 100점 만점으로 자동채점하고 최종 투자 우선순위를 도출합니다.")
    st.markdown("### 재무제표 활용 포인트")
    st.write("재무상태표: 유형자산·무형자산·매출채권·현금·차입금·사채")
    st.write("손익계산서: 매출액·영업이익·영업이익률")
    st.write("현금흐름표: 영업활동CF·투자활동CF·재무활동CF·운전자본조정·유형/무형자산 취득")
    st.write("IR: 사업별 손익의 원인을 생산량·판매량·가격·가동률·수율·M&A 효과로 분해")

elif page == "1. 자산구조와 성장투자":
    st.header("1. 자산구조와 성장투자")
    top_explanation(
        "성장투자가 실제로 집행되고 있다면 재무상태표의 비유동자산과 현금흐름표의 투자지출에 흔적이 남습니다.",
        "2023~2026 H1 유형자산·무형자산과 총자산을 비교하고, 뒤 단계에서 현금흐름표의 취득지출과 연결합니다.",
        "유형자산은 2023년 3조 7,049억원에서 2026 H1 5조 2,594억원, 무형자산은 2조 3,319억원에서 3조 5,630억원으로 증가했습니다. 성장투자가 계획이 아니라 실제 자산 증가로 이어지고 있음을 확인할 수 있습니다."
    )
    asset_long = balance.melt(id_vars="기간", value_vars=["유형자산","무형자산","관계·공동기업투자"], var_name="자산", value_name="금액")
    fig = px.bar(asset_long, x="기간", y="금액", color="자산", barmode="group", title="성장 관련 자산 추이")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(balance.set_index("기간"), use_container_width=True)
    source_note("2024·2025 사업보고서, 2026 반기보고서 연결재무제표")

elif page == "2. 이익과 영업현금흐름":
    st.header("2. 이익과 영업현금흐름")
    top_explanation(
        "발생주의 회계상 이익이 증가해도 실제 현금이 같은 속도로 들어오지 않을 수 있습니다. 투자여력을 판단하려면 순이익과 영업현금흐름을 함께 봐야 합니다.",
        "2025 H1과 2026 H1의 순이익·영업활동CF·운전자본조정을 비교하고 매출채권 변화를 재무상태표와 연결합니다.",
        "2026 H1 순이익은 5,246억원으로 증가했지만 영업활동CF는 4,692억원으로 감소했습니다. 운전자본조정이 +5,462억원에서 -5,443억원으로 바뀌었고 매출채권 및 기타채권이 2025년 말 4조 3,239억원에서 2026 H1 5조 3,266억원으로 증가했습니다. 이익의 현금전환 속도가 투자여력의 핵심 변수가 됐습니다."
    )
    cf_show = half_cf[["기간","영업활동CF","반기순이익","운전자본조정"]].melt(id_vars="기간", var_name="항목", value_name="금액")
    st.plotly_chart(px.bar(cf_show, x="기간", y="금액", color="항목", barmode="group", title="이익과 영업현금흐름 비교"), use_container_width=True)
    st.dataframe(half_cf.set_index("기간"), use_container_width=True)
    source_note("2025·2026 반기보고서 연결현금흐름표 및 연결재무상태표")

elif page == "3. 투자재원과 재무부담":
    st.header("3. 투자재원과 재무부담")
    top_explanation(
        "성장투자를 지속하려면 투자지출을 영업현금으로 감당하는지, 외부조달 의존도가 커지는지를 확인해야 합니다.",
        "영업·투자·재무활동CF를 연결하고 차입금·사채 잔액, 2026 H1 신규 장기차입과 사채 발행을 함께 봅니다.",
        "2025년에는 영업활동CF 1조 9,415억원이 투자활동 순유출 1조 3,297억원을 상회했지만, 2026 H1에는 영업활동CF 4,692억원보다 투자활동 순유출 4,985억원이 컸습니다. 같은 기간 장기차입과 사채 발행이 확대되어 투자 중단보다 선별적인 자본배분의 중요성이 커졌다고 판단합니다."
    )
    cf_all = pd.concat([annual_cf, half_cf[["기간","영업활동CF","투자활동CF","재무활동CF"]]], ignore_index=True)
    cf_long = cf_all.melt(id_vars="기간", var_name="현금흐름", value_name="금액")
    st.plotly_chart(px.bar(cf_long, x="기간", y="금액", color="현금흐름", barmode="group", title="영업·투자·재무활동 현금흐름"), use_container_width=True)
    st.plotly_chart(px.line(debt, x="기간", y="차입금·사채 합계", markers=True, title="차입금·사채 합계"), use_container_width=True)
    st.markdown("### 2026 H1 주요 재무활동")
    st.dataframe(financing_h1_2026.set_index("항목"), use_container_width=True)
    source_note("2024·2025 사업보고서, 2025·2026 반기보고서")

elif page == "4. 사업별 수익성":
    st.header("4. 사업별 수익성")
    top_explanation(
        "매출규모가 큰 사업과 실제 이익을 잘 만드는 사업은 다를 수 있습니다. 투자후보를 동일한 기준으로 비교하기 위한 첫 단계입니다.",
        "2025 연간 사업별 손익과 2026 H1/Q2 최신 손익을 사용해 영업이익 규모와 영업이익률을 함께 봅니다.",
        "에너지는 높은 절대 이익과 높은 수익성을 동시에 보이고, 인니팜은 2026년 이익이 빠르게 확대되고 있습니다. 모터코아는 절대 이익은 작지만 흑자전환 이후 개선 중이며, 철강은 가장 큰 매출규모에 비해 이익률이 낮아 추가 외형투자보다 수익성 개선의 우선도가 높습니다."
    )
    latest = candidates[["후보","2026Q2 매출","2026Q2 영업이익","2026Q2 영업이익률"]].copy()
    c1,c2=st.columns(2)
    with c1:
        st.plotly_chart(px.bar(latest.sort_values("2026Q2 영업이익"), x="2026Q2 영업이익", y="후보", orientation="h", title="2026 Q2 영업이익 비교"), use_container_width=True)
    with c2:
        st.plotly_chart(px.bar(latest.sort_values("2026Q2 영업이익률"), x="2026Q2 영업이익률", y="후보", orientation="h", title="2026 Q2 영업이익률 비교"), use_container_width=True)
    st.dataframe(latest.set_index("후보").style.format({"2026Q2 매출":"{:,.0f}","2026Q2 영업이익":"{:,.1f}","2026Q2 영업이익률":"{:.1f}%"}), use_container_width=True)
    st.caption("에너지는 미얀마·SENEX·터미널·발전 핵심 세부사업 합계 proxy로 비교합니다. 사업별 공시체계 차이를 숨기지 않고 화면에 명시합니다.")
    source_note("2025 FY, 2026 Q2 실적발표 자료")

elif page == "5. 이익 원인분해":
    st.header("5. 이익 원인분해")
    top_explanation(
        "높은 이익만 보고 투자하면 가격·환율 같은 일시적 외부효과를 구조적 경쟁력으로 오해할 수 있습니다.",
        "각 후보의 영업이익 변화를 생산·판매량, 가격·환율, 원가·수율, 가동률·계약, M&A 효과로 분해합니다. 지속가능성은 반복 가능한 이익의 구조만 평가하고, 과거 투자집행의 성과는 별도 항목에서 평가합니다.",
        "에너지는 미얀마의 높은 이익기반에 SENEX 증산성과와 터미널·발전 수익성 개선이 더해졌습니다. 인니팜은 신규 농장 편입, FFB 생산 회복, 수율 개선, CPO 판가 상승이 함께 작용했습니다. 모터코아는 판매량 확대와 Loss율·수율 개선이 이익 회복으로 이어졌습니다. 철강은 매출 증가에도 시황·환율 영향으로 이익 변동성이 상대적으로 크게 나타났습니다."
    )
    selected = st.selectbox("투자후보 선택", ["에너지","인니팜","구동모터코아","철강"])
    st.markdown(f"### {selected}: 왜 이익이 변했는가?")
    for i, line in enumerate(cause_detail[selected], 1):
        st.write(f"{i}. {line}")
    st.markdown("### 점수에 반영되는 방식")
    st.write("수율·원가 개선, 장기 계약 기반, 이익원 다변화처럼 반복 가능한 요인은 지속가능성에 반영합니다. 투자 이후 생산·판매 확대 성과는 투자성과에서 별도로 평가합니다.")
    st.write("가격·환율·SMP 등 외부변수만으로 설명되는 이익은 상대적으로 낮게 평가합니다. 여러 원인이 섞여 있으면 구조적 요인이 실제 숫자로 확인되는 정도를 기준으로 평가합니다.")
    source_note("2024~2026 Q2 IR의 사업별 주요 이익 및 지표 변동 내역")

elif page == "6. 투자성과":
    st.header("6. 기존 투자성과")
    top_explanation(
        "이미 집행한 자본이 실제 운영성과로 연결됐는지 확인하기 위해 분석합니다.",
        "투자·인수·증설 이후 생산량·판매량·영업이익 변화를 연결합니다. 인수 후 연결 실적 증가를 투자수익률 확정으로 해석하지 않습니다.",
        "SENEX는 증산투자와 판매량·영업이익 증가의 연결이 뚜렷합니다. 인니팜은 PT PAR 인수 후 연결 실적 확대가 확인되지만 투자수익률은 추가 검증이 필요합니다."
    )
    inv_long = investment.melt(id_vars="기간", var_name="구분", value_name="투자집행액")
    st.plotly_chart(px.bar(inv_long, x="기간", y="투자집행액", color="구분", barmode="group", title="전사 및 주요 성장영역 투자집행"), use_container_width=True)
    st.markdown("### 현금흐름표상 주요 투자지출")
    st.dataframe(investment_cf_detail.set_index("항목"), use_container_width=True)
    st.caption("전사·사업군 투자집행액은 후보별 ROIC나 투자수익률을 직접 뜻하지 않습니다.")
    st.markdown("### 투자성과 5단계 판정 규칙")
    for rule in [
        "5등급: 투자 집행 → 생산·판매 증가 → 영업이익 증가의 연결이 명확",
        "4등급: 투자 후 운영성과는 나타났지만 관찰기간·검증이 제한적",
        "3등급: 투자·가동은 확인되지만 운영성과는 초기 단계",
        "2등급: 투자와 운영성과의 직접 연결 근거가 약함",
        "1등급: 투자 확대 이후에도 운영성과 악화가 확인됨",
    ]:
        st.write(rule)
    st.dataframe(candidates[["후보", "투자성과등급", "투자성과점수"]].set_index("후보"), use_container_width=True)
    source_note("연결재무제표·현금흐름표, 2025 FY·2026 Q1·Q2 IR. 등급은 분석자 입력값")

elif page == "7. 평가기준과 배점":
    st.header("7. 평가기준과 배점")
    top_explanation(
        "이익 증가와 투자성과를 여러 항목에서 중복 채점하는 문제를 줄이기 위해서입니다.",
        "현재 수익성 35점, 이익 지속가능성 35점, 기존 투자성과 30점으로 100점을 구성합니다.",
        "지금 얼마나 버는가(수익성), 그 이익이 반복 가능한 구조인가(지속가능성), 과거 투자가 성과로 이어졌는가(투자성과)를 구분합니다. 미래 계획은 점수에 가산하지 않습니다."
    )
    weights = pd.DataFrame({
        "평가항목": ["현재 수익성", "이익 지속가능성", "기존 투자성과"],
        "배점": [35, 35, 30],
        "세부산식": ["영업이익 규모 18 + 영업이익률 17", "구조적 원인 등급(1~5) × 7", "투자성과 등급(1~5) × 6"],
        "중복 방지": ["현재 이익 수준만 평가", "반복 가능한 이익의 원인만 평가", "실제 투자 이후 운영성과만 평가"],
    })
    st.dataframe(weights.set_index("평가항목"), use_container_width=True)
    st.markdown("### 산식 상세")
    st.write("수익성: 영업이익 규모 순위 1~4위에 18·14·10·6점, 영업이익률 순위에 17·13·9·5점 부여")
    st.write("지속가능성: 수율·원가 개선, 장기 계약 기반, 이익원 다변화와 외부 변수 의존도를 종합해 5등급 × 7점")
    st.write("투자성과: 실제 투자 → 생산·판매 → 영업이익의 연결 검증 정도를 5등급 × 6점")
    st.warning("정성 등급은 IR에 근거한 분석자의 사전 입력값입니다. 공시자료를 실시간으로 읽어 자동 판정하는 것은 아닙니다.")
    st.markdown("### 전사 재무여력은 왜 점수에서 제외했나요?")
    st.write("영업CF·투자CF·차입금·운전자본은 네 사업이 공유하는 전사 자금제약이므로 후보별 점수에 중복 반영하지 않습니다.")

elif page == "8. 투자후보 자동채점":
    st.header("8. 투자후보 자동채점")
    top_explanation(
        "네 사업에 동일한 평가기준을 적용해 추가 자본배분의 상대적 근거를 비교합니다.",
        "수익성 35점 + 지속가능성 35점 + 기존 투자성과 30점을 합산합니다. 정성 등급과 그 근거를 공개합니다.",
        "현재 입력된 재무수치와 정성 등급을 적용한 결과입니다. 공식 투자순위나 ROIC·IRR을 뜻하지 않습니다."
    )
    ranking = candidates.sort_values(["총점", "수익성점수"], ascending=False).copy()
    score_cols = ["후보", "수익성점수", "지속가능성점수", "투자성과점수", "총점", "순위"]
    st.dataframe(ranking[score_cols].set_index("순위"), use_container_width=True)
    score_long = ranking.melt(id_vars=["후보"], value_vars=["수익성점수", "지속가능성점수", "투자성과점수"], var_name="평가항목", value_name="점수")
    st.plotly_chart(px.bar(score_long, x="후보", y="점수", color="평가항목", title="투자후보별 100점 구성"), use_container_width=True)
    selected = st.selectbox("점수 근거 확인", ranking["후보"].tolist())
    row = ranking[ranking["후보"] == selected].iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("총점", f"{row['총점']:.0f}/100")
    c2.metric("수익성", f"{row['수익성점수']:.0f}/35")
    c3.metric("지속가능성", f"{row['지속가능성점수']:.0f}/35")
    c4.metric("투자성과", f"{row['투자성과점수']:.0f}/30")
    with st.expander("① 현재 수익성", expanded=True):
        st.write(f"2026 Q2 영업이익 {row['2026Q2 영업이익']:,.1f}억원 → {row['이익규모점수']:.0f}/18")
        st.write(f"2026 Q2 영업이익률 {row['2026Q2 영업이익률']:.1f}% → {row['이익률점수']:.0f}/17")
    with st.expander("② 이익 지속가능성"):
        st.write(f"구조적 원인 {row['구조적원인등급']:.0f}/5등급 → {row['지속가능성점수']:.0f}/35")
        st.write(assessment_reasons[selected]["지속가능성"])
    with st.expander("③ 기존 투자성과"):
        st.write(f"투자성과 {row['투자성과등급']:.0f}/5등급 → {row['투자성과점수']:.0f}/30")
        st.write(assessment_reasons[selected]["투자성과"])
    source_note("2024~2026 Q2 IR, 사업보고서·반기보고서; 분석자 입력 정성 등급과 고정 산식")

elif page == "최종결론":
    st.header("최종결론")
    st.markdown("## 재무여력과 사업성과를 함께 고려한 자원배분")
    ranking = candidates.sort_values(["총점", "수익성점수"], ascending=False).copy()
    st.markdown("### 1. 왜 선별적인 투자가 필요한가")
    st.write("2025년 영업활동CF 1조 9,415억원이 투자활동 순유출 1조 3,297억원을 상회했지만, 2026 H1 영업활동CF 4,692억원은 투자활동 순유출 4,985억원보다 작았습니다. 따라서 성장투자의 우선순위를 선별할 필요가 있습니다.")
    st.markdown("### 2. 무엇을 기준으로 골랐는가")
    st.write("현재 수익성 35점, 이익 지속가능성 35점, 기존 투자성과 30점으로 평가했습니다. 단순 이익 증가율과 미래 확대계획은 중복 가산하지 않았습니다.")
    st.markdown("### 3. 최종 투자 우선순위")
    st.dataframe(ranking[["순위", "후보", "수익성점수", "지속가능성점수", "투자성과점수", "총점"]].set_index("순위"), use_container_width=True)
    winner, second = ranking.iloc[0], ranking.iloc[1]
    st.success(f"1순위 {winner['후보']} {winner['총점']:.0f}점, 2순위 {second['후보']} {second['총점']:.0f}점")
    st.markdown("### 4. 상위 사업의 평가 근거")
    for name in [winner["후보"], second["후보"]]:
        st.markdown(f"**{name}**")
        st.write("지속가능성:", assessment_reasons[name]["지속가능성"])
        st.write("투자성과:", assessment_reasons[name]["투자성과"])
    st.markdown("### 5. 최종 제언")
    st.write("에너지는 기존 이익창출력과 SENEX 증산투자 성과를 바탕으로 우선 검토합니다. 인니팜은 높은 이익률과 인수 후 실적 확대가 강점이나 CPO 가격효과 및 투자회수 성과를 추가 검증해야 합니다. 구동모터코아는 가동률·수율을 확인하며 단계적으로 투자하고, 철강은 외형 확대보다 수익성 및 운전자본 개선을 우선합니다.")
    st.markdown("### 6. 회계·재무 관점에서의 의미")
    st.write("전사 현금흐름으로 투자여력을 파악한 뒤, 사업별 현재 이익 수준·반복 가능한 수익구조·과거 투자 이후 성과를 구분해 평가했습니다. 실제 투자 승인에는 투자안별 현금흐름·ROIC·NPV 검증이 필요합니다.")
    st.caption("2026 수치는 H1 누적 또는 Q2 기준입니다. 에너지는 핵심 세부사업 합계 proxy이며 정성 등급은 분석자 판단입니다.")

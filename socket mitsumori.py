import streamlit as st

# --- 页面设置 ---
st.set_page_config(page_title="ソケット基板报价系统", layout="centered")

st.title("🏿ソケット基板見積システム")
st.markdown("---")

# --- 1. 侧边栏：参数设定 (默认折叠) ---
with st.sidebar:
    st.header("⚙️ 内部係数設定")
    # Streamlit 自带持久化，刷新网页会恢复默认，但部署后用户可调
    mat_markup = st.number_input("部材係数", value=1.2, step=0.1)
    profit_markup = st.number_input("利潤係数", value=1.2, step=0.1)
    
    st.markdown("---")
    rate_domestic = st.number_input("国内費用 (円/h)", value=6000, step=500)
    rate_overseas = st.number_input("海外費用 (円/h)", value=10000, step=500)
    
    st.info("注: 変更されたサイドバー パラメータは、計算にリアルタイムで適用されます。")

# --- 2. 主界面：输入区域 ---
col1, col2 = st.columns(2)

with col1:
    mat_cost = st.number_input("部材費入力 (単位:円)", min_value=0.0, step=100.0)

with col2:
    work_hours = st.number_input("作業時間入力 (単位:h)", min_value=0.0, step=0.5)

region = st.radio("地域", ["国内", "海外"], horizontal=True)

# --- 3. 计算逻辑 ---
if st.button("価格見積", type="primary"):
    if mat_cost > 0 and work_hours > 0:
        # 获取费率
        labor_rate = rate_domestic if region == "国内" else rate_overseas
        
        # 公式: (材料费*系数 + 时间*费率) * 利润系数
        mat_part = mat_cost * mat_markup
        labor_part = work_hours * labor_rate
        total_price = (mat_part + labor_part) * profit_markup
        
        # --- 4. 结果展示 ---
        st.success(f"### 最終価格: ¥{total_price:,.0f}")
        
        with st.expander("内訳の確認"):
            st.write(f"- **部材費(係数含む):** ¥{mat_part:,.0f}")
            st.write(f"- **作業費用({region}):** ¥{labor_part:,.0f}")
            st.write(f"- **利潤を反映した価格:** ¥{total_price:,.0f}")
            st.caption(f"計算基準：部材係数 {mat_markup}, 利潤係数 {profit_markup}, 地域費用 ¥{labor_rate}/h")
    else:
        st.warning("上記に有効な部材費と作業時間を入力してください。")

# --- 5. 页脚 ---
st.markdown("---")
st.caption("©2026 阪和電子工業第一営業部自動化ツール - Powered by Streamlit")
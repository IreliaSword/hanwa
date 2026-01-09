import streamlit as st

# --- 页面设置 ---
st.set_page_config(page_title="ソケット基板报价系统", layout="centered")

st.title("🚀 ソケット基板报价自动化系统")
st.markdown("---")

# --- 1. 侧边栏：参数设定 (默认折叠) ---
with st.sidebar:
    st.header("⚙️ 内部参数设定")
    # Streamlit 自带持久化，刷新网页会恢复默认，但部署后用户可调
    mat_markup = st.number_input("材料系数", value=1.2, step=0.1)
    profit_markup = st.number_input("利润系数", value=1.2, step=0.1)
    
    st.markdown("---")
    rate_domestic = st.number_input("国内费率 (円/h)", value=6000, step=500)
    rate_overseas = st.number_input("海外费率 (円/h)", value=10000, step=500)
    
    st.info("注：侧边栏参数修改后将实时应用于计算。")

# --- 2. 主界面：输入区域 ---
col1, col2 = st.columns(2)

with col1:
    mat_cost = st.number_input("请输入材料费 (单位:円)", min_value=0.0, step=100.0)

with col2:
    work_hours = st.number_input("请输入作业时间 (单位:h)", min_value=0.0, step=0.5)

region = st.radio("项目地区", ["国内", "海外"], horizontal=True)

# --- 3. 计算逻辑 ---
if st.button("生成正式报价单", type="primary"):
    if mat_cost > 0 and work_hours > 0:
        # 获取费率
        labor_rate = rate_domestic if region == "国内" else rate_overseas
        
        # 公式: (材料费*系数 + 时间*费率) * 利润系数
        mat_part = mat_cost * mat_markup
        labor_part = work_hours * labor_rate
        total_price = (mat_part + labor_part) * profit_markup
        
        # --- 4. 结果展示 ---
        st.success(f"### 最终报价: ¥{total_price:,.0f}")
        
        with st.expander("查看计算明细"):
            st.write(f"- **材料成本(含损耗):** ¥{mat_part:,.0f}")
            st.write(f"- **人工成本({region}):** ¥{labor_part:,.0f}")
            st.write(f"- **利润加成后总额:** ¥{total_price:,.0f}")
            st.caption(f"计算基准：材料系数 {mat_markup}, 利润系数 {profit_markup}, 费率 ¥{labor_rate}/h")
    else:
        st.warning("请在上方输入有效的材料费和作业时间。")

# --- 5. 页脚 ---
st.markdown("---")
st.caption("©2024 营业部自动化工具 - Powered by Streamlit")
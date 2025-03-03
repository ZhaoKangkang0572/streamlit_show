import streamlit as st
import json
import os
import pandas as pd

# 设置页面标题
st.set_page_config(page_title="模型回答对比", layout="wide")

# 问题列表
questions = [
    "南京的新用户占比有多少",
    "为什么某些产品的利润率更高",
    "周末与工作日的销售表现有何不同",
    "请对比单车业务线2月和3月解决率波动情况，分析出核心影响的服务问题",
    "申诉量近37天，申诉量每周上涨的标题有哪些",
    "两口价竞争应答率为什么这周比上一周的数值要高，高在哪些地方呢",
]


# 加载特定查询的数据
def load_query_data(query):
    ds_file = f"dummy_data_002/{query}_ds.json"
    qwen_file = f"dummy_data_002/{query}_qwen.json"
    excel_file = f"dummy_data_002/{query}.xlsx"

    ds_data = None
    qwen_data = None
    excel_data = None

    try:
        if os.path.exists(ds_file):
            with open(ds_file, "r", encoding="utf-8") as f:
                ds_data = json.load(f)
    except Exception as e:
        st.error(f"加载 {ds_file} 时出错: {e}")

    try:
        if os.path.exists(qwen_file):
            with open(qwen_file, "r", encoding="utf-8") as f:
                qwen_data = json.load(f)
    except Exception as e:
        st.error(f"加载 {qwen_file} 时出错: {e}")

    try:
        if os.path.exists(excel_file):
            excel_data = pd.read_excel(excel_file)
    except Exception as e:
        st.error(f"加载 {excel_file} 时出错: {e}")

    return ds_data, qwen_data, excel_data


# 创建问题选择器
selected_question = st.selectbox("选择问题", questions)

# 加载选定问题的数据
ds_data, qwen_data, excel_data = load_query_data(selected_question)

# 第一行：显示数据预览
st.markdown("## 数据预览")

if excel_data is not None:
    # 显示数据表格的前五行
    st.markdown("### 前五行数据预览")
    st.dataframe(excel_data.head())

    # 显示数据表格的行数和列数
    rows, cols = excel_data.shape
    st.markdown(f"**数据表格共有 {rows} 行，{cols} 列**")

    # 将数据表格的前五行转换为Markdown格式
    st.markdown("### Markdown表格预览")
    markdown_table = excel_data.head().to_markdown()
    st.markdown(markdown_table)
else:
    st.markdown(f"没有找到 '{selected_question}_ds.xlsx' 数据文件")

# 第二行：显示模型回答
st.markdown("---")
st.markdown("## 模型回答对比")
col1, col2 = st.columns(2)

# 在第一列显示Deepseek R1的回答
with col1:
    st.markdown("### Deepseek R1 回答")
    if ds_data:
        st.markdown(ds_data.get("response", "没有找到回答内容"))
    else:
        st.markdown("没有找到该问题的数据文件")

# 在第二列显示Qwen 2.5 72B的回答
with col2:
    st.markdown("### Qwen 2.5 72B 回答")
    if qwen_data:
        st.markdown(qwen_data.get("response", "没有找到回答内容"))
    else:
        st.markdown("没有找到该问题的数据文件")

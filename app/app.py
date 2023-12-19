import streamlit as st
from rag import RAG

st.title("My Chat App")

rag = RAG()

def generate(query, model_name):
    answer, answer_with_rag = rag.generate(query, model_name)
    return answer, answer_with_rag

def chat_parallel(query, model_name):
    with st.chat_message("user"):
        st.write(query)
    col1, col2 = st.columns(2)
    answer, answer_with_rag = generate(query, model_name)
    with col1:
        st.subheader("RAGなし")
        with st.chat_message("assistant"):
            ans_placeholder = st.empty()
    with col2:
        st.subheader("RAGあり")
        with st.chat_message("assistant"):
            ans_rag_placeholder = st.empty()
    for ans, ans_rag in zip(answer, answer_with_rag):
        ans_placeholder.markdown(ans)
        ans_rag_placeholder.markdown(ans_rag)

def chat(query, model_name):
    with st.chat_message("user"):
        st.write(query)
    col1, col2 = st.columns(2)
    answer, answer_with_rag = generate(query, model_name)
    with col1:
        st.subheader("RAGなし")
        with st.chat_message("assistant"):
            ans_placeholder = st.empty()
            with st.spinner("Generating Answer..."):
                for ans in answer:
                    ans_placeholder.markdown(ans)
    with col2:
        st.subheader("RAGあり")
        with st.chat_message("assistant"):
            ans_rag_placeholder = st.empty()
            with st.spinner("Generating Answer..."):
                for ans in answer_with_rag:
                    ans_rag_placeholder.markdown(ans)

def image_window(query):
    with st.chat_message("user"):
        st.write(query)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        image_rag = RAG(core_name="image", lang="multilingual")
        answer, filename = image_rag.generate_image_caption(query)
        for ans in answer:
            placeholder.markdown(ans)
        if filename:
            st.image(f"./img/{filename}", use_column_width=True)
        else:
            st.warning("filename is empty.")

def main():
    model_name = st.selectbox("使用するモデルを選んでください", ("Calm2", "Rinna"))
    query = st.chat_input("ex. Solrでのベクトル検索の始め方を教えてください。")
    if query:
        #chat(query, model_name)
        image_window(query)

if __name__ == "__main__":
    main()

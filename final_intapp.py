import streamlit as st
import time
from final_int_env import chain

# -------------------------------
# Streamlit UI Setup
# -------------------------------
st.set_page_config(page_title="NL2SQL", page_icon="💡", layout="wide")

st.title("💡 NL2SQL with Gemini + FAISS")
st.caption("Type your natural language question and get the corresponding SQL answer.")

# -------------------------------
# Initialize Session State
# -------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Render previous chat messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------
# Handle User Input
# -------------------------------
if user_query := st.chat_input("Type your question here..."):
    # Store and display user message
    st.session_state["messages"].append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Assistant response area
    with st.chat_message("assistant"):
        with st.spinner("🔍 Generating SQL and fetching results..."):
            time.sleep(0.5)  # small delay for smoother UI feedback

            try:
                # Invoke the full chain pipeline
                response = chain.invoke({"question": user_query})
                
                # Handle possible structure variations
                if isinstance(response, dict):
                    final_answer = (
                        response.get("answer", "⚠️ No answer generated.")
                    )
                    if hasattr(final_answer, "content"):
                        final_answer = final_answer.content
                else:
                    final_answer = str(response)

                st.success("✅ Query processed successfully!")
                st.markdown(final_answer)

            except Exception as e:
                # Log the error to the console for developers
                import traceback
                print("Error Traceback:\n", traceback.format_exc())

                final_answer = f"⚠️ **An error occurred while processing your request:**\n\n```\n{e}\n```"
                st.error(final_answer)

            # Save assistant message in session state
            st.session_state["messages"].append(
                {"role": "assistant", "content": final_answer}
            )

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("Built with ❤️ Jaiganesh Mabbu by [Dothis](https://dothis.ai)")

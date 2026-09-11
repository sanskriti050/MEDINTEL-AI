import streamlit as st
import os
from groq import Groq
from config import get_groq_api_key


def show_debug():
    st.title("🔧 Debug Test")

    # Check where key is coming from
    key = get_groq_api_key()

    # Also show source for debugging
    try:
        secrets_key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        secrets_key = ""

    env_key = os.getenv("GROQ_API_KEY", "")

    if secrets_key:
        st.success(f"✅ Key source: **st.secrets** → {secrets_key[:8]}...{secrets_key[-4:]}")
    elif env_key:
        st.success(f"✅ Key source: **.env file** → {env_key[:8]}...{env_key[-4:]}")
    else:
        st.error("❌ GROQ_API_KEY NOT FOUND in either st.secrets or environment!")
        st.warning("""
**To fix on Streamlit Cloud:**
1. Go to your app on share.streamlit.io
2. Click ⋮ → **Settings** → **Secrets**
3. Add this exactly:
```
GROQ_API_KEY = "your_key_here"
```
4. Save and reboot the app
        """)
        return

    if key:
        st.info(f"🔑 Active key: `{key[:8]}...{key[-4:]}`")
    else:
        st.error("❌ get_groq_api_key() returned empty string!")
        return

    # Test actual API call
    if st.button("🧪 Test Groq API Call"):
        try:
            client = Groq(api_key=key)
            response = client.chat.completions.create(
                model="qwen/qwen3.8-27b",
                messages=[{"role": "user", "content": "Say 'API works!' in exactly those words."}],
                max_tokens=20
            )
            result = response.choices[0].message.content
            st.success(f"✅ API Response: {result}")
        except Exception as e:
            st.error(f"❌ API Error: {str(e)}")

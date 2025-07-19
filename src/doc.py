import streamlit as st

TEXT = st.session_state.text  # already injected in main.py

st.markdown(TEXT["doc_welcome"])

# ------------------------------------------------------------------
# 1. Quick-start cards
# ------------------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(TEXT["step1_card"])

with col2:
    st.markdown(TEXT["step2_card"])

with col3:
    st.markdown(TEXT["step3_card"])

# ------------------------------------------------------------------
# 2. Interactive mini-tour
# ------------------------------------------------------------------
with st.expander(TEXT["mini_tour"], expanded=True):
    st.markdown(TEXT["tour_steps"])

# ------------------------------------------------------------------
# 3. Formula reference
# ------------------------------------------------------------------
st.markdown("---")
st.subheader(TEXT["formula_ref"])
st.latex(r"M_c = \frac{\rho  \cdot D^2}{1273}")
st.markdown(TEXT["formula_explainer"])

# ------------------------------------------------------------------
# 4. FAQ
# ------------------------------------------------------------------
with st.expander(TEXT["faq_title"], expanded=False):
    st.markdown(TEXT["faq_body"])

# ------------------------------------------------------------------
# 5. Need help?
# ------------------------------------------------------------------
st.markdown(TEXT["support"])

# ------------------------------------------------------------------
# 6. Author 
# ------------------------------------------------------------------

st.image("assets/profile.jpeg", caption="Nasser K.", width=256)
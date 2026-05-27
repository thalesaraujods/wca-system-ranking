import streamlit as st


def render_search_form() -> tuple[str, bool]:
    """
    Render the URL input form.
    Returns (url_value, was_submitted).
    """
    url = st.text_input(
        label="URL da competição",
        placeholder="live.worldcubeassociation.org/competitions/…",
        help="Cole o link direto do WCA Live",
        key="url_input",
        label_visibility="visible",
    )
    submitted = st.button(
        "Analisar competição",
        type="primary",
        width="stretch",
        key="btn_analisar",
    )

    with st.expander("Como obter o URL"):
        st.markdown(
            """
            1. Acesse [WCA Live](https://live.worldcubeassociation.org)
            2. Abra a página da competição desejada
            3. Copie o URL da barra de endereços e cole acima
            """,
            unsafe_allow_html=False,
        )

    return url, submitted


def render_active_competition_bar(competition_name: str) -> bool:
    """
    Render the 'currently viewing' bar when data is loaded.
    Returns True if user clicked 'Nova consulta'.
    """
    st.markdown(
        f'<p class="active-competition-label">Exibindo: '
        f'<strong>{competition_name}</strong></p>',
        unsafe_allow_html=True,
    )
    return st.button(
        "Nova consulta",
        type="secondary",
        width="stretch",
        key="btn_nova_consulta",
    )

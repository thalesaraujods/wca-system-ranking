import streamlit as st
from pathlib import Path


_BANNER_PATH = Path(__file__).parent.parent / "banner-circuito.jpg"


def render_header() -> None:
    # Banner completo em largura total
    if _BANNER_PATH.exists():
        st.image(str(_BANNER_PATH), use_container_width=True)
    else:
        st.markdown(
            '<p class="circuit-title">Circuito dos Shoppings</p>',
            unsafe_allow_html=True,
        )

    # Título e descrição abaixo do banner
    st.markdown(
        """
        <div class="circuit-header">
            <p class="circuit-ranking-title">Ranking — Circuito dos Shoppings</p>
            <p class="circuit-description">
                Este ranking apura os campeões gerais do circuito com base nos resultados
                combinados da <strong>Etapa Sumaúma</strong> e da
                <strong>Etapa Ponta Negra</strong>.
                A pontuação de cada competidor é a soma dos pontos obtidos nas duas etapas.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

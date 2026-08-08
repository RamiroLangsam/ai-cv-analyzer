import re
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -------------------------
# CONFIGURACIÓN
# -------------------------

st.set_page_config(
    page_title="AI CV Analyzer",
    page_icon="📄",
    layout="wide"
)


# -------------------------
# HABILIDADES
# -------------------------

habilidades = [
    "python",
    "sql",
    "excel",
    "machine learning",
    "github",
    "git",
    "pandas",
    "numpy",
    "power bi",
    "tableau",
    "javascript",
    "typescript",
    "html",
    "css",
    "react",
    "node",
    "java",
    "c++",
    "c#",
    "docker",
    "aws",
    "azure",
    "linux"
]


# -------------------------
# FUNCIÓN PARA DETECTAR SKILLS
# -------------------------

def contiene_habilidad(texto, habilidad):
    patron = r"(?<!\w)" + re.escape(habilidad) + r"(?!\w)"
    return re.search(patron, texto, re.IGNORECASE) is not None


# -------------------------
# TÍTULO
# -------------------------

st.title("AI CV Analyzer")

st.write(
    "Analizá la compatibilidad entre un CV y una oferta laboral "
    "utilizando técnicas de procesamiento de lenguaje natural."
)

st.divider()


# -------------------------
# INPUTS
# -------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("Tu CV")

    cv = st.text_area(
        "Pegá acá el contenido de tu CV",
        height=300,
        placeholder="Ejemplo: Tengo conocimientos de Python, SQL, GitHub..."
    )


with col2:
    st.subheader("Oferta laboral")

    oferta = st.text_area(
        "Pegá acá la descripción del puesto",
        height=300,
        placeholder="Ejemplo: Buscamos una persona con Python, SQL y Machine Learning..."
    )


# -------------------------
# ANÁLISIS
# -------------------------

if st.button(
    "Analizar compatibilidad",
    type="primary",
    use_container_width=True
):

    if not cv.strip() or not oferta.strip():

        st.warning(
            "Tenés que completar el CV y la oferta laboral."
        )

    else:

        # -------------------------
        # NLP - TF-IDF
        # -------------------------

        vectorizador = TfidfVectorizer(
            lowercase=True,
            stop_words=None
        )

        vectores = vectorizador.fit_transform(
            [cv, oferta]
        )

        similitud = cosine_similarity(
            vectores[0:1],
            vectores[1:2]
        )[0][0]

        similitud_texto = similitud * 100


        # -------------------------
        # ANÁLISIS DE HABILIDADES
        # -------------------------

        habilidades_oferta = []
        coincidencias = []
        faltantes = []

        for habilidad in habilidades:

            if contiene_habilidad(
                oferta,
                habilidad
            ):

                habilidades_oferta.append(
                    habilidad
                )

                if contiene_habilidad(
                    cv,
                    habilidad
                ):

                    coincidencias.append(
                        habilidad
                    )

                else:

                    faltantes.append(
                        habilidad
                    )


        # -------------------------
        # COBERTURA DE HABILIDADES
        # -------------------------

        if len(habilidades_oferta) > 0:

            cobertura = (
                len(coincidencias)
                / len(habilidades_oferta)
            ) * 100

        else:

            cobertura = 0


        # -------------------------
        # PUNTAJE FINAL
        # -------------------------

        puntaje_final = (
            similitud_texto * 0.4
            + cobertura * 0.6
        )


        # -------------------------
        # RESULTADOS
        # -------------------------

        st.divider()

        st.header(
            "Resultado del análisis"
        )

        m1, m2, m3 = st.columns(3)

        m1.metric(
            "Puntaje general",
            f"{puntaje_final:.0f}%"
        )

        m2.metric(
            "Similitud del texto",
            f"{similitud_texto:.0f}%"
        )

        m3.metric(
            "Cobertura de habilidades",
            f"{cobertura:.0f}%"
        )

        st.progress(
            min(
                int(puntaje_final),
                100
            ) / 100
        )


        # -------------------------
        # INTERPRETACIÓN
        # -------------------------

        if puntaje_final >= 75:

            st.success(
                "Alta compatibilidad con la oferta."
            )

        elif puntaje_final >= 50:

            st.info(
                "Compatibilidad media. "
                "Hay algunos puntos que podrías mejorar."
            )

        else:

            st.warning(
                "Compatibilidad baja. "
                "El CV podría adaptarse mejor a esta oferta."
            )


        # -------------------------
        # HABILIDADES
        # -------------------------

        izquierda, derecha = st.columns(2)


        with izquierda:

            st.subheader(
                "Habilidades coincidentes"
            )

            if coincidencias:

                for habilidad in coincidencias:

                    nombre = (
                        habilidad.upper()
                        if habilidad in [
                            "sql",
                            "html",
                            "css",
                            "aws"
                        ]
                        else habilidad.title()
                    )

                    st.write(
                        f"✅ {nombre}"
                    )

            else:

                st.write(
                    "No se detectaron "
                    "habilidades coincidentes."
                )


        with derecha:

            st.subheader(
                "Habilidades faltantes"
            )

            if faltantes:

                for habilidad in faltantes:

                    nombre = (
                        habilidad.upper()
                        if habilidad in [
                            "sql",
                            "html",
                            "css",
                            "aws"
                        ]
                        else habilidad.title()
                    )

                    st.write(
                        f"❌ {nombre}"
                    )

            else:

                st.write(
                    "No se detectaron "
                    "habilidades faltantes."
                )


        # -------------------------
        # RECOMENDACIÓN
        # -------------------------

        st.divider()

        st.subheader(
            "Recomendación"
        )

        if faltantes:

            skills = ", ".join(
                habilidad.upper()
                if habilidad in [
                    "sql",
                    "html",
                    "css",
                    "aws"
                ]
                else habilidad.title()
                for habilidad in faltantes
            )

            st.write(
                f"La oferta menciona habilidades "
                f"que no aparecen en tu CV: "
                f"**{skills}**."
            )

            st.write(
                "Si realmente tenés experiencia "
                "con alguna de ellas, considerá "
                "agregarla de forma clara en tu CV."
            )

        else:

            st.write(
                "Tu CV incluye todas las habilidades "
                "técnicas que el sistema detectó "
                "en la oferta."
            )


# -------------------------
# PIE DE PÁGINA
# -------------------------

st.divider()

st.caption(
    "AI CV Analyzer · Python · NLP · "
    "Scikit-learn · Streamlit"
)

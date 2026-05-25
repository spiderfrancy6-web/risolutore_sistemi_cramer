#letsgoski

# --- materiale di lavoro --- 
import streamlit as st
from sympy import (
    symbols, Rational, Matrix, latex
)

st.set_page_config(
    page_title="risolutore_sistemi_cramer",
    page_icon="🧮",
    layout="centered"
)

# --- Configurazione app ---
st.title("Sistemi con Cramer")
st.subheader("Passaggi Dettagliati :)")
#st.caption("made by SpiderFrancy")
st.divider()

# --- Sidebar con definizione --- 
with st.sidebar:
    st.header ("🔢Il metodo Cramer")
    st.write("Nel caso in cui ci sono due equazioni a due incognite (x e y), cramer permette di trovare i valori tramite i coefficienti delle variabili. conbinandoli in uno specifico modo per trovare il determinante. Successivamente si trovano x e y. ")
    st.divider()
    st.write("Piccolo sondaggio :D ")
    st.selectbox(
        "Metodo preferito",
        ["Sostituzione", "Confronto", "Riduzione", "Cramer (scelta giusta)"]
    )


st.subheader("Regola di Cramer")
st.info("Inserisci i coefficienti del sistema lineare 2×2. Verranno mostrati tutti i determinanti e i passaggi.")

n = 2

st.write("**Matrice dei coefficienti A**")
# coefficienti A
A_vals = []
for i in range(n):
    cols = st.columns(n)
    row = []
    for j in range(n):
        val = cols[j].number_input(
            f"a[{i+1},{j+1}]",
            value=0, step=1,
            key=f"a_{i}_{j}",
        )
        row.append(val)
    A_vals.append(row)

# termini noti
st.write("**Termini noti b**")
b_cols = st.columns(n)
b_vals = []
for i in range(n):
    val = b_cols[i].number_input(
        f"b[{i+1}]",
        value=0, step=1,
        key=f"b_{i}",
    )
    b_vals.append(val)

# solution
if st.button("Risolvi con Cramer", key="solve_cramer", type="primary"):
    try:
        A_sym = Matrix([[Rational(v).limit_denominator(1000) for v in row] for row in A_vals])
        b_sym = Matrix([Rational(v).limit_denominator(1000) for v in b_vals])
        det_A = A_sym.det()
        st.divider()
        st.write("### Passaggi della soluzione")

        # Passo 1 — determinante principale
        with st.expander("Passo 1 — Determinante principale det(A)", expanded=True):
            st.latex(r"A = " + latex(A_sym))
            st.latex(r"\det(A) = " + latex(det_A))

        if det_A == 0:
            st.error("det(A) = 0 — Il sistema non ha soluzione unica (impossibile o indeterminato).")
        else:
            var_names = ["x", "y"]
            solutions = {}

            for k in range(n):
                Ak = A_sym.copy().as_mutable()
                for i in range(n):
                    Ak[i, k] = b_sym[i]
                Ak = Matrix(Ak)
                det_Ak = Ak.det()
                xk = Rational(det_Ak, det_A)
                solutions[var_names[k]] = xk

                with st.expander(f"Passo {k+2} — Determinante A_{k+1} per {var_names[k]}", expanded=True):
                    st.write(f"Sostituisco la colonna {k+1} con **b**:")
                    st.latex(r"A_{" + str(k+1) + r"} = " + latex(Ak))
                    st.latex(r"\det(A_{" + str(k+1) + r"}) = " + latex(det_Ak))
                    st.latex(
                        var_names[k] + r" = \frac{\det(A_{" + str(k+1) + r"})}{\det(A)} = \frac{"
                        + latex(det_Ak) + r"}{" + latex(det_A) + r"} = " + latex(xk)
                    )

            # Risultato finale
            st.divider()
            st.write("### ✅ Soluzione")
            sol_cols = st.columns(n)
            for i, v in enumerate(var_names):
                sol_cols[i].metric(label=v, value=str(solutions[v]))

            # Verifica
            st.write("**Verifica nelle equazioni originali**")
            sol_sub = {symbols(v): solutions[v] for v in var_names}
            all_ok = True
            for i in range(n):
                lhs = sum(A_sym[i, j] * symbols(var_names[j]) for j in range(n))
                lhs_val = lhs.subs(sol_sub)
                ok = lhs_val == b_sym[i]
                if not ok:
                    all_ok = False
                eq_terms = " + ".join([
                    r"(" + latex(A_sym[i, j]) + r") \cdot " + var_names[j]
                    for j in range(n)
                ])
                check_icon = "✓" if ok else "✗"
                st.write(f"{check_icon} Equazione {i+1}:")
                st.latex(
                    eq_terms + " = " + latex(b_sym[i])
                    + r"\quad \Rightarrow \quad"
                    + latex(lhs_val) + " = " + latex(b_sym[i])
                )

            if all_ok:
                st.success("Verifica superata — tutte le equazioni sono soddisfatte.")
            else:
                st.warning("Attenzione: una o più equazioni non sono verificate.")

    except Exception as e:
        st.error(f"Errore: {e}")

st.divider()
st.caption("Programmato con il linguaggio python")
st.caption("Moduli usati: Streamlit & Sympy")
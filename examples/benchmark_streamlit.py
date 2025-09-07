import streamlit as st
from smooth_criminal.benchmark import benchmark_jam


def cube(x):
    return x ** 3


st.title("Benchmark de Smooth Criminal")

backends = ["thread", "process", "async"]
resultados = benchmark_jam(cube, [1, 2, 3], backends)

st.write("Resultados:")
st.write(resultados["results"])

st.success(f"Backend más rápido: {resultados['fastest']}")

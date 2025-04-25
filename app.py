import pandas as pd
import streamlit as st
import plotly_express as px

st.markdown(
    """
    <h1 style='text-align: center; color: white;'>
        Análisis del Almacén de Vehículos Usados
    </h1>
    """,
    unsafe_allow_html=True
)

st.write("A continuación se presenta un análisis básico de un almacén de vehículos usados. En este análisis se comparan variables como el estado del vehículo, su tipo, precio y año de fabricación, con el fin de identificar patrones o tendencias relevantes.")

df = pd.read_csv(
    'c:\\Users\\ING. JUAN ALVARADO\\Desktop\\Proyecto_sprint#7\\Proyecto_sprint7\\vehicles_us.csv')

st.header("Dataset de vehiculos de usados")
st.dataframe(df)

# Crear gráfico de distribución por año
st.subheader('Distribución de vehículos por año del modelo')

vehicles_per_year = df['model_year'].value_counts().sort_index()

# Slider para ajustar el límite del eje X
x_min = st.slider("Límite mínimo del eje X", min_value=vehicles_per_year.index.min(),
                  max_value=vehicles_per_year.index.max(), value=vehicles_per_year.index.min())
x_max = st.slider("Límite máximo del eje X", min_value=vehicles_per_year.index.min(),
                  max_value=vehicles_per_year.index.max(), value=vehicles_per_year.index.max())

# Crear gráfica
fig = px.bar(
    x=vehicles_per_year.index,
    y=vehicles_per_year.values,
    labels={'x': 'Año del modelo', 'y': 'Cantidad de vehículos'},
    color_discrete_sequence=['green']
)

# Aplicar los límites definidos por los sliders en el eje X
fig.update_xaxes(range=[x_min, x_max])

# Mostrar gráfica
st.plotly_chart(fig)

st.subheader('Precio promedio por condición del vehículo')

avg_price_by_condition = df.groupby('condition')['price'].mean().reset_index()

avg_price_by_condition.rename(
    columns={'condition': 'Condición', 'price': 'Precio'}, inplace=True)


fig_3 = px.bar(
    avg_price_by_condition,
    x='Condición',
    y='Precio',
    labels={'condition': 'Condición', 'price': 'Precio promedio (USD)'}
)

st.plotly_chart(fig_3)


if "show_table" not in st.session_state:
    st.session_state.show_table = False

# Crear un botón para alternar el estado de la tabla
if st.button('Mostrar/Ocultar tabla'):
    st.session_state.show_table = not st.session_state.show_table

# Mostrar u ocultar la tabla basado en el estado
if st.session_state.show_table:
    st.table(avg_price_by_condition)  # Muestra la tabla si el estado es True

st.subheader('Cantidad de vehículos según su tipo de transmisión')

type_transmission = df['transmission'].value_counts().reset_index()
type_transmission.rename(columns={
                         'transmission': 'Transmisión', 'count': 'Cantidad de unidades'}, inplace=True)

st.table(type_transmission)

type_vehicles = df['type'].value_counts().sort_index()

st.subheader('Distribución por tipo de vehículo')

fig_5 = px.bar(
    x=type_vehicles.index,
    y=type_vehicles.values,
    labels={'x': 'Tipo de vehiculo', 'y': 'Cantidad de vehículos'},
    color_discrete_sequence=['red']
)

st.plotly_chart(fig_5)


st.subheader('Distribución por tipo de vehículo y tipo de transmisión')


pivot_table = df.pivot_table(
    index='type',               # Filas: tipo de vehículo
    columns='transmission',      # Columnas: transmisión
    aggfunc='size',              # Función de agregación: contar
    # Reemplazar valores NaN con 0 (si hay combinaciones vacías)
    fill_value=0
)

# Mostrar la tabla dinámica
st.table(pivot_table)

st.subheader('Precio promedio por tipo de vehículo')

avg_price_by_type = df.groupby('type')['price'].mean().reset_index()

fig_6 = px.bar(
    avg_price_by_type,
    x='type',
    y='price',
    labels={'type': 'Tipo de vehiculo', 'price': 'Precio promedio (USD)'},
    color_discrete_sequence=['red']
)

st.plotly_chart(fig_6)

st.subheader('Kilometraje del vehículo vs Precio (USD)')

# Definir los rangos de los sliders
min_odometer = df['odometer'].min()
max_odometer = df['odometer'].max()
min_price = df['price'].min()
max_price = df['price'].max()

# Crear sliders para el rango de kilometraje y precio
odometer_range = st.slider(
    "Selecciona el rango de kilometraje",
    min_value=int(min_odometer),
    max_value=int(max_odometer),
    value=(int(min_odometer), int(max_odometer)),
    step=1000,  # Establecer un paso de 1000 para el kilometraje
    help="Ajusta el rango de kilometraje de los vehículos."
)

price_range = st.slider(
    "Selecciona el rango de precio (USD)",
    min_value=int(min_price),
    max_value=int(max_price),
    value=(int(min_price), int(max_price)),
    step=5000,  # Establecer un paso de 5000 para el precio
    help="Ajusta el rango de precio de los vehículos."
)

# Filtrar el DataFrame según el rango de los sliders
filtered_df = df[(df['odometer'] >= odometer_range[0]) &
                 (df['odometer'] <= odometer_range[1]) &
                 (df['price'] >= price_range[0]) &
                 (df['price'] <= price_range[1])]

# Crear la gráfica de dispersión con los datos filtrados
fig_4 = px.scatter(
    filtered_df,
    x='odometer',
    y='price',
    labels={'odometer': 'Kilometraje del vehículo', 'price': 'Precio (USD)'},
    color_discrete_sequence=['orange']
)

# Mostrar la gráfica
st.plotly_chart(fig_4)

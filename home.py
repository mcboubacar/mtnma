#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 16:40:34 2025

@author: mboubacar
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#from utils.data import load_data
import io

st.set_page_config(page_title="Suivi des Activités TIC", layout="wide")

# ⏱️ Constante pour les libellés
MAX_LIBELLE_LEN = 30
def tronquer(x): return x if len(x) < MAX_LIBELLE_LEN else x[:MAX_LIBELLE_LEN - 3] + "..."

st.title("📊 Tableau de bord")

# Chargement des données (admin=True => toutes les données)
# df = load_data(admin=True)
df = pd.read_excel("Suivi-des-activités 2025.xlsx")

# Nettoyage
df["Domaine"] = df["Domaine"].fillna("Non spécifié")
df["Responsable"] = df["Responsable"].fillna("Non attribué")
df["Date limite"] = pd.to_datetime(df["Date limite"], errors="coerce")
df["Activité"] = df["Activité"].fillna("Sans activité")
df["Tache"] = df["Tache"].fillna("Sans tâche")
df["Année"] = df["Date limite"].dt.year.fillna(0).astype(int)
df["Statut"] = df["Statut"].fillna("En cours")


with st.sidebar:
    st.header("🔍 Filtres")
    domaines = st.multiselect("Domaine", options=sorted(df["Domaine"].unique()))
    responsables = st.multiselect("Responsable", options=sorted(df["Responsable"].unique()))
    #annees = st.multiselect("Période (Année)", options=sorted(df["Année"].unique()))
    statuts = st.multiselect("Statut", options=sorted(df["Statut"].unique()))

# Si aucun filtre sélectionné, on prend tout

mask = pd.Series(True, index=df.index)
if domaines:
    mask &= df["Domaine"].isin(domaines)
if responsables:
    mask &= df["Responsable"].isin(responsables)
#if annees:
#    mask &= df["Année"].isin(annees)
if statuts:
    mask &= df["Statut"].isin(statuts)

filtered_df = df[mask]

# Gestion du cas vide
if filtered_df.empty:
    st.warning("⚠️ Aucune donnée ne correspond aux filtres sélectionnés.")
    st.stop()

# Vue hiérarchique Activité > Tâche
activites = filtered_df.groupby(["Responsable","Domaine","Activité"]).agg(
    Tâches_totales=("Tache", "count"),
    Tâches_realisees=("Statut", lambda x: (x == "Terminée").sum()),
    Date_limite=("Date limite", "max")
).reset_index()

activites["% execution"] = round(100 * activites["Tâches_realisees"] / activites["Tâches_totales"], 1)

activites["Statut"] = activites["% execution"].apply(
    lambda x: "Terminée" if x == 100 else "En cours"
)
st.markdown("##### 📋 Activités en fonction des filtres")
with st.expander("##### 📋 Rapport d'activités"):
    st.dataframe(activites.drop(["Tâches_totales","Tâches_realisees"],axis=1))
    #st.dataframe(activites[["Responsable","Domaine","Activité","Date_limite","% execution","Statut"]])
with st.expander("⬇️ Téléchargement"):
    output = io.BytesIO()
    activites.to_excel(output, index=False)
    st.download_button("Télécharger en Excel", data=output.getvalue(), 
                       file_name="activites_filtrees.xlsx",
                       key="download_excel_button"
    )
st.markdown("---")       
# 🎯 Statistiques globales
st.markdown("##### 📋 Les KPI")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🧩 Total Activités", activites.shape[0])
col2.metric("✅ Activités Terminées", (activites["% execution"] == 100).sum())
col3.metric("✅ Activités En cours", (activites.shape[0] - (activites["% execution"] == 100).sum()))
col4.metric("⏰ Activités en Retard", ((activites["Date_limite"] < pd.Timestamp.today()) & (activites["% execution"] < 100)).sum())
# 📥 Export Excel
# with st.expander("⬇️ Télécharger les données filtrées"):
#     output = io.BytesIO()
#     activites.to_excel(output, index=False)
#     st.download_button("Télécharger en Excel", data=output.getvalue(), file_name="activites_filtrees.xlsx")

st.markdown("---")

# Graphique 1 : Activités par domaine
st.markdown("##### 📌 Nombre d'Activités par Domaine")
activites["Domaine-trq"] = activites["Domaine"].apply(tronquer)
fig_domaine = px.bar(
    activites.groupby(["Domaine-trq","Statut"]).size().reset_index(name="Nombre d'activités"),
    x="Domaine-trq", y="Nombre d'activités", 
    text_auto=True, color="Statut",
    labels={'Domaine-trq': 'Domaine'},
    width=800,height=500,
    color_discrete_map={"Terminée": "#2ca02c", "En cours": "#Cca02c"},
)
st.plotly_chart(fig_domaine, use_container_width=True)

# Graphique 2 : Activités par responsable
st.markdown("##### 👤 Nombre d'Activités par Responsable")
# data_resp = activites["Responsable"].value_counts().reset_index()
# data_resp.columns = ["Responsable", "Nombre"]
# fig_resp = go.Figure(data=[go.Pie(
#     labels=data_resp["Responsable"],
#     values=data_resp["Nombre"],
#     textinfo="value",
#     insidetextorientation="radial",
#     marker=dict(colors=px.colors.qualitative.Set3)
# )])
activites["Resp-trq"] = activites["Responsable"].apply(tronquer)
fig_domaine = px.bar(
    activites.groupby(["Resp-trq","Statut"]).size().reset_index(name="Nombre d'activités"),
    x="Resp-trq", y="Nombre d'activités", 
    text_auto=True, color="Statut",
    labels={'Resp-trq': 'Responsable'},
    width=800,height=500,
    color_discrete_map={"Terminée": "#2ca02c", "En cours": "#Cca02c"},
)
st.plotly_chart(fig_resp, use_container_width=True)

# Graphique 3 : Répartition des activites par statuts
if  not ((filtered_df["Tache"]=="Sans tâche").all()):
    st.markdown("##### 📋 Répartition des Activites par Statut")
    fig_statut = px.histogram(
        activites.groupby(["Statut"]).size().reset_index(name="Nombre d'activités"), 
        x="Statut", y="Nombre d'activités",
        text_auto=True, color="Statut", barmode="group",
        color_discrete_map={"Terminée": "#2ca02c", "En cours": "#Cca02c"},
        )
    fig_statut.update_traces(textposition='outside')
    st.plotly_chart(fig_statut, use_container_width=True)

# Graphique 4 : Taux d'exécution

activites["libellé activité"] = activites["Activité"].apply(tronquer)
activites_filtrees = activites[activites["% execution"] > 0]
if len(activites_filtrees)!=0:
    st.markdown("##### ✅ Taux d'exécution > 0 des Activités")
    fig_exec = px.bar(
        #activites_filtrees.sort_values("% execution", ascending=False),
        activites_filtrees,
        y="% execution", x="libellé activité", orientation="v", 
        text_auto=True,color_continuous_scale="#2ca02c"
    )
    fig_exec.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig_exec, use_container_width=True)

# Graphique 5 : Activités en retard
st.markdown("##### ⏳ Activités en Retard")

retard = activites[
    (activites["Date_limite"] < pd.Timestamp.today()) &
    (activites["% execution"] < 100)
]

#st.dataframe(retard)
if not retard.empty:
    retard["libellé activité"] = retard["Activité"].apply(tronquer)
    fig_retard = px.bar(
        retard,
        x="libellé activité", y="% execution", color="Domaine", 
    )
    fig_retard.update_layout(
        yaxis=dict(range=[-1, 100]),
        xaxis_tickangle=45
    )
    
    st.plotly_chart(fig_retard, use_container_width=True)
else:
    st.success("🎉 Aucune activité en retard selon les filtres OU données de suivi non renseignées")

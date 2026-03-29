import streamlit as st
import pandas as pd

st.title("Playmobil - Suivi des stocks")

# Upload des fichiers
fichier_commande = st.file_uploader("Importer le fichier commande (Excel)", type=["xlsx"])
fichier_stock = st.file_uploader("Importer le fichier stock (CSV ou Excel)", type=["csv", "xlsx"])

# Bouton pour lancer le traitement
if st.button("Valider"):
    if fichier_commande is None or fichier_stock is None:
        st.error("Merci d'importer les deux fichiers.")
    else:
        try:
            # Lecture fichier commande
            df = pd.read_excel(fichier_commande, sheet_name="Lignes", skiprows=6)
            references_ok = df["Article"]

            # Lecture fichier stock
            if fichier_stock.name.endswith(".csv"):
                df_stock = pd.read_csv(fichier_stock, sep=";")
            else:
                df_stock = pd.read_excel(fichier_stock)

            # Détection automatique colonne "Référence fabricant"
            if "Référence fabricant" not in df_stock.columns:
                cols_valides = []
                for i in range(len(df_stock.columns)):
                    col = df_stock.columns[i]
                    if df_stock[col].astype(str).str.match(r"^\d{4,8}$").all():
                        cols_valides.append(i)

                cols = list(df_stock.columns)
                for i in cols_valides:
                    cols[i] = "Référence fabricant"
                df_stock.columns = cols

            # Vérification des colonnes nécessaires
            required_cols = ["Référence fabricant", "Stock article", "Nombre d'UV vendues"]
            if not all(col in df_stock.columns for col in required_cols):
                st.error("Le fichier de stock doit contenir les colonnes : 'Référence fabricant', 'Stock article', 'Nombre d'UV vendues'")
            else:
                # Traitement
                references_stock_ok = df_stock[
                    df_stock["Référence fabricant"].isin(references_ok)
                    & df_stock["Référence fabricant"].notnull()
                ]

                references_stock_ok = references_stock_ok[
                    ["Référence fabricant", "Stock article", "Nombre d'UV vendues"]
                ]

                references_stock_ok["Stock initial"] = (
                    references_stock_ok["Stock article"] +
                    references_stock_ok["Nombre d'UV vendues"]
                )

                # Affichage
                st.success("Traitement réussi ✅")
                st.dataframe(references_stock_ok)

        except Exception as e:
            st.error(f"Erreur : {e}")
import pandas as pd
import matplotlib.pyplot as plt



######### INIZIO METODI PER METRICHE DI PROCESSO QUINDI DA USARE IL DATFRAME RESTITUITO DA generate_process_metrics in spMetrics ###########



def revision_number(df):
    """Genera e restituisce un grafico a barre con il numero totale di autori per data del commit"""
    plt.figure(figsize=(10, 6))
    plt.bar(df["Data del Commit"], df["Numero di Revisioni"], color='blue')
    plt.xlabel('Data del Commit')
    plt.ylabel('Numero di Revisioni')
    plt.title('Number of revisions')
    plt.xticks(rotation=45)
    return plt



def loc_number(df):
    """Genera e restituisce un grafico a linee LOC con l'indice basato sulla data del commit"""
    df.set_index("Data del Commit", inplace=True)
    df = df.sort_index()
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["Linee di Codice"], label='Linee di Codice', marker='o')
    plt.plot(df.index, df["Linee vuote"], label='Linee Vuote', marker='o')
    plt.plot(df.index, df["Commenti"], label='Commenti', marker='o')
    plt.xlabel('Data del Commit')
    plt.ylabel('Numero di Linee')
    plt.title(' Amount (in LOC) of previous changes')
    plt.legend()
    plt.xticks(rotation=45)
    return plt



def authors(df):
    """Genera e restituisce un grafico a barre con il numero totale di autori per ogni data del commit"""
    authors_count = pd.DataFrame(columns=["Data del Commit", "Numero di Autori"])
    for date, group in df.groupby("Data del Commit"):
        authors_count = pd.concat([authors_count, pd.DataFrame({"Data del Commit": [date], "Numero di Autori": [len(set(group["Autori Distinti"].sum()))-1]})])
    plt.figure(figsize=(10, 6))
    plt.bar(authors_count["Data del Commit"], authors_count["Numero di Autori"], color='blue')
    plt.xlabel('Data del Commit')
    plt.ylabel('Numero di Autori')
    plt.title('Numero di Autori per Data del Commit')
    plt.xticks(rotation=45)
    return plt

    

def weeks(df):
    """Genera e restituisce un grafico a barre con il numero di settimane del file per data del commit"""
    plt.figure(figsize=(10, 6))
    plt.bar(df["Data del Commit"], df["Settimane file"], color='blue')
    plt.xlabel('Data del Commit')
    plt.ylabel('Settimane file')
    plt.title('Age in weeks')
    plt.xticks(rotation=45)
    return plt



def codeC(df):
    """Genera e restituisce un grafico a barre con il numero di codechurn per  data del commit"""
    plt.figure(figsize=(10, 6))
    plt.bar(df["Data del Commit"], df["Code churn"], color='blue')
    plt.xlabel('Data del Commit')
    plt.ylabel('Code churn')
    plt.title('Number of changed code churns')
    plt.xticks(rotation=45)
    return plt



def bugfix(df):
    """Genera e restituisce un grafico a barre con il numero di bugfix per data del commit"""
    plt.figure(figsize=(10, 6))
    plt.bar(df["Data del Commit"], df["Bugfix commit"], color='blue')
    plt.xlabel('Data del Commit')
    plt.ylabel('Bugfix commit')
    plt.title('Bugfix')
    plt.xticks(rotation=45)
    return plt



######### FINE METODI PER METRICHE DI PROCESSO QUINDI DA USARE IL DATFRAME RESTITUITO DA generate_process_metrics #####################



######### INIZIO METODI PER METRICHE DI PROGETTO QUINDI DA USARE IL DATFRAME RESTITUITO DA generate_metrics_ck in spMetrics ###########



def wmc(df):
    """Genera e restituisce un grafico a linee con il valore di wmc per data del commit"""
    plt.figure(figsize=(10, 6))
    plt.plot(df["Data del Commit"], df["wmc"], marker='o', linestyle='-', color='green', label='WMC')
    plt.xlabel('Data del Commit')
    plt.ylabel('WMC (Weighted Methods per Class)')
    plt.title('Andamento della Metrica WMC nel Tempo')
    plt.xticks(rotation=45)
    return plt
    



def cbo(df):
    """Genera e restituisce un grafico a linee con il valore di cbo per data del commit"""
    plt.figure(figsize=(10, 6))
    plt.plot(df["Data del Commit"], df["wmc"], marker='o', linestyle='-', color='green', label='WMC')
    plt.xlabel('Data del Commit')
    plt.ylabel('WMC (Weighted Methods per Class)')
    plt.title('Andamento della Metrica WMC nel Tempo')
    plt.xticks(rotation=45)
    return plt



def dit(df):
    """Genera e restituisce un grafico a linee con il valore di dit per data del commit"""
    plt.figure(figsize=(10, 6))
    plt.plot(df["Data del Commit"], df["dit"], marker='o', linestyle='-', color='green', label='WMC')
    plt.xlabel('Data del Commit')
    plt.ylabel('DIT (Depth of Inheritance)')
    plt.title('Andamento della Metrica DIT nel Tempo')
    plt.xticks(rotation=45)
    return plt



def noc(df):
    """Genera e restituisce un grafico a linee con il valore di noc per data del commit"""
    plt.figure(figsize=(10, 6))
    plt.plot(df["Data del Commit"], df["noc"], marker='o', linestyle='-', color='green', label='WMC')
    plt.xlabel('Data del Commit')
    plt.ylabel('NOC  (Number of Children)')
    plt.title('Andamento della Metrica NOC nel Tempo')
    plt.xticks(rotation=45)
    return plt



def rfc(df):
    """Genera e restituisce un grafico a linee con il valore di rfc per data del commit"""
    plt.figure(figsize=(10, 6))
    plt.plot(df["Data del Commit"], df["rfc"], marker='o', linestyle='-', color='green', label='WMC')
    plt.xlabel('Data del Commit')
    plt.ylabel('RFC (Response for a Class)')
    plt.title('Andamento della Metrica RFC nel Tempo')
    plt.xticks(rotation=45)
    return plt



def lcom(df):
    """Genera e restituisce un grafico a linee con il valore di lcom per data del commit"""
    plt.figure(figsize=(10, 6))
    plt.plot(df["Data del Commit"], df["lcom"], marker='o', linestyle='-', color='green', label='WMC')
    plt.xlabel('Data del Commit')
    plt.ylabel('LCOM (Lack of Cohesion of Methods)')
    plt.title('Andamento della Metrica LCOM nel Tempo')
    plt.xticks(rotation=45)
    return plt


######### FINE METODI PER METRICHE DI PROGETTO QUINDI DA USARE IL DATFRAME RESTITUITO DA generate_metrics_ck #################
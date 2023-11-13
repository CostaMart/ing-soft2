import pandas as pd
import matplotlib.pyplot as plt



def revision_number(df):
    """Genera e restituisce un grafico a barre con X = Data del Commit, Y = Numero di Revisioni"""
    plt.figure(figsize=(10, 6))
    plt.bar(df["Data del Commit"], df["Numero di Revisioni"], color='blue')
    plt.xlabel('Data del Commit')
    plt.ylabel('Numero di Revisioni')
    plt.title('Number of revisions')
    plt.xticks(rotation=45)
    return plt



def loc_number(df):
    """Genera e restituisce un grafico a linee con l'indice basato sulla data del commit"""
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
    """Da utilizzare con grafico a barre X = Data del Commit, Y = Settimane File"""
    plt.figure(figsize=(10, 6))
    plt.bar(df["Data del Commit"], df["Settimane file"], color='blue')
    plt.xlabel('Data del Commit')
    plt.ylabel('Settimane file')
    plt.title('Age in weeks')
    plt.xticks(rotation=45)
    return plt



def codeC(df):
    """Da utilizzare grafico a barre per quantità quindi X= Data del Commit, Y = Code Churn"""
    plt.figure(figsize=(10, 6))
    plt.bar(df["Data del Commit"], df["Code churn"], color='blue')
    plt.xlabel('Data del Commit')
    plt.ylabel('Code churn')
    plt.title('Number of changed code churns')
    plt.xticks(rotation=45)
    return plt



def bugfix(df):
    """Da utilizzare con grafico a barre vicino alle metriche di ck però X = Data del Commit, Y = bugfix commit"""
    plt.figure(figsize=(10, 6))
    plt.bar(df["Data del Commit"], df["Bugfix commit"], color='blue')
    plt.xlabel('Data del Commit')
    plt.ylabel('Bugfix commit')
    plt.title('Bugfix')
    plt.xticks(rotation=45)
    return plt



def wmc(df):
    """Da utilizzare con grafico a linea X = Data Del Commit Y = wmc"""
    plt.figure(figsize=(10, 6))
    plt.plot(df["Data del Commit"], df["wmc"], marker='o', linestyle='-', color='green', label='WMC')
    plt.xlabel('Data del Commit')
    plt.ylabel('WMC (Weighted Methods per Class)')
    plt.title('Andamento della Metrica WMC nel Tempo')
    plt.xticks(rotation=45)
    return plt
    



def cbo(df):
    """Da utilizzare con grafico a linea X = Data Del Commit Y = cbo"""
    plt.figure(figsize=(10, 6))
    plt.plot(df["Data del Commit"], df["wmc"], marker='o', linestyle='-', color='green', label='WMC')
    plt.xlabel('Data del Commit')
    plt.ylabel('WMC (Weighted Methods per Class)')
    plt.title('Andamento della Metrica WMC nel Tempo')
    plt.xticks(rotation=45)
    return plt



def dit(df):
    """Da utilizzare con grafico a linea X = Data Del Commit Y = dit"""
    plt.figure(figsize=(10, 6))
    plt.plot(df["Data del Commit"], df["dit"], marker='o', linestyle='-', color='green', label='WMC')
    plt.xlabel('Data del Commit')
    plt.ylabel('DIT (Depth of Inheritance)')
    plt.title('Andamento della Metrica DIT nel Tempo')
    plt.xticks(rotation=45)
    return plt



def noc(df):
    """Da utilizzare con grafico a linea X = Data Del Commit Y = noc"""
    plt.figure(figsize=(10, 6))
    plt.plot(df["Data del Commit"], df["noc"], marker='o', linestyle='-', color='green', label='WMC')
    plt.xlabel('Data del Commit')
    plt.ylabel('NOC  (Number of Children)')
    plt.title('Andamento della Metrica NOC nel Tempo')
    plt.xticks(rotation=45)
    return plt



def rfc(df):
    """Da utilizzare con grafico a linea X = Data Del Commit Y = rfc"""
    plt.figure(figsize=(10, 6))
    plt.plot(df["Data del Commit"], df["rfc"], marker='o', linestyle='-', color='green', label='WMC')
    plt.xlabel('Data del Commit')
    plt.ylabel('RFC (Response for a Class)')
    plt.title('Andamento della Metrica RFC nel Tempo')
    plt.xticks(rotation=45)
    return plt



def lcom(df):
    """Da utilizzare con grafico a linea X = Data Del Commit Y = lcom"""
    plt.figure(figsize=(10, 6))
    plt.plot(df["Data del Commit"], df["lcom"], marker='o', linestyle='-', color='green', label='WMC')
    plt.xlabel('Data del Commit')
    plt.ylabel('LCOM (Lack of Cohesion of Methods)')
    plt.title('Andamento della Metrica LCOM nel Tempo')
    plt.xticks(rotation=45)
    return plt
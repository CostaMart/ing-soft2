import pandas as pd

def revision_number(df):
    """Da utilizzare con grafico a barre X = Nome della Classe, Y = Numero di Revisioni"""
    return df[["Data del Commit", "Numero di Revisioni"]]

def loc_number(df):
    """Grafico a linee: L'indice è la data del commit le linee sono gli altri attributi"""
    return df[["Data del Commit", "Linee di Codice", "Linee Vuote", "Commenti"]]

def authors(df):
    """Grafico a dispersione che dovrebbe rappresnetare la presenza di quell'autore nel tempo(quindi nel commit)"""
    return df[["Data del Commit", "Autori"]]

def weeks(df):
    """Da utilizzare con grafico a barre X = Data del Commit, Y = Settimane File"""
    return df[["Data del Commit", "Settimane file"]]

def codeC(df):
    """Da utilizzare grafico a barre per quantità quindi X= Data del Commit, Y = Code Churn"""
    return df[["Data del Commit", "Code churn con hash1"]]

def bugfix(df):
    """Da utilizzare con grafico a barre vicino alle metriche di ck però X = Data del Commit, Y = bugfix commit"""
    return df[["Data del Commit", "bugfix commit"]]

def wmc(df):
    """Da utilizzare con grafico a linea X = Data Del Commit Y = wmc"""
    return df[["Data del Commit", "wmc"]]

def cbo(df):
    """Da utilizzare con grafico a linea X = Data Del Commit Y = cbo"""
    return df[["Data del Commit", "cbo"]]

def dit(df):
    """Da utilizzare con grafico a linea X = Data Del Commit Y = dit"""
    return df[["Data del Commit", "dit"]]

def noc(df):
    """Da utilizzare con grafico a linea X = Data Del Commit Y = noc"""
    return df[["Data del Commit", "noc"]]
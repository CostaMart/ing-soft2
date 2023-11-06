import pandas as pd

def revision_number(df):
    """Da utilizzare con grafico a barre X = Nome della Classe, Y = Numero di Revisioni"""
    return df[["Nome della Classe", "Numero di Revisioni"]]

def loc_number(df):
    """Da utilizzare con grafico a torta Titolo = LOC 'Nome della Classe' e ogni spicchio è una di queste cose"""
    return df[["Nome della Classe", "Linee di Codice", "Linee Vuote", "Commenti"]]

def authors(df):
    """Da utilizzare con grafico a torta Titolo = Autori 'Nome della Classe' e ogni spicchio è un autore """
    return df[["Nome della Classe", "Autori"]]

def weeks(df):
    """Da utilizzare con grafico a barre X = Nome della Classe, Y = Settimane File"""
    return df[["Nome della Classe", "Settimane file"]]

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
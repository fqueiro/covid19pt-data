import pandas as pd
import datetime
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.ndimage.filters import gaussian_filter1d

casos_wide = pd.read_csv(str(Path(__file__).resolve().parents[2] / 'data_concelhos.csv'))

casos_wide.columns = map(str.title, casos_wide.columns)
plot_days = 1000
smoothing = 7
concelhos_lx = {'name':'Lisboa','label':'Lisboa Norte','conc':['Lisboa','Loures','Odivelas','Sintra','Amadora','Cascais','Mafra','Oeiras','Vila Franca De Xira','Azambuja']}
concelhos_aml = {'name':'AML','label':'Área Metropolitana de Lisboa','conc':['Lisboa','Loures','Odivelas','Sintra','Amadora','Cascais','Mafra','Oeiras','Vila Franca De Xira','Azambuja','Alcochete', \
                'Almada','Barreiro','Moita','Montijo','Palmela','Setúbal','Sesimbra','Seixal']}
concelhos_lxsul = {'name':'LxSul','label':'Lisboa Sul','conc':['Sesimbra','Seixal','Barreiro','Montijo']}
concelhos_curia = {'name':'Curia','label':'Área Metropolitana de Tamengos','conc':['Anadia','Mealhada','Águeda','Cantanhede','Oliveira Do Bairro','Mortágua']}
concelhos_amp = {'name':'AMP','label':'Área Metropolitana do Porto','conc':['Arouca','Espinho','Gondomar','Maia','Matosinhos','Oliveira De Azeméis','Paredes','Porto', \
                   'Póvoa De Varzim','Santa Maria Da Feira','Santo Tirso','São João Da Madeira','Trofa','Vale De Cambra', \
                   'Valongo','Vila Do Conde','Vila Nova De Gaia']}
concelhos_pt = {'name':'Portugal','label':'Portugal','conc':['Área Metropolitana de Lisboa','Área Metropolitana do Porto','Área Metropolitana de Tamengos']}

plticks = list(casos_wide['Data'].tail(plot_days))[10::max(1,int(len(list(casos_wide['Data'].tail(plot_days)))/20))]

plt.rc('xtick', labelsize=20)
plt.rc('ytick', labelsize=20)

def plot_conc(concelhos):
    casos_wide[concelhos['label']] = casos_wide[concelhos['conc']].sum(axis = 1, skipna = True) 
    fig, ax = plt.subplots(figsize=(15,12))
    #ylim = plt.ylim(0, 60)
    for concelho in concelhos['conc']:
        casos_wide['temp'] = gaussian_filter1d(casos_wide[concelho].diff(), sigma=3)
        #_ = plt.plot(casos_wide['Data'].tail(plot_days), casos_wide[concelho].diff().rolling(window=smoothing).mean().tail(plot_days))
        _ = plt.plot(casos_wide['Data'].tail(plot_days), casos_wide['temp'].tail(plot_days))
        lgd = ax.legend(concelhos['conc'], prop={'size': 20}, loc='upper left', bbox_to_anchor=(1, 1))
        plt.xticks(plticks)
        fig.autofmt_xdate()
    PATH_TO_GRAPH = str(Path(__file__).resolve().parents[2]) + '/docs/' + concelhos['name']
    fig.savefig(PATH_TO_GRAPH, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.show()

plot_conc(concelhos_aml)
plot_conc(concelhos_curia)
plot_conc(concelhos_amp)
plot_conc(concelhos_pt)

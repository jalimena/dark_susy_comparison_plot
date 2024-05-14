'''
Script to plot a comparison of the 
2016 Dark SUSY results. S.D. Butalla, 2024/03/13.
'''

import argparse
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Patch
import mplhep
import numpy as np
import sys
import comparison_2016_style # import style file 

global outline
global fill
global alpha

outline = comparison_2016_style.outline
fill    = comparison_2016_style.fill
alpha   = comparison_2016_style.alpha

matplotlib.rcParams.update({'font.size': 34})
plt.style.use(mplhep.style.CMS)

def load_data(directory=None):
    # load data
    if not directory:
        gr_1em3_2_part1 = np.loadtxt('gr_1em3_part1.txt')
        gr_1em3_2_part2 = np.loadtxt('gr_1em3_part2.txt')
        gr_1em3_2_part3 = np.loadtxt('gr_1em3_part3.txt')
        gr_1em3_2_part4 = np.loadtxt('gr_1em3_part4.txt')
        gr_1em3_2_part5 = np.loadtxt('gr_1em3_part5.txt')

        br_H_gD_1_2018 = np.loadtxt('Limit_epsvsmass_BrHtoGamD_1_2018.dat')

        exo = np.loadtxt('exo21006.txt')
    else:
        direc = args.directory
        ## dark SUSY
        gr_1em3_2_part1 = np.loadtxt(direc + '/gr_1em3_part1.txt')
        gr_1em3_2_part2 = np.loadtxt(direc + '/gr_1em3_part2.txt')
        gr_1em3_2_part3 = np.loadtxt(direc + '/gr_1em3_part3.txt')
        gr_1em3_2_part4 = np.loadtxt(direc + '/gr_1em3_part4.txt')
        gr_1em3_2_part5 = np.loadtxt(direc + '/gr_1em3_part5.txt')

        ## HAHM
        br_H_gD_1_2018  = np.loadtxt(direc + '/Limit_epsvsmass_BrHtoGamD_1_2018.dat')

        exo             = np.loadtxt(direc + '/exo21006.txt')

    
    data = {'gr': {'1': gr_1em3_2_part1,
                   '2': gr_1em3_2_part2,
                   '3': gr_1em3_2_part3,
                   '4': gr_1em3_2_part4,
                   '5': gr_1em3_2_part5
                  },
            'hGD': {'1': br_H_gD_1_2018
                   },
            'exo': {'1': exo
                   }
            
           }

    return data

def scale_data(data):
    data_scaled = {}
    for br in data.keys():
        data_scaled[br] = {}
        for region in data[br].keys():
            if br == 'hGD':
                mass = data[br][region][:, 0]
                temp = np.power(10**data[br][region][:, 1], 0.5)
                data_scaled[br][region] = np.column_stack((mass, temp))
            else:
                data_scaled[br][region] = data[br][region]

    return data_scaled
            
        
def plot_data(data_scaled, version):
    
    matplotlib.rcParams.update({'font.size': 34})

    fig, ax = plt.subplots(figsize = (10, 10))
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_ylim([1e-10, 1e-2])
    ax.set_xlim([0.1, 1e2])
#    ax.set_xlabel(r'Dark boson mass [GeV]', loc='right')
    ax.set_xlabel(r'$m_{A^{\prime}}$ [GeV]', loc='right')
    if version == 0:
        ax.set_ylabel(r'Kinetic mixing parameter $\varepsilon$', loc='top')
    else:
#        ax.set_ylabel(r'95% CL exclusion on $\varepsilon$', loc='top')
        ax.set_ylabel(r'$\varepsilon$', loc='top')

    for br in data_scaled.keys():
        for region in data_scaled[br].keys():
            ax.plot(data_scaled[br][region][:, 0], data_scaled[br][region][:, 1], color=outline[br][region], linewidth=1)

            if br == 'hGD':
                ax.fill_between(data_scaled[br][region][:, 0],  data_scaled[br][region][:, 1],
                               np.full((data_scaled[br][region][:, 0].shape[0],), 1e-2), color=fill[br][region], alpha=alpha[br])
            else:
                ax.fill(data_scaled[br][region][:,0],  data_scaled[br][region][:,1],  fill[br][region], alpha=alpha[br])

    ## manually add legend patches
    if version == 0:
        leg = [
            Patch(facecolor=fill['exo']['1'], alpha=0.5, edgecolor=outline['exo']['1'],
                                 label='HAHM, $2\mu$, 97.6 fb$^{-1}$\nJHEP 05 (2023) 228'),
            Patch(facecolor=fill['hGD']['1'], alpha=0.5, edgecolor=outline['hGD']['1'],
                                 label='Dark SUSY, $4\mu$, 35.9 fb$^{-1}$\nPLB 796 (2019) 131'),
            Patch(facecolor=fill['gr']['1'], alpha=0.5, edgecolor=outline['gr']['1'],
                                 label='HAHM, $2\mu$ (scouting), 101 fb$^{-1}$\nJHEP 04 (2022) 062'),
        ]
    else:
        leg = [
            Patch(facecolor=fill['exo']['1'], alpha=0.5, edgecolor=outline['exo']['1'],
                                 label=r'$\bf{HAHM,}$ $\bf{2\mu,}$ $\bf{97.6}$ $\bf{fb^{-1}}}$'+'\nJHEP 05 (2023) 228'),
            Patch(facecolor=fill['hGD']['1'], alpha=0.5, edgecolor=outline['hGD']['1'],
                                 label=r'$\bf{Dark}$ $\bf{SUSY,}$ $\bf{4\mu,}$ $\bf{35.9}$ $\bf{fb^{-1}}$'+'\nPhys. Lett. B 796 (2019) 131'),
            Patch(facecolor=fill['gr']['1'], alpha=0.5, edgecolor=outline['gr']['1'],
                                 label=r'$\bf{HAHM,}$ $\bf{2\mu}$ $\bf{(scouting),}$ $\bf{101}$ $\bf{fb^{-1}}$'+'\nJHEP 04 (2022) 062'),
        ]


    ax.legend(handles=leg, loc='lower left', fontsize=16, handletextpad=0.4)
    if version == 0:
        ax.text(0.04, 0.37, r'$\mathcal{B}(h\rightarrow 2\gamma_{D}/2Z_{D})=1\%$', fontsize=22,transform=ax.transAxes)
    elif version == 1:
        ax.text(0.04, 0.37, 'B', family='sans-serif', fontsize=22, style='italic', weight='normal', transform=ax.transAxes)
        ax.text(0.07, 0.37, r"$(h\rightarrow 2A^{ })=1\%$", fontsize=22,transform=ax.transAxes)
        ax.text(0.207, 0.36, r"$^{\prime}$", fontsize=27,style='normal', fontweight='heavy', transform=ax.transAxes)
        ax.text(0.07, 0.30, '95% CL exclusion limits', style='normal', fontsize=20, fontweight='normal', transform=ax.transAxes)


    mplhep.cms.lumitext(text='35.9-101 $fb^{-1}$ (13 TeV)', fontname=None, fontsize=35)
    mplhep.cms.text(fontsize=35)

    fig.tight_layout()
    fig.savefig('comparison_2016_v%d_%s.pdf' % (version, datetime.today().strftime('%Y%m%d')))


if __name__ == "__main__":
    # arg parser
    parser = argparse.ArgumentParser(description='Script to plot the Dark SUSY comparison plot.')
    parser.add_argument('-d', '--directory', action="store", dest='directory', default=None,
                        help='Directory containing data (optional if the data are in the current working directory)')
    parser.add_argument('-v', '--version', action='store', dest='version', default=None,
                        help='Version of the plot style. Available options: [0, 1]. Default = 0')

    args = parser.parse_args() 

    ## check python version
    if sys.version_info[0] < 3:
        raise Exception('Python 3+ is required')

    if not args.version:
        version = 0
    else:
        version = int(args.version)
        if version not in [0, 1]:
            raise Exception('Acceptable versions are 0 (default) or 1.')


    ## load and prepare data
    data        = load_data(args.directory)
    data_scaled = scale_data(data)          # transform Dark SUSY model data

    plot_data(data_scaled, version)


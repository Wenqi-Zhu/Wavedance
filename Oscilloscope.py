import pandas as pd
import matplotlib.pyplot as plt
import matplotlib


def Oscilloscope(Record: pd.DataFrame, StateList: list):

    matplotlib.style.use('Solarize_Light2')

    TotalSubplot = len(StateList)
    SubplotID = 0
    fig, axes = plt.subplots(nrows=TotalSubplot, ncols=1)
    for State in StateList:
        yLable = "$" + State[0] + '_{' + State[1:] + '}$'
        Record.plot(x='θ', y=State, linewidth=2,
                    ax=axes[SubplotID], legend=False, grid=True)
        axes[SubplotID].set_ylabel(yLable)
        axes[SubplotID].get_xaxis().set_visible(False)
        # if State == 'vO':
        # axes[SubplotID].set_ylim([0.0,None])
        SubplotID += 1
    axes[SubplotID - 1].get_xaxis().set_visible(True)
    # plt.tight_layout()
    plt.show()
    return fig

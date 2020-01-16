import pandas as pd
import matplotlib.pyplot as plt
import matplotlib


def oscilloscope(record: pd.DataFrame, state_list: list):

    matplotlib.style.use('Solarize_Light2')

    total_subplot = len(state_list)
    subplot_id = 0
    fig, axes = plt.subplots(nrows=total_subplot, ncols=1)
    for State in state_list:
        y_lable = "$" + State[0] + '_{' + State[1:] + '}$'
        record.plot(x='t', y=State, linewidth=2,
                    ax=axes[subplot_id], legend=False, grid=True)
        axes[subplot_id].set_ylabel(y_lable)
        axes[subplot_id].get_xaxis().set_visible(False)
        # if State == 'vO':
        # axes[SubplotID].set_ylim([0.0,None])
        subplot_id += 1
    axes[subplot_id - 1].get_xaxis().set_visible(True)
    # plt.tight_layout()
    plt.show()
    return fig

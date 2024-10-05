import plotly.express as px


def linechart(df, col, reversed=False):
    '''
    '''
    fig = px.line(
        df,
        x='round',
        y=col,
        color='User',
        markers=True)

    for i in range(len(fig.data)):
        fig.data[i].line.color = '#B0B0B0'
        length = len(px.colors.qualitative.Pastel2)
        fig.data[i].marker.color = px.colors.qualitative.Pastel2[i % length]

    fig.update_traces(marker=dict(size=12))

    fig.update_xaxes(showgrid=False,
                     range=[0, 38])

    fig.update_yaxes(showgrid=False)

    if reversed:
        fig.update_yaxes(range=[23, 0], autorange=False)

    fig.update_layout(
        autosize=False,
        margin=dict(l=0, r=0, t=0, b=0, pad=0),
        height=500,
        xaxis_title=None,
        yaxis_title=None,
        showlegend=True,
        legend=dict(
            orientation="h",
            title=None),
        dragmode=False,
        xaxis_fixedrange=True,
        yaxis_fixedrange=True
      )
    return fig


def highlight_row(row, player_id):
    '''
    _summary_

    Args:
        player_id (_type_): _description_
    '''
    bcolor = '#f7f6fa' if row.name == player_id else ''

    color = 'background-color: {};color: #808080'.format(bcolor)

    return [color for i in range(len(row))]


def color_totals(res, inc_zero=False):
    '''
    _summary_

    Args:
        result (_type_): _description_
    '''
    if res > 0:
        tcolor = '#a5ddc3'

    elif res == 0 and inc_zero:
        tcolor = '#fbc29c'

    elif res < 0:
        tcolor = '#F56769'

    else:
        tcolor = '#808080'

    return 'color: {}'.format(tcolor)


def color_results(res):
    '''
    _summary_

    Args:
        result (_type_): _description_
    '''
    if res == 'Won':
        tcolor = '#a5ddc3'

    elif res == 'Drew':
        tcolor = '#fbc29c'

    elif res == 'Lost':
        tcolor = '#F56769'

    else:
        tcolor = '#808080'

    return 'color: {}'.format(tcolor)

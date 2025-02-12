import plotly.express as px
import streamlit as st 


def barchart(df, x, y, color):
    '''
    '''
    df['Performance'] = df[color].apply(lambda x: '+ Points' if x > 0 else ('0 Points' if x == 0 else '- Points'))
    df[color] = df[color].map(lambda x: str(x) + ' pts')

    # st.dataframe(df)

    fig = px.bar(
        df,
        x=x,
        y=y,
        color='Performance',  # Color bars based on 'Performance' category
        text=color,
        hover_data={color: False,
                    'Performance': False,
                    'users': False,
                    'player_count': False, 
                    'Choice': False},

        color_discrete_map={
            '+ Points': '#a5ddc3',   # Green for positive
            '0 Points': '#fbc29c',      # Orange for zero
            '- Points': '#F56769'      # Red for negative
        },
        title=None,
    )

    fig.update_layout(
        autosize=False,
        margin=dict(l=0, r=0, t=0, b=0, pad=0),
        height=400,
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False,
        legend=dict(
            orientation="h",
            title=None),
        dragmode=False,
        xaxis_fixedrange=True,
        yaxis_fixedrange=True
    )

    # Show the chart
    return fig


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
        fig.update_yaxes(range=[30, 0], autorange=False)

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


def highlight_choices(x):
    '''
    _summary_

    Args:
        x (_type_): _description_
    '''
    tcolor = '#808080'
    opacity = 0.1

    if not x['2nd Pick'] and not x['1st Pick']:
        # Green
        tcolor = '#a5ddc3'
        tcolor = 'rgb(165, 221, 194, {})'.format(opacity)

    if x['1st Pick']:
        # Yellow
        tcolor = '#fbc29c'
        tcolor = 'rgb(251, 194, 156, {})'.format(opacity)

    if x['2nd Pick']:
        # Red
        tcolor = '#F56769'
        tcolor = 'rgb(245, 103, 105, {})'.format(opacity)

    return ['background-color: {};'.format(tcolor) for _ in range(len(x))]

import plotly.express as px


def linechart(df, col, reversed = False):
    '''
    '''
    fig = px.line(
        df,
        x='round',
        y=col,
        color='USER',  
        markers=True)
    
    for i in range(len(fig.data)):
        fig.data[i].line.color = '#B0B0B0' 
        fig.data[i].marker.color = px.colors.qualitative.Pastel2[i % len(px.colors.qualitative.Pastel2)]  

    fig.update_traces(marker=dict(size=12)) 
    fig.update_xaxes(showgrid=False, range=[0, 15])
    fig.update_yaxes(showgrid=False)

    if reversed:
        fig.update_yaxes(autorange='reversed')

    fig.update_layout(
        autosize=False,
        margin=dict(l=0, r=0, t=0, b=0, pad=0),
        height = 300,
        xaxis_title=None,
        yaxis_title=None,
        showlegend=True
    )
    return fig
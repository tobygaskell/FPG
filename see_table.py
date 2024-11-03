import streamlit as st
import utils
import pandas as pd
import vis


def main(player_id, round):
    '''
    '''
    stand = utils.fpg_api_get('get_standings', player_id=player_id)

    standings = pd.DataFrame(stand)

    standings['Position'] = (standings['Position']
                             .map(lambda n: "%d%s" %
                             (n, "tsnrhtdd"[(n//10 % 10 != 1) *
                                            (n % 10 < 4) * n % 10::4])))

    standings = standings.set_index('player_id', drop=True)

    st.subheader('Overall Table', divider='grey')

    if st.toggle('See Goal Difference'):
        standings = standings[['Position', 'User', 'Goal Diff', 'Score']]

    else:
        standings = standings[['Position', 'User', 'Score']]

    styled_standings = (standings.style
                        .apply(lambda x: vis.highlight_row(x, player_id),
                               axis=1))

    st.dataframe(styled_standings,
                 use_container_width=True,
                 hide_index=True)

    st.subheader('Points Details', divider='grey')

    round_ops = [i+1 for i in range(round-1)]

    round_ops.sort(reverse=True)

    round_choice = st.selectbox('Pick a Round: ', round_ops)

    points = utils.fpg_api_get('get_points',
                               round_id=round_choice,
                               player_id=player_id)

    points = pd.DataFrame(points)

    if len(points) != 0:

        round_info = utils.fpg_api_get('get_round_info',
                                       round_id=round_choice,
                                       player_id=player_id)

        left, right = st.columns(2)

        left.button('Draw Means More Round',
                    disabled=not round_info['DMM'],
                    use_container_width=True,
                    type='primary')

        right.button('Double Points Round',
                     disabled=not round_info['Double'],
                     use_container_width=True,
                     type='primary')

        pts_choice = st.radio('Pick Pts Type',
                              ['Table', 'Chart'],
                              horizontal=True,
                              label_visibility='collapsed')
        if pts_choice == 'Chart':
            # st.dataframe(points)

            choice_cnt = points.groupby('Choice').agg(
                player_count=('player_id', 'count'),
                pts=('Total', 'max'),
                users=('User', list)
            ).reset_index()

            fig = vis.barchart(choice_cnt,
                               x='Choice',
                               y='player_count',
                               color='pts')

            st.plotly_chart(fig, config={'displayModeBar': False})
        elif pts_choice == 'Table':
            points = points.set_index('player_id', drop=True)

            styled_points = (points.style
                             .apply(lambda x: vis.highlight_row(x, player_id),
                                    axis=1)

                             .map(vis.color_results,
                                  subset=['Result'])

                             .map(vis.color_totals,
                                  subset=['Total'],
                                  inc_zero=True)

                             .map(vis.color_totals,
                                  subset=['Subtotal'],
                                  inc_zero=True)

                             .map(vis.color_totals,
                                  subset=['Basic'],
                                  inc_zero=True)

                             .map(vis.color_totals,
                                  subset=['Head 2 Head'],
                                  inc_zero=True)

                             .map(vis.color_totals,
                                  subset=['Derby'],
                                  inc_zero=True)

                             .map(vis.color_totals,
                                  subset=['Draw Means More'],
                                  inc_zero=True))

            st.dataframe(styled_points,
                         use_container_width=True,
                         hide_index=True)

    else:
        st.warning('Score not yet calculated for this round - come back soon!')

    st.subheader('Charts', divider='grey')

    chart_choice = st.radio('Pick Chart Type',
                            ['Score', 'Position'],
                            horizontal=True,
                            label_visibility='collapsed')

    stand = utils.fpg_api_get('get_rolling_standings', player_id=player_id)

    df = pd.DataFrame(stand)

    fig = vis.linechart(df, chart_choice,
                        False if chart_choice == 'Score' else True)

    st.plotly_chart(fig, config={'displayModeBar': False})

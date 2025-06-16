import streamlit as st
import utils

st.set_page_config(layout='wide')

st.title('FPG Feedback')


def question(title, type_):
    '''
    '''
    # left, right = st.columns(2)

    st.caption(title)

    data = st.feedback(type_, key=title)

    return data


def escape(val):
    if isinstance(val, str):
        return val.replace("'", "''")
    return val


def text(title, type_='area'):
    '''
    '''
    st.caption(title)

    if type_ == 'area':
        data = st.text_area(title, label_visibility='collapsed')

    elif type_ == 'line':
        data = st.text_input(title, label_visibility='collapsed')

    return data


@st.dialog('Thankyou')
def success():
    '''
    '''
    st.success('Thankyou for playing FPG and submitting feedback')


def check_values(needed):
    '''
    '''
    failed = False
    for answer in needed:
        if not answer[0] and answer[0] != 0:
            st.error('Please fill out question {} as it is a required question!'.format(answer[1]))
            failed = True

    return failed


st.caption(':red[*] Answered Needed ')

with st.form('feedback', border=True):

    st.subheader('Player Info')

    name = text('1) What is your name? :red[*]','line')

    st.subheader('Game Experiance')

    overall = question('2) What would you rate FPG as a concept? :red[*]', 'stars')

    enjoy_most = text('3) What do you enjoy most about FPG? :red[*]', 'line')

    frustrating = text('4) What do you find frustrating or confusing about FPG?', 'line')

    st.subheader('Game Play')

    balanced = question('5) Do you feel the game is fair and balanced? :red[*]', 'thumbs')

    intuative = question('6) How intuitive did you find the rules and the scoring system? :red[*]', 'stars')

    rule_changes = text('7) Do you think the rules need to be altered in anyway?', 'line')

    st.subheader('App Experiance')

    app = question('8) What would you rate the FPG mobile app experiance? :red[*]', 'stars')

    performance = question('9) How would you rate the speed and performance of the app? :red[*]', 'stars')

    difficult_to_use = text('10) Did you find any parts of the app hard to use?', 'line')

    st.subheader('Retention')

    continue_playing = question('11) Do you want to play FPG next season? :red[*]', 'thumbs')

    recommend = question('12) Would you recommend FPG to a friend? :red[*]', 'thumbs')

    money = question('13) Would you be willing to pay for any features? (premium leagues, stats, advanced analytics, etc.) :red[*]', 'thumbs')

    stop_playing = text('14) Did you stop playing, if so why? :red[*]', 'line')

    st.subheader('Additional')

    feature_requests = text('15) Do you have any feature requests you would like to see come to the app?')

    additional_comments = text('16) Do you have any additional comments?')

    if st.form_submit_button('Submit Feedback',
                             use_container_width=True,
                             type='primary'):

        needed = [(name, 1), (overall, 2), (enjoy_most, 3), (balanced, 5),
                  (intuative, 6), (app, 8), (performance, 9),
                  (continue_playing, 11), (recommend, 12), (money, 13),
                  (stop_playing, 14)]

        failed = check_values(needed)

        if not failed:
            query = '''
                INSERT INTO DEV_FPG.FEEDBACK
                (name, overall, enjoy_most, frustrating, balanced, intuative,
                rule_changes, app, performance, difficult_to_use,
                continue_playing, recommended, money, stop_playing,
                feature_requests, additional_comments, submitted_at)
                VALUES
                ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}',
                '{}', '{}', '{}', '{}', '{}', '{}', '{}', current_timestamp(2))
            '''.format(
                escape(name), overall, escape(enjoy_most), escape(frustrating),
                balanced, intuative, escape(rule_changes), app, performance,
                escape(difficult_to_use), continue_playing, recommend, money,
                escape(stop_playing), escape(feature_requests),
                escape(additional_comments))

            utils.run_sql_query(query, True)

            success()

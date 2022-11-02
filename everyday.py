
import utils 
import random 
import scores


def get_round(): 
    '''
    '''
    round_id = utils.get_api("https://api-football-v1.p.rapidapi.com/v3/fixtures/rounds", 
                            {"league":"39","season":"2022","current":"true"})[0][-2:].strip()
    return round_id


def check_if_round_has_changed(round_id): 
    '''
    '''
    changed = False

    query = '''
            SELECT DISTINCT round
            FROM logs
            WHERE time_added = (SELECT MAX(time_added) FROM logs)
            LIMIT 1
            '''
    last_round_id = utils.run_query(query)['ROUND'][0]

    print(last_round_id, round_id)

    if int(last_round_id) != int(round_id): 
        changed = True

    return changed, last_round_id


def get_results_for_last_round(round_id, last_round_id): 
    '''
    '''
    collected = False
    return collected


def calculate_scores(round_id, last_round_id): 
    '''
    '''
    # try: 
    query = '''
            SELECT a.player_id, b.team_choice, 
                COALESCE(NULLIF(HOME_TEAM, TEAM_CHOICE), NULLIF(AWAY_TEAM, TEAM_CHOICE)) AS OPPO, 
                b.round, b.fixture_id, D.DERBY, C.SCORE,
                
                CASE WHEN (home_team = TEAM_CHOICE AND home_goals > away_goals) 
                    OR (away_team = TEAM_CHOICE AND away_goals > home_goals) 
                THEN 'Win' 

                WHEN home_goals = away_goals 
                THEN 'Draw' 

                WHEN (home_team = TEAM_CHOICE AND home_goals < away_goals)
                    OR (away_team = TEAM_CHOICE AND away_goals < home_goals) 
                THEN 'Loss' 
                
                END AS result,
                CASE WHEN OPPO IN (SELECT DISTINCT TEAM_CHOICE FROM CHOICES WHERE ROUND = 14) THEN TRUE ELSE FALSE END AS HEAD_2_HEAD
                
            FROM PLAYERS AS A 
            LEFT JOIN CHOICES AS B
            ON A.PLAYER_ID = B.PLAYER_ID
            LEFT JOIN RESULTS AS C 
            ON B.FIXTURE_ID = C.GAME_ID
            LEFT JOIN FIXTURES AS D
            ON B.FIXTURE_ID = D.ID
            WHERE B.ROUND = {}
            '''.format(last_round_id)

    choices = utils.run_query(query)

    draw_round, double_round = get_round_details(last_round_id)

    for player in list(choices['PLAYER_ID']): 

        row = choices[choices['PLAYER_ID']== player].reset_index(drop = True)

        result = row['RESULT'][0]

        head_2_head = row['HEAD_2_HEAD'][0]

        derby = row['DERBY'][0]

        scores.main(player, result, head_2_head, derby, draw_round, double_round, last_round_id)

    calculated = True

    # except: 
    #     calculated = False

    return calculated


def get_round_details(round_id): 
    '''
    '''
    query = '''
            SELECT DOUBLE_POINT_ROUND, DRAW_ROUND 
            FROM ROUNDS 
            WHERE ROUND = {}
            '''.format(round_id)

    round_details = utils.run_query(query)

    double_round = round_details['DOUBLE_POINT_ROUND'][0]

    draw_round = round_details['DRAW_ROUND'][0]

    return draw_round, double_round

def configure_next_round(round_id): 
    '''
    '''
    try: 
        draw_round = random.randrange(100) < 10

        double_point_round = random.randrange(100) < 10

        query = '''
                SELECT MIN(kickoff) AS cutoff, DATE(MAX(kickoff)) AS end_date
                FROM fixtures 
                WHERE round = {}
                AND season = 2022
                '''.format(round_id)
        
        df = utils.run_query(query)

        cutoff = df['CUTOFF'][0]

        end_date = df['END_DATE'][0]

        query = '''
                INSERT INTO ROUNDS 
                VALUES
                ({}, {}, {}, '{}', '{}')
                '''.format(round_id, draw_round, double_point_round, cutoff, end_date)

        utils.run_query(query)

        configured = True
    except: 
        configured = False

    return configured


def save_log(round_id, collected, calculated, configured): 
    '''
    '''
    query = '''
            INSERT INTO LOGS
            VALUES
            (CURRENT_TIMESTAMP(2), {}, {}, {}, {})
            '''.format(round_id, collected, calculated, configured)
    utils.run_query(query)


def main():
    '''
    '''
    round_id = get_round()

    changed, last_round_id = check_if_round_has_changed(round_id) 

    collected = False
    calculated = False
    configured = False

    if changed: 
        collected = get_results_for_last_round(round_id, last_round_id)
        calculated = calculate_scores(round_id, last_round_id)
        configured = configure_next_round(round_id)

    save_log(round_id, collected, calculated, configured) 

if __name__ == '__main__': 
    main()
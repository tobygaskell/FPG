import utils

def get_basic_score(result): 
    '''
    '''
    if result == 'Win': 
        score = 1
    elif result == 'Draw': 
        score = 0 
    elif result == 'Loss':
        score = -1 
    else: 
        score = None
    return score

def get_h2h_score(result, head_2_head): 
    '''
    '''
    if head_2_head: 
        if result == 'Win': 
            score = 1
        elif result == 'Draw': 
            score = 0 
        elif result == 'Loss':
            score = -1 
        else: 
            score = None 
    else: 
        score = 0 

    return score

def get_derby_score(result, derby): 
    '''
    '''
    if derby: 
        if result == 'Win': 
            score = 1
        elif result == 'Draw': 
            score = -1 
        elif result == 'Loss':
            score = -1 
        else: 
            score = None 
    else: 
        score = 0 

    return score

def get_draw_score(result, draw_round): 
    '''
    '''
    if draw_round: 
        if result == 'Win': 
            score = 0
        elif result == 'Draw': 
            score = 2 
        elif result == 'Loss':
            score = 0 
        else: 
            score = None 
    else: 
        score = 0

    return score

def get_total(sub_total, double_round): 
    '''
    '''
    if double_round: 
        score = sub_total * 2 

    else: 
        score = sub_total

    return score

def write_scores(player, round_id, basic_score, head_2_head_score, derby_score, draw_score, double_round, total):
    '''
    '''
    query = '''
            INSERT INTO SCORES
            VALUES 
            ({}, {}, {}, {}, {}, {}, {}, {})
            '''.format(player, round_id, basic_score, head_2_head_score, 
                    derby_score, draw_score, double_round, total)

    utils.run_query(query)


def main(player, result, head_2_head, derby, draw_round, double_round, round_id): 
    '''
    '''
    basic_score = get_basic_score(result)

    head_2_head_score = get_h2h_score(result, head_2_head)

    derby_score = get_derby_score(result, derby)

    draw_score = get_draw_score(result, draw_round)

    sub_total = basic_score + head_2_head_score + derby_score + draw_score

    total_score = get_total(sub_total, double_round)

    write_scores(player, round_id, basic_score, head_2_head_score, derby_score, draw_score, double_round, total_score)





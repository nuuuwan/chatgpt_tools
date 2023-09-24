CMD_PREAMBLE = '''
The following is a part from a document:
'''

CMD_POSTAMBLE = '''
You will be asked a set of questions about the part.
'''


def get_cmd_summarize(n_bullets: int):
    return f'''
Summarize into {n_bullets} unnumbered bullet points,
including a space after each bullet paragraph.
        '''


CMD_PRETTIFY = '''
In your summary, append emojis next to words,
replace each bullet with an emoji that represents the bullet's content,
and replace words with hashtags and handles
        '''

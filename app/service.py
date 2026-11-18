from .analysis import summarize
from .storage import load

def report(root):
    content = load(root)
    return {'project': content['definition']['name'],
            'subject': content['definition']['subject'],
            'summary': summarize(content)}

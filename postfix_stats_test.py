import unittest

import postfix_stats

class LineReader(object):
    def __init__(self, lines):
        self.lines = lines

    def get(self):
        return self.lines.pop()

def get_line_reader(line):
    return LineReader([line])

class TestParser(unittest.TestCase):
    def test_parser(self):
        line = "Nov 10 08:06:58 smtprelay-foobar postfix-sendgrid/smtp[5818]: 788745E865: to=<removed>, relay=smtp.foobar.net[127.0.0.1]:587, delay=82, delays=0.2/80/0.46/0.55, dsn=2.0.0, status=sent (250 Ok: queued as bdT3qimVR7SSpBEKunexIg)"
        pln = postfix_stats.Parser.line_re.match(line)
        self.assertIsNotNone(pln)
        pline = pln.groupdict()
        self.assertEqual(pline['facility'], "postfix-sendgrid/smtp")
        # print pline['message']
        # message_pline = postfix_stats.Handler.filter_re.match(pline['message'])
        # message_dict = message_pline.groupdict()
        # print message_dict


if __name__ == "__main__":
    unittest.main()

import unittest
from mock import patch

import postfix_stats

class LineReader(object):
    def __init__(self, lines):
        self.lines = lines

    def get(self):
        return self.lines.pop()

def get_line_reader(line):
    return LineReader([line])

def reset_stats():
    postfix_stats.stats = {}

class TestParser(unittest.TestCase):
    def test_parser(self):
        line = "Nov 10 08:06:58 smtprelay-foobar postfix-sendgrid/smtp[5818]: 788745E865: to=<removed>, relay=smtp.foobar.net[100.34.12.12]:587, delay=82, delays=0.2/80/0.46/0.55, dsn=2.0.0, status=sent (250 Ok: queued as bdT3qimVR7SSpBEKunexIg)"
        pln = postfix_stats.Parser.line_re.match(line)
        self.assertIsNotNone(pln)
        pline = pln.groupdict()
        self.assertEqual(pline['facility'], "postfix-sendgrid/smtp")

class TestSmtpHandler(unittest.TestCase):
    def test_handle(self):
        line = "Nov 10 08:06:58 smtprelay-foobar postfix-sendgrid/smtp[5818]: 788745E865: to=<removed>, relay=smtp.foobar.net[100.34.12.12]:587, delay=82, delays=0.2/80/0.46/0.55, dsn=2.0.0, status=sent (250 Ok: queued as bdT3qimVR7SSpBEKunexIg)"
        handlers = postfix_stats.SmtpHandler()
        with patch.object(postfix_stats.Parser, 'start', return_value=None):
            parser = postfix_stats.Parser(get_line_reader(line))
            parser.parse_line(line)
            self.assertEqual(postfix_stats.stats['send']['status']['sent'], 1)
            self.assertEqual(postfix_stats.stats['send']['queue']['sendgrid']['sent'], 1)

class TestSmtpRecv(unittest.TestCase):
    def test_recv(self):
        line = "Nov 26 06:40:24 smtp-foobar postfix-sendgrid-high/smtpd[4701]: 65CE58285A: client=unknown[10.0.0.19]"
        handlers = (postfix_stats.SmtpdHandler(), postfix_stats.SmtpHandler())
        with patch.object(postfix_stats.Parser, 'start', return_value=None):
            parser = postfix_stats.Parser(get_line_reader(line))
            parser.parse_line(line)
            self.assertEqual(postfix_stats.stats['recv']['all'], 1)
            self.assertEqual(postfix_stats.stats['recv']['queue']['sendgrid-high'], 1)


if __name__ == "__main__":
    unittest.main()

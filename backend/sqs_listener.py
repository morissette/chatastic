#/usr/bin/env python
import threading
import sys, time, re
import json, subprocess, os, requests
from aws import create_session
import atexit
from signal import SIGTERM

class Daemon:

    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        os.chdir("/")
        os.setsid()
        os.umask(0)

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

	sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        print "Starting SQSListener"
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        self.daemonize()
        self.run()

    def stop(self):
        print "Stopping SQSListener"
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return

        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)

    def restart(self):
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """

class MyDaemon(Daemon):

    def run(self):
        session = create_session()
        response = session.get_queue_url(
            QueueName='MyChatQueue'
        )
        url = response['QueueUrl']

        # Setup how many workers should be listening to SQS
        workers = 5
        threads = []
        for i in range(workers):
            t = threading.Thread(target=self.worker, args=(i, session, url))
            threads.append(t)
            t.start()

    def worker(self, tid, client, url):
        """
        Check SQS Queue Every 5 Seconds
        """
        while True:
            self.check_sqs(client, url)

    def check_sqs(self, client, url):
        """
        Pull SQS queue and look for new messages
        """
        # Attempt to read Messages from SQS
        messages = client.receive_message(
            QueueUrl=url,
            AttributeNames=['All'],
            MaxNumberOfMessages=1,
            VisibilityTimeout=300,
            WaitTimeSeconds=5
        )

        # Read 1 Message and pass to worker
        if messages.get('Messages'):
            m = messages.get('Messages')[0]
            body = m['Body']
            receipt_handle = m['ReceiptHandle']
            if self.pass_msg(body):
                self.delete_msg(client, url, receipt_handle)

    def pass_msg(self, body):
        """
        Handle fork to api
        """
        decoded_body = json.loads(body)
        api_url = "http://127.0.0.1:5000"
        payload = json.dumps({
            "message": decoded_body['message']
        })
        requests.put(api_url + '/hipchat', payload)
        requests.put(api_url + '/slack', payload)
        requests.put(api_url + '/pagerduty', payload)
        requests.put(api_url + '/victorops', payload)
        return True

    def delete_msg(self, client, url, receipt_handle):
        """
        Delete message from SQS
        """
        response = client.delete_message(
                QueueUrl=url,
                ReceiptHandle=receipt_handle
                )

if __name__ == "__main__":
    daemon = MyDaemon('/home/mharris/Projects/var/run/sqs_listener.pid', '/dev/null', '/dev/stdout', '/dev/stderr')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

#!/usr/bin/env python
"""
The Tornado server used to receive operation requests and deliver results to the user.
"""
import json
import os, sys, psutil

from sys import stderr
from linguine.transaction import Transaction
from concurrent.futures import ThreadPoolExecutor
from linguine.transaction_exception import TransactionException

"""
Check to ensure Tornado is installed
"""
try:
    import tornado.ioloop
    import tornado.web
    #import tornado.exceptions.MultipleExceptionsRaised
except ImportError:
    sys.stderr.write("Tornado not found.")

class MainHandler(tornado.web.RequestHandler):
    numTransactionsRunning = 0
    transactions = []
    try:
        maxThreadPoolWorkers = int(os.environ['LINGUINE_THREADS'])
    except KeyError as err:
        maxThreadPoolWorkers = 2
    print("starting thread pool with " + str(maxThreadPoolWorkers) + " threads.")
    analysis_executor = ThreadPoolExecutor(max_workers=maxThreadPoolWorkers)

    def post(self):
        self.set_header('Content-Type', 'application/json')
        try:
            self.numTransactionsRunning+=1
            transaction = Transaction()
            self.transactions.append(transaction)
            requestObj = transaction.parse_json(self.request.body)
            transaction.read_corpora(transaction.corpora_ids)
            transaction.calcETA(self.numTransactionsRunning)
            analysis_id = transaction.create_analysis_record()

            #Generate response to server before kicking off analysis
            self.write(json.JSONEncoder().encode({'analysis_id': str(analysis_id)}))
            self.finish()

            #Encapsulate running of analysis in a future
            print("Submitting analysis " + str(analysis_id) + " to analysis queue")
            f = self.analysis_executor.submit(transaction.run, analysis_id, self)

#            print("Transactions: " + str(self.transactions))
            for p in psutil.pids():
                if psutil.Process(p).name() in ["python3.4", "java"]:
                    for child in psutil.Process(p).children():
                        cdict = child.as_dict(attrs=['pid', 'name', 'status', 'ppid'])
                        print("\t" + str(cdict))
                        if cdict['status'] in ['sleeping', 'zombie'] and self.numTransactionsRunning == 0:
                            print("There are no transactions running currently. Cleaning up idle java threads.")
                            child.kill()
#        except tornado.exceptions.MultipleExceptionsRaised as multiple:
#            for e in multiple.get_all_exceptions():
#                print("===========error==================")
#                try:
#                    print(json.JSONEncoder().encode({'error': err.error}))
#                except AttributeError as e:
#                    print(json.JSONEncoder().encode({'error': e.error}))
#                print("===========end_error==================")
        #Keep this error instance as a catch-all for all web requests
        except Exception as err:
            print("===========error==================")
            print(err.error)
            try:
                print(json.JSONEncoder().encode({'error': err.error}))
            except AttributeError as e:
                print(json.JSONEncoder().encode({'error': e.error}))
            print("===========end_error==================")
            self.set_status(err.code)
            self.write(json.JSONEncoder().encode({'error': err.error}))

if __name__ == "__main__":

    try:
        application = tornado.web.Application([(r"/", MainHandler)])
        application.listen(5555)
        tornado.ioloop.IOLoop.instance().start()
        for p in psutil.pids():
            if psutil.Process(p).name() in ["python3.4", "java"]:
                for child in psutil.Process(p).children():
                    cdict = child.as_dict(attrs=['pid', 'name', 'status', 'ppid'])
                    print("\t" + str(cdict))
                    if cdict['status'] in ['sleeping', 'zombie'] and self.numTransactionsRunning == 0:
                        print("There are no transactions running currently. Cleaning up idle java threads.")
                        child.kill()

    except KeyboardInterrupt:
        pass
    #Keep this error instance as a catch-all for all web requests
    except Exception as err:
        print("===========error==================")
        print(err)
        print(err.error)
        try:
            print(json.JSONEncoder().encode({'error': err}))
        except AttributeError as e:
            print(json.JSONEncoder().encode({'error': e}))
        print("===========end_error==================")
        self.set_status(err.code)
        self.write(json.JSONEncoder().encode({'error': err}))

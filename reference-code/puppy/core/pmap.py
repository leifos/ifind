from Queue import Empty, Queue
import threading


class error_wrap(object):
    def __init__(self, e, trace):
        self.e = e
        self.trace = trace


class finished(object):
    pass


class worker(object):
    """ Accomplishes tasks as an independent thread. """
    def __init__(self, employment_line):
        self.next_task = Queue()
        self.employment_line = employment_line
        self._thread = threading.Thread(target=self._run)
        self.last_id = None
        self.last_answer = None

    def delegate(self, item, assignment_id):
        """ Assign task to this worker. """

        if not self._thread.is_alive():
            self._thread.start()

        self.last_id = assignment_id
        self.next_task.put(item)

    def deactivate(self):
        """ Stop this worker. """

        if self._thread.is_alive():
            self.next_task.put(finished())
            self._thread.join()

    def _run(self):
        while True:
            task = self.next_task.get()
            if isinstance(task, finished):
                break
            fun, args = task
            try:
                result = fun(args)
            except Exception as e:
                import sys
                result = error_wrap(e, sys.exc_info()[2])

            self.last_answer = (args, result)
            self.employment_line.put(self)


class pmap(object):
    """ Behaves like itertools.imap, except parallelized into thread_count
    threads.

    :param func: function to apply
    :param iterable: iterable to which func is applied
    :param thread_count: number of threads to run.  If None, a thread will be created for each item in the iterable.
    :param catch: exceptions to catch.  Parent exceptions will catch child exceptions (e.g., setting 'Exception' will catch all child exceptions)
    :type catch: `tuple` of exceptions
    :param fun_return_on_exception: function to specify what is to be done in the case of an exception

    Format for `fun_return_on_exception` is as follows:

    >>> def fun_return_on_exception(input_causing_exception, exception):
    ...   # do something
    ...   return # something

    Example usage:

    >>> def waiter(i):
    ...    time.sleep(i)
    ...    return i
    >>>
    >>> for item in pmap(waiter, reversed(xrange(5))):
    ...    print item

    Exception handling:

    >>> def thrower(i):
    ...    raise IOError('ok')

    >>> def catcher(input, ex):
    ...    return i  # return input despite exception

    >>> for item in pmap(thrower, xrange(3), catch=(IOError, ),
    ...    fun_return_on_exception=catcher):
    ...    pass

    """

    def __init__(self, func, iterable, thread_count=8, catch=None,
            fun_return_on_exception=None):
        self.fun = func
        self.itr = iter(iterable)
        self.num_workers = thread_count
        self.running = True
        self.handle = fun_return_on_exception
        if catch is None:
            catch = ()
        self.catch = catch

        self.all_workers = []
        self.available_workers = Queue()

        for item in xrange(self.num_workers):
            employee = worker(self.available_workers)
            self.available_workers.put(employee)
            self.all_workers.append(employee)

        self._entered = False

    def __iter__(self):
        self._entered = True
        answers = {}
        current_response = current_assignment = 0
        more_items = True

        while more_items or current_response < current_assignment:
            try:
                employee = self.available_workers.get(timeout=.25)
            except Empty:
                # need to time out in case we were deactivated, in which case
                # the available_workers will be empty

                continue

            if employee.last_id is not None:
                answers[employee.last_id] = employee.last_answer

            while current_response in answers:
                (itr_input, result) = answers[current_response]
                del answers[current_response]
                current_response += 1

                if isinstance(result, error_wrap):
                    error = result.e

                    from cStringIO import StringIO
                    import traceback

                    trace_string = StringIO()

                    traceback.print_tb(result.trace, None, trace_string)
                    
                    setattr(error, 'pmap_trace', trace_string.getvalue())

                    if isinstance(error, self.catch):
                        if self.handle:
                            import inspect
                            params = len(inspect.getargspec(self.handle)[0])
                            if params == 2:
                                yield self.handle(itr_input, error)
                    else:
                        for employee in self.all_workers:
                            employee.deactivate()

                        #exception = type('pmap_exception', (type(error),), {'trace': result.trace})

                        raise error
                else:
                    yield result

            if more_items:
                try:
                    x = self.itr.next()
                    employee.delegate((self.fun, x), current_assignment)
                    current_assignment += 1
                except StopIteration:
                    more_items = False

            if not more_items:
                employee.deactivate()
                del employee

    def __del__(self):
        if not self._entered:
            list(self)

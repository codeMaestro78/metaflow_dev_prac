from metaflow.exception import METAFLOW_EXIT_DISALLOW_RETRY
from metaflow.runtime import NativeRuntime, TaskFailed


class _FakeTask:
    def __init__(self, retries=0, user_code_retries=0, error_retries=0):
        self.step = "mystep"
        self.task_id = "1"
        self.retries = retries
        self.user_code_retries = user_code_retries
        self.error_retries = error_retries


class _FakeWorker:
    def __init__(self, task, returncode, cleaned=False):
        self.task = task
        self._returncode = returncode
        self.cleaned = cleaned

    def terminate(self):
        return self._returncode

    def fds(self):
        return [99]


class _FakeEvent:
    fd = 99
    can_read = False
    is_terminated = True


class _FakePoll:
    def poll(self, timeout):
        return [_FakeEvent()]

    def remove(self, fd):
        pass


def _make_runtime(returncode, cleaned=False, task=None):
    rt = NativeRuntime.__new__(NativeRuntime)
    rt._logger = lambda *a, **k: None
    rt._active_tasks = {0: 1, "mystep": [1, 0]}
    rt._workers = {99: _FakeWorker(task or _FakeTask(), returncode, cleaned)}
    rt._poll = _FakePoll()
    rt._retry_worker = lambda w: (_ for _ in ()).throw(
        AssertionError("should not retry")
    )
    return rt


def test_disallow_retry_raises_task_failed():
    assert METAFLOW_EXIT_DISALLOW_RETRY == 202
    rt = _make_runtime(202, cleaned=False)
    try:
        list(rt._poll_workers())
    except TaskFailed as e:
        assert "mystep" in str(e)
    else:
        raise AssertionError("exit 202 should raise TaskFailed, got no exception")


def test_cleaned_worker_does_not_raise():
    # Orchestrator-killed workers are drained during _killall; must stay log-only.
    for rc in (202, 1):
        rt = _make_runtime(rc, cleaned=True)
        assert list(rt._poll_workers()) == []


def test_success_yields_task():
    task = _FakeTask()
    rt = _make_runtime(0, cleaned=False, task=task)
    assert list(rt._poll_workers()) == [task]

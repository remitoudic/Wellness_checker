from . import models
from . import wizard


def post_init_hook(env):
    """Seed the dashboard singleton with real data after first install."""
    env['wellness.dashboard']._refresh_pulse()


def post_load():
    """Called after every module load - used for patching."""
    pass

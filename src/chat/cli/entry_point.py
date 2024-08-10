from package_utils.context.entry_point import create_entry_point

from chat.context import context
from chat.main.main import main

entry_point = create_entry_point(main, context)

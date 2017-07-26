import click

from objection.utils.frida_transport import FridaRunner
from objection.utils.templates import android_hook


def show_android_classes(args: list = None) -> None:
    """
        Show the currently loaded classes.

        :param args:
        :return:
    """

    hook = android_hook('hooking/list-classes')
    runner = FridaRunner(hook=hook)
    runner.run()

    response = runner.get_last_message()

    if not response.is_successful():
        click.secho('Failed to list classes with error: {0}'.format(response.error_reason), fg='red')
        return None

    # print the enumerated classes
    for class_name in sorted(response.data):
        click.secho(class_name)

    click.secho('\nFound {0} classes'.format(len(response.data)), bold=True)


def watch_class_method(args: list) -> None:
    """
        Watches for invocations of an Android Java class method.
        All overloads are watched.

        :param args:
        :return:
    """

    if len(args) < 2:
        click.secho(('Usage: android hooking watch class_method <class> <method>'
                     ' (eg: com.example.test dologin)'), bold=True)
        return

    target_class = args[0]
    target_method = args[1]

    runner = FridaRunner()
    runner.set_hook_with_data(android_hook('hooking/watch-method'),
                              target_class=target_class, target_method=target_method)

    runner.run_as_job(name='watch-java-method')


def dump_android_method_args(args: list) -> None:
    """
        Starts an objection job that hooks into a class method and
        dumps the argument values as the method is invoked.

        :param args:
        :return:
    """

    if len(args) < 2:
        click.secho('Usage: android hooking dump_args <class> <method>', bold=True)
        return

    target_class = args[0]
    target_method = args[1]

    # prepare a runner for the arg dump hook
    runner = FridaRunner()
    runner.set_hook_with_data(android_hook('hooking/dump-arguments'),
                              target_class=target_class, target_method=target_method)

    runner.run_as_job(name='dump-arguments')
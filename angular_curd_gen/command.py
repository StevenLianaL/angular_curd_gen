import click


@click.group()
def ang():
    """top command"""
    pass


@ang.command()
def curd():
    """gen all curd pages"""
    pass


@ang.command()
def api():
    """gen api"""
    print('api')


@ang.command()
def router():
    """gen router"""
    pass


@ang.command()
def interface():
    """gen interface"""
    pass


@ang.command()
def component():
    """gen component"""
    pass


if __name__ == '__main__':
    ang()

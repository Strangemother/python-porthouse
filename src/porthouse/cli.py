
import arguments


def run():
    print('cli run')
    res = arguments.get_args()
    print(f'{res=}')
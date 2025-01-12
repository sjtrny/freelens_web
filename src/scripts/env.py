import os

from django.core.management.utils import get_random_secret_key

env_default_map = {
    "SECRET_KEY": lambda: get_random_secret_key(),
}


def main():

    out_dict = {}
    for env_var, default_fn in env_default_map.items():
        if env_var not in os.environ or not os.environ[env_var]:
            out_dict[env_var] = default_fn()

    print(" ".join([f"{key}={value}" for key, value in out_dict.items()]))

    return


if __name__ == "__main__":
    main()

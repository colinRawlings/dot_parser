# !python3

"""
Build the boost test binary for use testing the test discovery
"""

# imports

import subprocess as sp
import os
import shutil
import sys
import argparse

# definitions

BOOST_DIR = 'C:/third_party_libs/boost_1_70_0'
BOOST_BOOTSTRAP_NAME = "bootstrap.bat"
BOOST_BJAM_NAME = "b2.exe"

CPP_SOURCE_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'test_cpp_project'))
CPP_BUILD_PATH = os.path.join(CPP_SOURCE_PATH, 'build')
CPP_BIN_PATH = os.path.join(CPP_BUILD_PATH, 'bin')

CPP_TESTRUNNER_PATH = os.path.join(CPP_BIN_PATH, 'test_runner.exe')

TOOLCHAIN = dict(VS2015={"CMAKE_GENERATOR": 'Visual Studio 14 2015 Win64',
                         "BOOST_TOOLSET": "msvc-14.0"},
                 VS2017={"CMAKE_GENERATOR": 'Visual Studio 15 2017 Win64',
                         "BOOST_TOOLSET": "msvc-14.1"})

# functions

# functions: ui


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--boost_dir',
                        default=BOOST_DIR, help="path to boost")
    parser.add_argument('--use_vs2015', action='store_true',
                        help="Use Visual Studio 2015")
    parser.add_argument('--use_vs2017', action='store_true',
                        help="Use Visual Studio 2017")
    args = parser.parse_args()

    if args.use_vs2015 and args.use_vs2017:
        raise ValueError()

    if not args.use_vs2015 and not args.use_vs2017:
        raise ValueError("No Visual Studio toolchain specified")

    return args


def get_toolchain(args):
    if args.use_vs2015:
        return TOOLCHAIN["VS2015"]
    elif args.use_vs2017:
        return TOOLCHAIN["VS2017"]
    else:
        assert False

# functions: build


def build_boost(toolchain):
    """
    :params: toolchain: dict
    return: None (raise on failure)
    """

    if not os.path.isdir(args.boost_dir):
        raise ValueError(f"Invalid path to boost: {args.boost_dir}")

    bootstrap_path = os.path.join(args.boost_dir, BOOST_BOOTSTRAP_NAME)

    if not os.path.isfile(bootstrap_path):
        raise ValueError(
            f"Invalid path to boost ({bootstrap_path}) does not exist.")

    result = sp.run([bootstrap_path], cwd=args.boost_dir)
    if result.returncode != 0:
        raise RuntimeError()

    b2_path = os.path.join(args.boost_dir, "b2.exe")

    result = sp.run([b2_path, "--with-filesystem", "--with-test", "--with-regex", "--with-chrono",
                     f"toolset={toolchain['BOOST_TOOLSET']}", "address-model=64", "architecture=x86", "link=shared",
                     "threading=multi"],
                    cwd=args.boost_dir)
    if result.returncode != 0:
        raise RuntimeError()


def build_test_project(toolchain):
    """
    :params: toolchain: dict
    return: None (raise on failure)
    """

    if os.path.isdir(CPP_BUILD_PATH):
        shutil.rmtree(CPP_BUILD_PATH)

    os.mkdir(CPP_BUILD_PATH)

    result = sp.run(["cmake", '-G', toolchain["CMAKE_GENERATOR"], '..', f'-DBOOST_DIR={args.boost_dir}'],
                    cwd=CPP_BUILD_PATH)
    if result.returncode != 0:
        raise RuntimeError()

    result = sp.run(["cmake", '--build', '.'], cwd=CPP_BUILD_PATH)
    if result.returncode != 0:
        raise RuntimeError()

# main


if __name__ == "__main__":

    # args

    args = get_args()
    toolchain = get_toolchain(args)

    # Boost

    build_boost(toolchain)

    build_test_project(toolchain)

    sys.exit(int(not os.path.isfile(CPP_TESTRUNNER_PATH)))

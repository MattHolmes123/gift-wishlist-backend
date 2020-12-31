#!/bin/bash

poetry run pylint -j 4 \
    database \
    routers \
    tests  \
    wishlist

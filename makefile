MAKEFLAGS += --silent

-include .makefiles/*.mk

make:
	cat ./Makefile

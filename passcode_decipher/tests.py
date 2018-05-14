from time import sleep
import pygame, sys
import RPi.GPIO as GPIO
from classes.rotary import Rotary
from classes.algorithm import Algorithm
from classes.algorithm import AlgorithmType

algo = Algorithm(AlgorithmType.VIGENERE)
print (algo.encrypt("mathieu","ee"))

algo = Algorithm(AlgorithmType.BASE64)
print (algo.encrypt("mathieu"))

algo = Algorithm(AlgorithmType.ROT13)
print (algo.encrypt("mathieu"))

algo = Algorithm(AlgorithmType.ATBASH)
print (algo.encrypt("mathieu"))

algo = Algorithm(AlgorithmType.COLTRANS)
print (algo.encrypt("mathieu", "1234"))
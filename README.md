## rpi505A

## Introduction

This is a tool to automatically manage dorm505A, Zijing Apartment, Tsinghua Univ.


# Light on/off
	GET '/#{config['onpassword']}'
	GET '/#{config['offpassword']}'

# Humidity and Temprature
	GET '/env'

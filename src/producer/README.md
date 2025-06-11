# PRODUCER
This folder includes the source files that calculate the threshold to see if a BUY or SELL operation shall be performed.

---------------------      ----------------------------------------------------- If THR % > X   -----------------------
| Fetch Alpaca news | ---> | Request ChatGPT to calculate how good the news is | -------------> | Enqueue in RabbitMQ |
---------------------      -----------------------------------------------------                -----------------------

ChatGPT -> Given a prompt (in JSON format) will return a JSON with the % of how good this news is to invest in short term
RabbitMQ -> Shared Queue with the info to be consumed later and processed to do the pertinent investment operation

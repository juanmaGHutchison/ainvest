# CONSUMER
The consumer will process data introduced in the shared queue (RabbitMQ).

------------            --------  THR > Xbuy   ------
| RabbitMQ | ---------> | LTSM | ------------> | TODO
------------            --------
                            | THR < Xsell      ------
                            -----------------> | TODO

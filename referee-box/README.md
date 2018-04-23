# Ref-Box
Node for converting udp packet data in google protocol buffer type to custom rostype. 
This package publishes <code>referee/msg/debug_msg.msg</code> on the topic <code>'/ref_data'</code>

**Running**
```
chmod +x udp_recieve.py
rosrun referee udp_recieve.py
```
This runs the node which listens on 
```
host: '224.5.23.1'
port: 10003
```
converts the received data into <code>debug_msg</code> type and publishes on <code>'/ref_data'</code> topic.
# Machine Learning-Based DDoS (Distributed Denial of Service) Detection System

- Source code for my final project / dissertation

## Abstract:
- This project has created a framework for DDoS attack prediction using a set of modules to create a framework to tackle changes in network traffic and block incoming malicious traffic. This framework creates a hierarchical pipeline model that will block obvious malicious traffic early, and use machine learning techniques from multiple models to potentially detect more non-linear attack traffic patterns. 
- It uses a SDN (software defined networking) solution, chosen for its ease of use and effectiveness in controlling an entire network with multiple connected devices, which can scale to larger networks with more devices connected. 
- This framework was tested on multiple test cases, with a different and increasing number of nodes being targeted, increasing testing standards. 
- The first module uses a “window” of incoming packets from live traffic to discern whether the packets are coming from a common source too often, which can signal a flood attack from an attacker. 
- The second is aimed at preventing IP spoofing, by detecting associated duplicate IP and MAC addresses associated with each other, and blocks addresses with multiple associated MAC/IP addresses respectively. 
- The third is the Machine learning module, which classifies whether traffic is malicious and, is the last line of defence in the framework, and blocks bad traffic like the other 2 modules. 
- The fourth module is less about traffic detection and more about mitigating already discovered potential attacks and malicious source addresses, which are then forwarded to this module to be blocked and added to a blacklist. 
- This project was tested with MiniNet, a program to accurately simulate different required types of network traffic on a local machine, and the modules were connected to POX (a controller program) in order to implement a solution on MiniNet traffic. My supervisor also suggested using openDaylight, however its java based architecture and lack of integration with machine learning libraries such as Keras, means that it increases the complexity of implementation and is too complex for this project. 

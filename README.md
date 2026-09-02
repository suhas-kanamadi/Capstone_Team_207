Cyber-Physical Threat Detection in SCADA Systems Using Self-Attention Models and Federated Learning
Abstract

Cyber-Physical Systems (CPS) and Supervisory Control and Data Acquisition (SCADA) systems are critical components of modern industrial and smart-grid infrastructure. The increasing connectivity of these systems exposes them to cyber attacks that can manipulate sensor measurements, disrupt system behavior, and compromise the reliability of physical processes.

This project presents a cyber-physical threat detection framework for SCADA and smart-grid environments using real-time data streaming, cyber-attack simulation, anomaly detection, self-attention-based machine learning, and Federated Learning. The system simulates multiple cyber attacks on distributed client data and streams the resulting data through a Kafka-based communication layer. Apache Spark is used for stream processing, while the anomaly detection component analyzes the processed data to identify potentially malicious behavior.

The framework follows a distributed architecture consisting of clients/producers, attack injection modules, Kafka, Spark Streaming, anomaly detection, Federated Learning components, and a monitoring dashboard. The modular design allows different attack types and detection approaches to be incorporated without requiring major changes to the overall architecture.

1. Introduction

SCADA systems are widely used to monitor and control industrial processes, power systems, and other critical infrastructure. As these systems increasingly rely on networked communication and distributed computing, they become vulnerable to cyber-physical attacks.

Attackers may manipulate measurements, introduce false information, or gradually alter system values in an attempt to remain undetected. Such attacks can affect the reliability of monitoring and decision-making systems.

This project develops a real-time cyber-physical threat detection pipeline that combines distributed clients, attack simulation, Kafka-based messaging, Apache Spark Streaming, anomaly detection, self-attention-based machine learning, and Federated Learning.

The objective is to provide a modular environment in which different cyber attacks can be simulated and the resulting data can be analyzed to identify anomalous behavior.

2. Objectives

The main objectives of the project are:

To develop a cyber-physical threat detection framework for SCADA and smart-grid environments.
To simulate different types of cyber attacks on system data.
To provide a modular attack injection mechanism.
To stream data from multiple clients in real time.
To use Apache Kafka as the communication and message-broker layer.
To process streaming data using Apache Spark.
To detect anomalous behavior using machine-learning-based anomaly detection.
To investigate self-attention-based models for detecting complex patterns in sequential system data.
To incorporate Federated Learning for distributed model training.
To provide a dashboard for monitoring system activity and detection results.
To develop a modular architecture that can be extended with additional attacks, clients, and detection techniques.
3. Scope

The project focuses on the simulation and detection of cyber-physical attacks against SCADA and smart-grid data streams.

The scope includes:

Distributed client data generation and streaming.
Simulation of cyber attacks on client measurements.
Real-time transmission of data using Kafka.
Stream processing using Apache Spark.
Machine-learning-based anomaly detection.
Self-attention-based analysis of sequential data.
Distributed/Federated Learning architecture.
Monitoring and visualization through a dashboard.
Evaluation of normal and attack-injected data.

The project is intended as an academic and experimental framework. The attacks are simulated on project datasets and are not intended for deployment against real-world SCADA or industrial infrastructure.

4. Proposed System

The proposed system consists of distributed clients that provide SCADA/smart-grid measurements. Each client can stream its data through the system while an attack controller determines whether an attack should be applied.

When an attack is selected, the corresponding attack module modifies the client data according to the attack model. The resulting data is transmitted through Apache Kafka.

Kafka acts as the message-broker layer between data producers and downstream processing components. Apache Spark Streaming processes the incoming data and forwards it to the anomaly detection layer.

The anomaly detection component analyzes the incoming measurements and identifies potentially anomalous behavior. Self-attention-based machine-learning techniques are used to analyze sequential patterns, while the Federated Learning architecture supports distributed model training across participating clients.

The dashboard provides a monitoring interface for observing system activity and detection results.

5. System Architecture

The overall architecture of the project is:
                    +----------------------+
                    |   Client A Dataset   |
                    +----------+-----------+
                               |
                    +----------v-----------+
                    |   Client / Producer  |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |   Attack Controller  |
                    +----------+-----------+
                               |
          +--------------------+--------------------+
          |                    |                    |
          v                    v                    v
   +-------------+    +------------------+   +-------------+
   |  Byzantine  |    | Data Substitution|   |    Pulse    |
   |    Attack   |    |      Attack      |   |    Attack   |
   +-------------+    +------------------+   +-------------+
          |                    |                    |
          +--------------------+--------------------+
                               |
                               v
                       +---------------+
                       |     Kafka     |
                       |     Broker    |
                       +-------+-------+
                               |
                               v
                    +----------------------+
                    |  Spark Streaming     |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |  Anomaly Detection   |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Detection Results    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |      Dashboard       |
                    +----------------------+
The system can support multiple clients and attack types. The Ramp Attack is also implemented as part of the attack layer.

6. End-to-End Data Flow

The complete data flow is:Client Dataset
      |
      v
Client Sender
      |
      v
Attack Controller
      |
      v
Selected Attack
      |
      v
Kafka Broker
      |
      v
Spark Streaming
      |
      v
Anomaly Detection
      |
      v
Detection Results
      |
      v
Dashboard

For normal data, the attack stage can be bypassed so that the original measurements are streamed through the system.

For attack scenarios, the selected attack modifies the measurements before they are transmitted to Kafka.

7. Implemented Cyber Attacks

The project currently implements the following attack types.

7.1 Byzantine Attack

The Byzantine attack simulates malicious behavior from a participating client. A compromised client can provide manipulated information to the system, allowing the framework to evaluate the detection mechanism against unreliable or malicious client behavior.

This attack is particularly relevant to distributed and Federated Learning environments.

7.2 Data Substitution Attack

The Data Substitution Attack replaces legitimate measurement values with manipulated values.

It represents a scenario in which an attacker modifies sensor or operational measurements before the data reaches downstream processing and detection components.

7.3 Pulse Attack

The Pulse Attack introduces a sudden temporary change in measurement values.

This attack is useful for evaluating whether the detection system can identify short-duration abnormal behavior in an otherwise normal data stream.

7.4 Ramp Attack

The Ramp Attack introduces a gradual change in measurement values over a period of time.

This attack represents a slowly developing manipulation and allows the detection system to be evaluated against gradual deviations that may be less obvious than sudden changes.

8. Attack Injection Framework

The attack implementation is organized as independent modules under the attacks directory.

attacks/
├── attack_controller.py
├── byzantine_attack.py
├── data_substitution_attack.py
├── pulse_attack.py
└── ramp_attack.py

The attack_controller.py module provides a centralized mechanism for selecting and applying the appropriate attack.

This modular design allows additional attack types to be introduced without significantly modifying the client or downstream processing components.

The general attack workflow is:

Input Measurement
       |
       v
Attack Controller
       |
       +---- Byzantine Attack
       |
       +---- Data Substitution Attack
       |
       +---- Pulse Attack
       |
       +---- Ramp Attack
       |
       v
Modified Measurement
       |
       v
Kafka
9. Client and Producer Layer

The client layer represents distributed sources of SCADA/smart-grid measurements.

The project currently contains four client datasets:

clients/
├── client_A.csv
├── client_B.csv
├── client_C.csv
└── client_D.csv

The client-side streaming implementation is:

clients/client_sender.py

The client sender reads the selected dataset and streams its records into the attack and communication pipeline.

Multiple clients can be used to represent distributed data sources in the system.

10. Kafka Communication Layer

Apache Kafka is used as the message-broker and communication layer.

The producer sends streaming data to Kafka, while downstream components consume the data for processing and anomaly detection.

Kafka provides a decoupled communication mechanism between the client layer and the processing layer. This allows individual components to operate independently and supports the distributed nature of the architecture.

Kafka-related configuration is maintained within:

kafka_config/
11. Apache Spark Streaming

Apache Spark is used for stream processing.

The Spark component receives incoming data from the Kafka layer and processes the stream before passing the relevant information to the anomaly detection system.

The primary streaming component is:

spark_stream.py

Spark provides a distributed processing framework suitable for handling continuously arriving data and can be extended to support additional clients and larger workloads.

12. Anomaly Detection

The anomaly detection layer forms the core analytical component of the project.

The main anomaly detection component is:

anomaly_detector.py

The detector analyzes incoming SCADA/smart-grid measurements and identifies deviations from expected system behavior.

The system can process both normal and attack-injected data. Normal data provides the expected operating behavior, while attack-injected data provides controlled deviations that can be used to evaluate the detection capability.

13. Self-Attention-Based Detection

SCADA and smart-grid measurements are sequential and may contain relationships between observations over time.

Self-attention provides a mechanism for identifying important relationships within sequential input data. This allows the model to focus on relevant portions of the input when analyzing system behavior.

The project investigates self-attention-based machine-learning approaches for identifying anomalous patterns in cyber-physical system data.

Model-related components are maintained under:

models/

The self-attention approach provides a foundation for detecting complex patterns that may not be easily identified using simple threshold-based methods.

14. Federated Learning

The project incorporates a distributed learning architecture based on Federated Learning.

Multiple clients can represent independent data sources within the cyber-physical environment. Local model training can be performed at individual clients, after which model updates can be aggregated to develop an updated global model.

The conceptual workflow is:

                       Global Model
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
           Client A      Client B      Client C
              |             |             |
              v             v             v
        Local Training  Local Training  Local Training
              |             |             |
              +-------------+-------------+
                            |
                            v
                    Model Aggregation
                            |
                            v
                     Updated Model

This distributed architecture is relevant to SCADA and smart-grid environments where data may originate from multiple independent entities.

15. Master / Server Layer

The master/server components provide the server-side functionality required to coordinate different parts of the system.

These components are maintained under:

master/

The master layer interacts with the client, streaming, processing, and detection components as required by the project architecture.

16. Dashboard

The dashboard provides a monitoring interface for observing the operation of the threat detection system.

Dashboard-related components are maintained under:

dashboard/

The dashboard can be used to visualize relevant system information and detection results, providing a convenient interface for monitoring the streaming pipeline.

17. GridShield

The repository contains a gridshield directory containing project components associated with the GridShield implementation.

gridshield/

These components form part of the overall project implementation and are integrated according to their respective responsibilities.

18. Repository Structure

The overall repository is organized into functional modules:

Capstone_Team_207/
│
├── attacks/
│   ├── attack_controller.py
│   ├── byzantine_attack.py
│   ├── data_substitution_attack.py
│   ├── pulse_attack.py
│   └── ramp_attack.py
│
├── clients/
│   ├── __init__.py
│   ├── client_A.csv
│   ├── client_B.csv
│   ├── client_C.csv
│   ├── client_D.csv
│   └── client_sender.py
│
├── dashboard/
│   └── ...
│
├── gridshield/
│   └── ...
│
├── kafka_config/
│   └── ...
│
├── master/
│   └── ...
│
├── models/
│   └── ...
│
├── anomaly_detector.py
├── spark_stream.py
├── requirements.txt
├── .gitignore
└── README.md
Directory Description
Directory/File	Description
attacks/	Contains cyber-attack implementations and the attack controller.
clients/	Contains client datasets and the client-side data streaming implementation.
dashboard/	Contains dashboard and monitoring components.
gridshield/	Contains GridShield-related project components.
kafka_config/	Contains Kafka-related configuration.
master/	Contains master/server-side components.
models/	Contains machine-learning model-related components.
anomaly_detector.py	Main anomaly detection component.
spark_stream.py	Spark streaming component.
requirements.txt	Python dependencies required by the project.
.gitignore	Files and directories excluded from version control.

README.md	Project documentation.
19. Technologies Used
Programming Language
Python 3
Machine Learning
Self-Attention Models
Anomaly Detection
Federated Learning
Streaming and Distributed Processing
Apache Kafka
Apache Spark
Spark Streaming
Application and Server Technologies
FastAPI
Uvicorn
Data
CSV-based SCADA/smart-grid datasets
Distributed client datasets
Development Tools
Git
GitHub
Linux/Ubuntu
Visualization
Web-based monitoring dashboard
20. Installation Requirements

The following software is required to run the complete system:

Python 3
pip
Git
Apache Kafka
Apache Spark
Java runtime compatible with the installed Kafka and Spark versions

The exact versions may depend on the configuration of the deployment environment.

21. Installation
Clone the Repository
git clone <https://github.com/suhas-kanamadi/Capstone_Team_207>
cd Capstone_Team_207
Create a Virtual Environment
python3 -m venv venv

Activate the environment:

source venv/bin/activate

For Windows:

venv\Scripts\activate
Install Dependencies
pip install -r requirements.txt
22. Configuration

Before running the complete system, configure the required services and network parameters.

Important configuration areas include:

Kafka broker address
Kafka topic
Client configuration
Spark configuration
Master/server address
Network ports
Model configuration
Dashboard configuration


23. Running the Client

A client dataset can be streamed using:

python3 clients/client_sender.py clients/client_A.csv

Other client datasets can be used in the same way:

python3 clients/client_sender.py clients/client_B.csv
python3 clients/client_sender.py clients/client_C.csv
python3 clients/client_sender.py clients/client_D.csv

The client sender reads the selected dataset and streams its records into the project pipeline.

24. Running the System

The complete system consists of several services that work together.

A typical execution sequence is:

Start the Kafka broker and required Kafka services.
Configure the required Kafka topic.
Start the master/server components.
Start the Spark Streaming component.
Start the anomaly detection pipeline.
Start one or more client producers.
Configure the required attack scenario.
Stream the client data.
Observe the anomaly detection results.
Monitor the system using the dashboard.

The exact commands for individual components depend on the configuration and entry points used in the deployment.

25. Attack Testing

Each attack can be evaluated independently.

The recommended testing procedure is:

Start the complete streaming and detection pipeline.
Run a client using normal data.
Observe the system behavior.
Select an attack type.
Enable the selected attack through the attack controller.
Stream the client data.
Observe the detection output.
Repeat the experiment with other attack types.
Repeat the experiment using different client datasets.
Compare normal and attack-injected behavior.

This allows the detection system to be evaluated against different forms of malicious behavior.

26. Normal Data Flow

When no attack is applied, the original client measurements are streamed through the system.

Client Dataset
      |
      v
Client Sender
      |
      v
Kafka
      |
      v
Spark Streaming
      |
      v
Anomaly Detection
      |
      v
Dashboard

Normal data provides the baseline for evaluating the behavior of the detection system.

27. Attack Data Flow

When an attack is enabled, the data passes through the attack controller before being transmitted.

Client Dataset
      |
      v
Client Sender
      |
      v
Attack Controller
      |
      v
Selected Attack
      |
      v
Modified Data
      |
      v
Kafka
      |
      v
Spark Streaming
      |
      v
Anomaly Detection
      |
      v
Dashboard

This provides a controlled environment for evaluating the ability of the detection system to identify abnormal behavior.

28. Evaluation

The project can be evaluated using multiple performance dimensions.

Detection Performance

The ability of the anomaly detector to identify attack-injected measurements can be evaluated using classification metrics.

Attack Coverage

Each implemented attack can be tested separately to determine whether the detection pipeline identifies the corresponding anomalous behavior.

Streaming Performance

The system can be evaluated based on its ability to continuously process incoming data.

Distributed Processing

Multiple clients can be used to evaluate the behavior of the distributed architecture.

Federated Learning

The distributed learning architecture can be evaluated based on local model training, model aggregation, and global model performance.

Potential evaluation metrics include:

Accuracy
Precision
Recall
F1-score
Detection rate
False-positive rate
Detection latency
Processing throughput
29. Expected Outcomes

The expected outcome of the project is a working cyber-physical threat detection pipeline capable of processing streaming SCADA/smart-grid data and identifying anomalous behavior caused by simulated cyber attacks.

The framework provides:

Distributed client data sources
Configurable attack injection
Multiple cyber-attack scenarios
Real-time data streaming
Kafka-based communication
Spark-based stream processing
Machine-learning-based anomaly detection
Self-attention-based analysis
Federated Learning architecture
Dashboard-based monitoring
30. Advantages
Modular Design

The attack, client, processing, detection, and visualization components are separated into individual modules, making the system easier to maintain and extend.

Real-Time Processing

The streaming architecture allows continuously arriving data to be processed rather than relying exclusively on offline analysis.

Multiple Attack Scenarios

The framework supports multiple attack types, allowing the detection system to be evaluated under different malicious behaviors.

Distributed Architecture

Multiple clients can participate in the system, reflecting the distributed nature of SCADA and smart-grid environments.

Machine-Learning-Based Detection

Machine-learning-based techniques provide an additional layer of analysis beyond manually defined rules.

Self-Attention

Self-attention enables the analysis of relationships within sequential measurements and can help identify complex patterns.

Federated Learning

Federated Learning provides a framework for distributed model training across participating clients.

Scalable Communication

Kafka decouples data producers from downstream processing components and provides a scalable messaging architecture.

Distributed Stream Processing

Apache Spark provides distributed processing capabilities for continuously arriving data.

31. Limitations

The current project is primarily a software-based academic and experimental framework.

The cyber attacks are simulated using project datasets and streaming mechanisms rather than through direct interaction with physical SCADA hardware.

The effectiveness of the detection system depends on factors such as dataset quality, model configuration, available computational resources, and deployment configuration.

Real-world SCADA environments may contain additional communication protocols, device behavior, network conditions, and attack scenarios that are not fully represented in the current implementation.

Deployment in a production environment would require additional security hardening, extensive testing, fault tolerance, and validation.


Conclusion

This project presents a modular cyber-physical threat detection framework for SCADA and smart-grid environments by integrating distributed client data, cyber-attack simulation, Kafka-based communication, Apache Spark Streaming, anomaly detection, self-attention-based machine learning, Federated Learning, and dashboard-based monitoring.

The architecture separates data generation, attack injection, communication, stream processing, anomaly detection, distributed learning, and visualization into independent components. This modularity makes the system suitable for experimentation with multiple cyber-attack scenarios and detection approaches.

The implemented attack modules provide a controlled environment for evaluating the ability of the detection system to identify different forms of malicious behavior. The streaming architecture enables continuous processing of incoming measurements, while the distributed client and Federated Learning architecture provide a foundation for decentralized threat detection.

Overall, the project demonstrates an integrated approach to cyber-physical security by combining cybersecurity, machine learning, distributed computing, and real-time streaming technologies into a unified SCADA and smart-grid threat detection framework.
                    

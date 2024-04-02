# Celeb Look-Alike
<a name="readme-top"></a>

<!-- ABOUT THE PROJECT -->
## Introduction
In today's digital age, the fascination with celebrities and their lifestyles is more prevalent than ever. Social media platforms inundate users with images and updates of their favorite stars, fueling a desire to emulate their style, appearance, and even their facial features. With advancements in computer vision and machine learning, the concept of finding one's celebrity look-alike has transitioned from a mere curiosity to a captivating technological pursuit.

The Find Celebrity Look-alike Project seeks to fulfill this curiosity by leveraging cutting-edge image recognition algorithms to match users' facial features with those of well-known celebrities. Through the integration of sophisticated facial recognition technology, this project aims to provide users with an engaging and personalized experience, allowing them to discover their celebrity doppelgängers with remarkable accuracy.

At its core, the project utilizes deep learning models trained on vast datasets of celebrity images, enabling the system to identify subtle facial similarities and nuances. By employing convolutional neural networks (CNNs) and other machine learning techniques, the project can analyze facial landmarks, contours, and proportions to generate a comprehensive similarity score between the user's photo and a vast database of celebrity images.

The user experience is designed to be intuitive and seamless, allowing individuals to upload their photos effortlessly and receive instantaneous results. Leveraging cloud-based infrastructure, the project can efficiently process image data and deliver real-time recommendations, showcasing the closest matches to each user's facial characteristics.

Moreover, the Find Celebrity Look-alike Project offers a fun and interactive platform for users to explore their celebrity resemblances, fostering social sharing and engagement. Users can compare their matches with friends, share results on social media platforms, and even receive personalized recommendations for styling and makeup based on their celebrity counterparts.

In addition to its entertainment value, the project also holds potential applications in various industries, including marketing, advertising, and fashion. Brands can leverage the platform to identify influencers and endorsers who bear resemblances to popular celebrities, enhancing the effectiveness of their promotional campaigns and brand endorsements.

Overall, the Find Celebrity Look-alike Project represents a convergence of technology and pop culture, offering users a captivating glimpse into the world of celebrity resemblance while showcasing the power of machine learning and computer vision in delivering personalized experiences. As the project continues to evolve, it promises to redefine the way individuals interact with and perceive their favorite celebrities, transcending boundaries and creating new avenues for exploration and entertainment.

<!-- ARCHITECTURE -->
## Architecture
FaceDB is a Python library that provides an easy-to-use interface for face recognition and face database management. It allows you to perform face recognition tasks, such as face matching and face searching, and manage a database of faces efficiently. FaceDB supports two popular face recognition frameworks: DeepFace and face_recognition. Please visit this <a href="https://github.com/shhossain/FaceDB">link</a> to see details.
<p align="right">(<a href="#readme-top">Back to Top</a>)</p>

<!-- Used Technologies -->
## Used technologies
### FastAPI
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. It is designed to be easy to use, while also being fast and efficient. Some key features and advantages of FastAPI include:

* Fast and High Performance: FastAPI is built on top of Starlette and Pydantic, utilizing asynchronous programming to achieve high performance. It is one of the fastest web frameworks available for Python.

* Automatic API Documentation: FastAPI automatically generates interactive API documentation (using Swagger UI and ReDoc) based on the Python type hints, making it easy for developers to understand, test, and consume the API.

* Type Hints and Data Validation: FastAPI uses Python type hints for request and response data, enabling automatic data validation. This helps catch errors early in the development process and improves the overall reliability of the API.

* Dependency Injection System: FastAPI provides a built-in dependency injection system, making it easy to manage and inject dependencies into route functions.

* Security: It comes with built-in security features, such as OAuth and JWT token support, which simplifies the implementation of secure authentication and authorization in APIs.

* WebSocket Support: FastAPI supports WebSocket communication, allowing real-time bidirectional communication between clients and the server.

* Synchronous and Asynchronous Code: FastAPI supports both synchronous and asynchronous code, making it flexible for different use cases and allowing developers to leverage the benefits of asynchronous programming when needed.

* Easy Integration with Other Libraries: FastAPI seamlessly integrates with other popular Python libraries and frameworks, such as SQLAlchemy, Tortoise-ORM, and others.

* Automatic Generation of API Client Code: Using the generated OpenAPI documentation, FastAPI can automatically generate API client code in multiple programming languages, reducing the effort required to consume the API.

* Active Development and Community Support: FastAPI is actively developed and has a growing community. The framework is well-documented, and its community actively contributes to its improvement.

Overall, FastAPI is a modern and powerful web framework that prioritizes developer productivity, type safety, and high performance, making it an excellent choice for building APIs with Python.

### Uvicorn
Uvicorn is an ASGI (Asynchronous Server Gateway Interface) server that is specifically designed to run ASGI applications, such as those built with the FastAPI web framework. ASGI is a specification for asynchronous web servers and applications in Python, providing a standard interface between web servers and Python web applications or frameworks.

Here are some advantages of using Uvicorn:

* ASGI Support: Uvicorn supports the ASGI specification, which is designed to handle asynchronous programming and enables the development of highly concurrent web applications.

* Fast and Efficient: Uvicorn is known for its high performance and efficiency, making it well-suited for handling concurrent connections and delivering fast responses.

* Compatibility with FastAPI: Uvicorn is the recommended server for running FastAPI applications. When paired with FastAPI, it allows developers to take full advantage of asynchronous programming and achieve optimal performance.

* Ease of Use: Uvicorn is easy to install and use. It can be started with a single command, making it accessible for developers at all levels.

* WebSocket Support: Uvicorn supports WebSocket communication, allowing real-time bidirectional communication between clients and the server. This is particularly useful for applications that require real-time updates.

* Graceful Shutdown: Uvicorn supports graceful shutdowns, allowing existing requests to finish processing before the server stops. This helps maintain the stability and reliability of the application.

* Configuration Options: Uvicorn provides various configuration options, allowing developers to customize the server settings based on the requirements of their applications.

* TLS/SSL Support: Uvicorn supports TLS/SSL encryption, providing a secure way to transmit data over the network.

* Active Development and Community Support: Uvicorn is actively maintained and has a supportive community. Regular updates and contributions from the community ensure that the server stays up-to-date and improves over time.

* Integration with Other ASGI Frameworks: While commonly used with FastAPI, Uvicorn is not limited to a specific framework. It can be used with other ASGI frameworks and applications, providing flexibility and compatibility.

In summary, Uvicorn is a versatile and performant ASGI server that excels in handling asynchronous web applications. Its compatibility with FastAPI and support for WebSocket communication make it a popular choice for developers building modern, real-time web applications with Python. 

For this project, Uvicorn is using 3 workers. This means there will 3 subprocesses and the users can send requests in parallel. With this feature, the server can accept more than one request at the same time. You can increase the worker number regarding to your VRAM.

<p align="right">(<a href="#readme-top">Back to Top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started - Python
Instructions on setting up your project locally.
To get a local copy up and running follow these simple steps.

### Install dependencies
To install the required packages, in a terminal, type:
  ```sh
  pip install -r requirements.txt
  ```

### Run the project
To run the project, in a terminal, type:
  ```sh
  uvicorn app:app --proxy-headers --host 0.0.0.0 --port 8000 --workers 3
  ```
Then, visit <a href="http://localhost:8000/docs">http://localhost:8000/docs</a> to see the endpoints.

## Getting Started - Docker
Instructions on setting up your project locally using Docker.
To get a local copy up and running follow these simple steps.

### Build Docker
To build the Docker image, in a terminal, type:
  ```sh
  docker build -t celeb -f Dockerfile .
  ```

### Run the container
To run the container, in a terminal, type:
  ```sh
  docker run -it -d --name celeb -p 80:80 celeb
  ```
Then, visit <a href="http://localhost/docs">http://localhost/docs</a> to see the endpoints.

<p align="right">(<a href="#readme-top">Back to Top</a>)</p>


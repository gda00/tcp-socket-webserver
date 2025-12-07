# Multithreaded TCP Web Server

A raw HTTP server implementation using Python sockets, built to demonstrate the Application Layer protocols over TCP without external web frameworks.

## About The Project

This project evolves a basic TCP socket connection into a functional **HTTP/1.1 Web Server**. It manually handles socket creation, binds ports, and parses raw HTTP GET requests to serve static assets (HTML and Images) to standard web browsers (Chrome, Firefox, etc.).

## Core Features

* **Multithreading:** Handles multiple simultaneous browser connections (e.g., loading HTML and Favicon/Images in parallel) using Python's `threading`.
* **HTTP Protocol Implementation:** Manually constructs HTTP/1.1 headers (`200 OK`, `404 Not Found`, `Content-Type`).
* **Static File Serving:** Correctly serves text (`.html`) and binary (`.jpg`) files by determining MIME types.
* **Error Handling:** Detects non-existent files and returns a custom 404 HTML error page with the correct status code.

## How It Works

1.  **Server:** Listens on a specified TCP port (default: 2048).
2.  **Request:** Browser sends a standard `GET /file.html HTTP/1.1`.
3.  **Processing:** Server parses the request string to extract the filename.
4.  **Response:**
    * **Found:** Sends header `HTTP/1.1 200 OK` followed by the file's binary content.
    * **Not Found:** Sends header `HTTP/1.1 404 Not Found` and a generic error HTML.
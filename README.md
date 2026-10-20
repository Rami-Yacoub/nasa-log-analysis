# NASA Log Analysis

A data analysis project focused on processing and analyzing NASA web server access logs to explore website traffic patterns, HTTP requests, and server activity.

The project is organized into dedicated directories for analysis, source code, scripts, and generated results, providing a structured workflow for working with log data.

## 🎯 Project Objectives

- Process and analyze NASA web server access logs.
- Extract useful information from raw log records.
- Explore HTTP request patterns and server activity.
- Identify traffic trends and HTTP response status distributions.
- Generate results that support further investigation and data analysis.
- Practice data processing techniques using a real-world dataset.

## 📊 Dataset

The project is based on NASA web server access logs, which record HTTP requests made to a web server.

A typical log entry contains information such as:

- **Host:** The client hostname or IP address.
- **Timestamp:** The date and time of the request.
- **HTTP Request:** The requested resource and HTTP method.
- **Status Code:** The HTTP response status.
- **Response Size:** The amount of data returned by the server.

Example log entry:

```text
199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] "GET /history/apollo/ HTTP/1.0" 200 6245
```

This record describes an HTTP request for a NASA website resource, including its timestamp, response status, and response size.

## 🔍 Analysis Workflow

The project is structured around the following general workflow:

1. **Data Input:** Access the available NASA log data.
2. **Data Processing:** Process the log records and extract relevant information.
3. **Data Analysis:** Examine request patterns, traffic activity, and response information.
4. **Results Generation:** Store analysis outputs and results for further inspection.

## 🛠️ Technologies and Tools

The repository includes source code, scripts, an analysis directory, and a results directory.

| Component | Purpose |
|---|---|
| Source code (`src/`) | Main implementation and processing logic |
| Scripts (`scripts/`) | Supporting scripts and execution tasks |
| Analysis (`analysis/`) | Analysis-related files and exploration |
| Results (`nasa-results/`) | Generated or collected project results |

*The exact programming languages, libraries, and processing frameworks should be documented according to the implementation in the repository.*

## 📂 Project Structure

```text
nasa-log-analysis/
├── analysis/       # Analysis-related files
├── nasa-results/   # Analysis results
├── scripts/        # Supporting scripts
├── src/            # Source code
└── .gitignore
```

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Rami-Yacoub/nasa-log-analysis.git
cd nasa-log-analysis
```

### 2. Explore the Project

Review the source code and supporting scripts to identify the required dependencies, input data, and execution procedure.

### 3. Run the Analysis

Follow the instructions and execution commands associated with the scripts and source files included in the repository.

The required environment and commands depend on the implementation and its dependencies.

## 💡 Key Learning Outcomes

- Working with server log data.
- Understanding semi-structured data processing.
- Extracting useful information from HTTP access records.
- Exploring web traffic and server activity.
- Organizing data processing code and analysis outputs.
- Developing practical data analysis and problem-solving skills.

## 👨‍💻 Author

**Rami Yacoub**

- GitHub: [@Rami-Yacoub](https://github.com/Rami-Yacoub)
- Repository: [NASA Log Analysis](https://github.com/Rami-Yacoub/nasa-log-analysis)

---

*An exploratory data analysis project based on NASA web server access logs.*

import subprocess

def run_postgres_container():
    command = [
        "docker", "run", "--name", "my_postgres_container",
        "-e", "POSTGRES_USER=postgres",
        "-e", "POSTGRES_PASSWORD=mytestpassword",
        "-e", "POSTGRES_DB=my_fastapi_db",
        "-p", "2345:5432",
        "-d", "postgres"
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Container started successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error starting container:")
        print(e.stderr)

if __name__ == "__main__":
    run_postgres_container()
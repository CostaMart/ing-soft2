import subprocess


def run_pylint(file_name):
    command = ["pylint","--disable=C0103", file_name]

    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running pylint on {file_name}:")
        print(e.stderr)
    else:
        print(f"Pylint output for {file_name}:\n{result.stdout}")

def main():
    # Leggi i nomi dei file dal file static_analysis.txt
    with open("static_analysis.txt", "r") as file:

        # Leggi e rimuovi eventuali spazi bianchi e a capo
        file_names = [line.strip() for line in file]
        # Analizza ciascun file con Pylint
        for file_name in file_names:
            # Unisci il percorso del progetto e il nome del file
            full_path = f"{file_name}.py"
            run_pylint(full_path)


if __name__ == "__main__":
    main()

import sys
import csv
import os 
import subprocess

# Functions
def parse_csv_data(file:str) -> tuple[list[str], list[list[str]]]:
    """
    Parses CSV data from the given file.

    Args:
        file (str): The path to the CSV file.

    Returns:
        tuple[list[str], list[list[str]]]: A tuple containing:
            - The headers of the CSV file as a list of strings.
            - The data of the CSV file as a list of lists of strings.

    Raises:
        OSError: If the file does not exist.
    """
    if not os.path.exists(file):
        raise OSError(f"{file} doesn`t exists!")

    data = []                                                                      # list of list containing table content
    with open(file, "r", newline="") as f:
        reader = csv.reader(f)
        for i, rows in enumerate(reader):
            if i == 0:
                headers = [k.strip() for k in rows]
            else:
                data.append([k.strip() for k in rows])
    return headers, data


def create_table_headers(headers: list) -> str:
    """
    Creates the HTML table headers from the given list of headers.

    Args:
        headers (list): A list of header strings.

    Returns:
        str: The HTML table headers as a string.
    """
    result = ""
    result += "<tr>\n"
    for i in headers:
        result += f"<th>{i}</th>\n"
    result += "</tr>\n"
    return result


def create_table_body(table_content:list) -> str:
    """
    Creates the HTML table body from the given list of table content.

    Args:
        table_content (list): A list of lists representing table rows.

    Returns:
        str: The HTML table body as a string.
    """
    result = ""
    for row in table_content:   
        result += "<tr>\n"
        for i in row:
            result += f"<td>{i}</td>\n"
        result += "</tr>\n"
    return result
    
    
def writeToHtml(file:str, html_content:str) -> None:
    """
    Writes to a html file
    
    Args:
        file(str): Path to the html File.
        html_content(str): HTML content to write to the file.
    """
    with open(file, "w") as htmlFile:
        htmlFile.write(html_content)


def validateFileExistence(file:str) -> None:
    if not os.path.exists(file):
        raise FileNotFoundError(f"{file} was not found.")


def validateFileExt(file: str, expected_extension: str) -> None:
    _, actual_extension = os.path.splitext(file)
    if actual_extension != expected_extension:
        raise ValueError(f"ExtensionError: File should have the extension {expected_extension}.")


def handle_command_line_args() -> tuple[str, str]:
    """
    Handles command-line arguments.

    Returns:
        tuple[str, str]: A tuple containing the CSV file path and HTML file path.

    Raises:
        NameError: If there is an issue with command-line arguments.
        RuntimeError: If there is an issue with file existence or extension validation.
    """
    usage = "Usage: python3 main.py <CSV_FILE> <HTML_FILE>"

    try:
        csv_file = sys.argv[1]
        html_file = sys.argv[2]

        if len(sys.argv) != 3:
            raise UsageError(usage)

        validateFileExistence(csv_file)
        validateFileExt(csv_file, ".csv")
        validateFileExt(html_file, ".html")

        return csv_file, html_file

    except IndexError:
        raise NameError(usage)
    except (FileNotFoundError, ValueError) as e:
        raise RuntimeError(f"Error: {e}")


def main(openFile=True):
    """
    The main function of the CSV to HTML converter.

    Args:
        open_file (bool, optional): Whether to automatically open the generated HTML file. Defaults to True.
    """

    csv_file, html_file = handle_command_line_args()

    table_headers = create_table_headers(parse_csv_data(csv_file)[0])
    table_body = create_table_body(parse_csv_data(csv_file)[1])

    name, ext = os.path.splitext(csv_file)

    # Html content
    html_head = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title> {0} </title>
        <style>
            header h1 {{
                font-weight: 500;
                text-align: center;
                color: indianred;
            }}

            table {{
                width: 100%;
                border: 0.5px solid salmon;
                vertical-align: bottom;
            }}

            th,
            td {{
                padding: 5px 5px;
            }}

            table th {{
                background-color: #d79797;
                text-align: center;
                min-width: 100px;
                height: 35px;
            }}

            table td {{
                background-color: rgb(227, 204, 204);
                text-align: center;
            }}

            hr {{
                width: 97%;
                color: indianred;
                padding: 0px 10px;
            }}
        </style>
    </head>
    """.format(name)

    html_body = """
    <header>
        <h1><b><u>{0}</u></b></h1>
    </header>

    <hr>
    <body>
        <table>
            {1}
            {2}
        </table>
    <hr>
    </body>
    </html>
    """.format(name,table_headers, table_body)
    html_content = html_head + html_body                                                 # concatenating the final html code

    writeToHtml(html_file, html_content)                                                 # writing the html code

    if openFile:
        try:
            result = subprocess.run(["open {}".format(html_file)], shell=True)           # open the html file in a browser
        except Exception as e:
            print("Error Opening File: ", e)


def _mainTemp():
    ''' Temporary main function '''
    print(create_table_body(parse_csv_data("nba.csv")[1]))

if __name__ == "__main__":
    main()




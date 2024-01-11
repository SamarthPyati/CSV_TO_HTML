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


def main(openFile=True):
    """
    The main function of the CSV to HTML converter.

    Args:
        open_file (bool, optional): Whether to automatically open the generated HTML file. Defaults to True.
    """

    usage = "Usage: python3 <main.py> <CSV_FILE> <HTML_FILE>"

    try:
        csv_file = sys.argv[1]
        html_file = sys.argv[2]
    except IndexError as e:
        raise IndexError(usage)

    if len(sys.argv) != 3:
        raise UsageError(usage)

    if ".csv" not in csv_file:
        print('Missing ".csv" file extension from first command-line argument!')
        print("Exiting program...")
        sys.exit(1)

    if ".html" not in html_file:
        print('Missing ".html" file extension from second command-line argument!')
        print("Exiting program...")
        sys.exit(1)

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
        <title> Table </title>
        <style>
            h1 {
                /* text-align: center; */
                font-weight: 500;
            }

            table {
                width: 100%;
                border: 0.5px solid salmon;
                vertical-align: bottom;
            }

            th,
            td {
                padding: 5px 5px;
            }

            table th {
                background-color: #d79797;
                text-align: center;
                min-width: 100px;
                height: 35px;
            }

            table td {
                background-color: rgb(227, 204, 204);
                text-align: center;
            }
        </style>
    </head>
    """

    html_body = """
    <body>
        <table>
            {0}
            {1}
        </table>
    </body>
    </html>
    """.format(table_headers, table_body)
    html_content = html_head + html_body                                                 # concating the final html code

    writeToHtml(html_file, html_content)                                                 # writing that html code

    if openFile:
        try:
            result = subprocess.run(["open {}".format(html_file)], shell=True)           # opening the code
        except Exception as e:
            print("Error Opening File: ", e)


def _mainTemp():
    ''' Temporary main function '''
    print(create_table_body(parse_csv_data("nba.csv")[1]))

if __name__ == "__main__":
    main()




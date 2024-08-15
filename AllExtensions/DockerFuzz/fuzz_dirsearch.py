import concurrent.futures
import requests
import argparse
import concurrent.futures
import requests

def fetch(url):
    response = requests.get(url)
    if response.status_code == 200:
        result = f"Found: {url} - Status Code: {response.status_code}\n"
    else:
        result = f"Not Found: {url} - Status Code: {response.status_code}\n"
    print(result)  
    return result

def fuzz_dir(url, wordlist_file, output_file):
    with open(wordlist_file, "r") as f:
        directories = f.read().splitlines()
    
    urls = [f"{url}/{directory}" for directory in directories]
    
    with open(output_file, "w") as out_file:
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
            futures = [executor.submit(fetch, url) for url in urls]
            for future in concurrent.futures.as_completed(futures):
                out_file.write(future.result())

if __name__ == "__main__":
    print("""
  ooooo   ooooo ooooooooooooo ooooooooooooo ooooooooo.    .oooooo..o          88      88       .o.       ooo        ooooo       .o.       ooooo             88 oooooooooooo ooooo     ooo  oooooooooooo  oooooooooooo 
`888'   `888' 8'   888   `8 8'   888   `8 `888   `Y88. d8P'    `Y8         .8'     .8'      .888.      `88.       .888'      .888.      `888'            .8' `888'     `8 `888'     `8' d'""""""d888' d'""""""d888' 
 888     888       888           888       888   .d88' Y88bo.             .8'     .8'      .8"888.      888b     d'888      .8"888.      888            .8'   888          888       8        .888P         .888P   
 888ooooo888       888           888       888ooo88P'   `"Y8888o.        .8'     .8'      .8' `888.     8 Y88. .P  888     .8' `888.     888           .8'    888oooo8     888       8       d888'         d888'    
 888     888       888           888       888         oo     .d8P `"' .8'     .8'      .88ooo8888.    8  `888'   888    .88ooo8888.    888          .8'     888    "     888       8     .888P         .888P      
 888     888       888           888       888         88888888P'  o8o 88      88      o88o     o8888o o8o        o888o o88o     o8888o o888ooooood8 88      o888o           `YbodP'    .8888888888P  .8888888888P  
                                                                     `"'                                                                                                                                              
                                                                                                                                                                                                                        
                                                                                                                                                                                                                        
github:coming soon
    """)

    target_url = input("Enter target URL: ")
    wordlist_file = input("Enter wordlist file name: ")
    output_file = input("Enter output file name: ")

    fuzz_dir(target_url, wordlist_file, output_file)

    print("Process finished. Results saved to", output_file)

def fetch(url, status_code=None):
    response = requests.get(url)
    if status_code is not None and response.status_code != status_code:
        return None
    if response.status_code == 200:
        return f"Found: {url} - Status Code: {response.status_code}\n"
    else:
        return f"Not Found: {url} - Status Code: {response.status_code}\n"

def fuzz_dir(url, wordlist_file, status_code=None):
    with open(wordlist_file, "r") as f:
        directories = f.read().splitlines()
    
    urls = [f"{url}/{directory}" for directory in directories]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = [executor.submit(fetch, url, status_code) for url in urls]
        results = []
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                results.append(future.result())
    
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fuzz directory with optional status code filter")
    parser.add_argument("target_url", help="Target URL to fuzz")
    parser.add_argument("wordlist_file", help="Wordlist file containing directories")
    parser.add_argument("-mc", "--match_code", type=int, help="Status code to filter matching responses")
    parser.add_argument("-o", "--output_file", help="Output file name to save results")

    args = parser.parse_args()

    results = fuzz_dir(args.target_url, args.wordlist_file, args.match_code)

    if args.output_file:
        with open(args.output_file, "w") as f:
            f.writelines(results)
        print("Process finished. Results saved to", args.output_file)
    else:
        for result in results:
            print(result)

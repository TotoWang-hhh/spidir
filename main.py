import log
import network
import cli

VERSION="0.1.1"

if __name__=="__main__":
    print("Welcome to Spidir!")
    print("2024 by rgzz666")
    print(f"v{VERSION}")
    print("==============================\n")
    print("Program started.")
    url=input("Enter URL: ")
    parser=cli.ask_parser()
    save_path=input("Download files to: ")
    log.info("Starting parsing and download...")
    network.main(url,parser,save_path)

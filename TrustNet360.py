import re
import csv
import glob
import sys
import asyncio
import os
import argparse
from collections import defaultdict
import pycountry_convert as pc
from rich import print
from rich.console import Console
from rich.style import Style
from rich.table import Column, Table
from selenium import webdriver
from pyppeteer import launch
from selenium.webdriver.firefox.options import Options
from time import sleep
from bs4 import BeautifulSoup

console = Console()
style = Style()

def Banner():
    console.print("""[#00FFFF]

████████╗██████╗ ██╗   ██╗███████╗████████╗███╗   ██╗███████╗████████╗██████╗  ██████╗  ██████╗ 
╚══██╔══╝██╔══██╗██║   ██║██╔════╝╚══██╔══╝████╗  ██║██╔════╝╚══██╔══╝╚════██╗██╔════╝ ██╔═████╗
   ██║   ██████╔╝██║   ██║███████╗   ██║   ██╔██╗ ██║█████╗     ██║    █████╔╝███████╗ ██║██╔██║
   ██║   ██╔══██╗██║   ██║╚════██║   ██║   ██║╚██╗██║██╔══╝     ██║    ╚═══██╗██╔═══██╗████╔╝██║
   ██║   ██║  ██║╚██████╔╝███████║   ██║   ██║ ╚████║███████╗   ██║   ██████╔╝╚██████╔╝╚██████╔╝
   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═════╝  ╚═════╝  ╚═════╝ 
                                                                                                
                                 [link=https://github.com/trilokisingh]Check out my GitHub profile!
                                                                https://github.com/trilokisingh[/link]
                                                                                 """, style=style)



def arguments():
    parser = argparse.ArgumentParser(usage="python " + sys.argv[0] + " file_contains_ip_list.txt")
    parser.add_argument("file", help="A file containing IP addresses should be provided")
    parser.add_argument("-vt", "--virustotal", help="Take screenshots for evidence with VirusTotal", action='store_true')
    
    args = parser.parse_args()
    vt = args.virustotal

    return args.file, vt

def directorys():
    try:
        os.makedirs('Trust-Rep/screenshots')
    except FileExistsError:
        pass

async def spam():
    print("[#00FF00][+] Starting...")
    file, vt = arguments()
    with open(file, 'r') as f:
        lines = f.readlines()
    browser = await launch(options={'args': ['--no-sandbox']}, headless=True)
    page = await browser.newPage()
    await page.goto("https://www.bulkblacklist.com/")
    await page.waitForSelector("[name=ips]")
    await page.click("[name=ips]")
    for line in lines:
        await page.keyboard.type(line.strip())
        await page.keyboard.press("Enter")
    sleep(4)
    await page.click('input[type="submit"]')
    await page.waitForSelector("table.table-hover", visible=True)
    sleep(6)
    await page.pdf({'path':'./Trust-Rep/BulkBlacklist.pdf'})
    content = await page.content()
    soup = BeautifulSoup(content, "html.parser")
    s = soup.select("td > a")
    list1 = [n for n in s]
    for i in range(len(list1)):
        l = str(list1[i])
        if "r.png" in l:
            ip = re.findall(r'[0-9]+(?:.[0-9]+){3}', l)
            ip = ip[0]
            
            with open('unsorted.txt', 'a') as f:
                f.write('%s\n' %ip)

    print("[+] PDF written successfully...")

    with open('unsorted.txt', 'r') as f:
        lines = set(f.readlines())
        lines = list(lines)
        with open("ip.txt", 'w') as f:
            for i in lines:
                i = i.strip()
                f.write('%s\n' %i)
                
async def whois():
    file, t = arguments()
    with open(file, 'r') as f:
        lines = f.readlines()
    
    browser = await launch(options={'args': ['--no-sandbox']}, headless=True)
    page = await browser.newPage()
    await page.goto("https://www.infobyip.com/ipbulklookup.php/")
    await page.waitForSelector("[name=ips]")
    await page.click("[name=ips]")
    
    for line in lines:
        await page.keyboard.type(line.strip())
        await page.keyboard.press("Enter")
    
    await page.click('input[type="submit"]')
    xp = '//a[contains(text(), "Download CSV")]'
    await page.waitForXPath(xp)
    accept, = await page.xpath(xp)
    await accept.click()
    await page._client.send("Page.setDownloadBehavior", {
        "behavior": "allow",
        "downloadPath": os.getcwd()  # Set the download path to the current working directory
    })
    
    # Wait for the CSV file to be downloaded
    while not any(fname.endswith('.csv') for fname in os.listdir()):
        await asyncio.sleep(1)
    
    csv_files = glob.glob('*.csv')
    if not csv_files:
        # Create a dummy CSV file if none is found
        with open('dummy.csv', 'w') as dummy_file:
            dummy_file.write("Header1,Header2,Header3\n")
        csv_file = 'dummy.csv'
    else:
        csv_file = csv_files[0]
    
    destination = './Trust-Rep/whoislookup.csv'
    
    try:
        os.rename(csv_file, destination)
        print("CSV file downloaded successfully.")
    except Exception as e:
        print(f"Error moving CSV file: {e}")

def screenshots(value=False):
    print("[+] Taking Screenshots...")
    file_path = 'ip.txt'
    destination_path = './Trust-Rep/spamedips.txt'
    
    if os.path.exists(destination_path):
        os.remove(destination_path)
    
    with open(file_path) as file:
        for line in file:
            print("IP: {}".format(line.strip()))
            ips = line.strip()
            option = Options()
            option.headless = True
            driver = webdriver.Firefox(options=option)
            driver.set_window_size(1920,1080)
            if value == True:
                driver.get('https://www.virustotal.com/gui/ip-address/' + ips )
            else:
                driver.get('https://mxtoolbox.com/SuperTool.aspx?action=blacklist%3a' + ips + '&run=toolpage')
            sleep(4)
            driver.get_screenshot_as_file("Trust-Rep/screenshots/" + ips + ".png")
            driver.quit()
    
    os.renames(file_path, destination_path)
    print("[+] Screenshots have been saved...")

def conti(value=True):
    columns = defaultdict(list)
    file = './Trust-Rep/whoislookup.csv'
    
    if not os.path.exists(file):
        print("CSV file not found in the directory.")
        return
    
    try:
        with open(file) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                for (i, v) in enumerate(row):
                    columns[i].append(v)
            ip = columns[0]
            country = columns[2]
            regions = columns[3]
            city = columns[4]

        test = 0
        for i in range(len(regions)):
            if regions[test] == "":
                regions[test] = "None"
            if city[test] == "":
                city[test] = "None"
            test += 1

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("NO:", style="dim")
        table.add_column("IP", style="dim")
        table.add_column("Continent")
        table.add_column("Country", justify="left")
        table.add_column("Region")
        table.add_column("City")

        qq = 0
        for cont in country:
            if cont != "Private network":
                country_code = pc.country_name_to_country_alpha2(cont , cn_name_format="default")
                continent_name = pc.country_alpha2_to_continent_code(country_code)
                table.add_row(
                    str(qq + 1),"[cyan]"+ip[qq]+"[/cyan]","[yellow]" + continent_name + "[/yellow]", cont + " ("+ country_code +")" , regions[qq], city[qq]
                )
                qq += 1
            else:
                table.add_row(
                    str(qq + 1),"[red]"+ip[qq]+"[/red]", "[green]"+continent_name+"[/green]", cont, regions[qq], city[qq]
                )
        print(table)
        print("[+] Files have been stored at: {}/Trust-Rep".format(os.getcwd()))
    except Exception as e:
        print(f"Error occurred while processing CSV file: {e}")


def main():
    Banner()
    file, vt = arguments()
    directorys()
    asyncio.get_event_loop().run_until_complete(spam())
    if vt == True:
        screenshots(True)
    else:
        screenshots()
    asyncio.get_event_loop().run_until_complete(whois())
    conti()
    print("[+] Done")
    print("[+] Happy Hacking")

if __name__ == "__main__":
    main()

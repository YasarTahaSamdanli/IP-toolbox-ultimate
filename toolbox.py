#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import threading
import os
import time
from datetime import datetime
import psutil  # Sistem kaynakları için

class HackerToolboxUltimate:
    def __init__(self, root):
        self.root = root
        self.root.title("Toolbox ULTIMATE")
        self.root.minsize(1000, 800)
        
        # Logo ekleme
        try:
            self.logo = tk.PhotoImage(file='logo.png')
            self.root.iconphoto(False, self.logo)
        except Exception as e:
            print(f"Logo yüklenirken hata oluştu: {e}")
            # Logo yüklenemezse devam et
            
        self.is_running = False
        self.current_process = None
        
        # Variables
        self.stealth_var = tk.BooleanVar()
        # ... (diğer kodlar aynı şekilde devam eder)
        
        # Variables
        self.stealth_var = tk.BooleanVar()
        self.service_var = tk.BooleanVar()
        self.os_var = tk.BooleanVar()
        self.ping_var = tk.BooleanVar()
        self.fast_var = tk.BooleanVar()
        self.vuln_var = tk.BooleanVar()
        self.mac_var = tk.StringVar(value="Yok")
        self.scan_type = tk.StringVar(value="-sS")
        self.speed_var = tk.StringVar(value="3")
        
        self.setup_ui()
        self.setup_menubar()
        self.setup_status_bar()
        
    def setup_menubar(self):
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Sonuçları Kaydet", command=self.export_results)
        file_menu.add_command(label="Çıkış", command=self.root.quit)
        menubar.add_cascade(label="Dosya", menu=file_menu)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Ping", command=self.run_ping)
        tools_menu.add_command(label="DNS Lookup", command=self.run_dns_lookup)
        tools_menu.add_command(label="Traceroute", command=self.run_traceroute)
        tools_menu.add_command(label="Port Tarama", command=self.run_port_scan)
        menubar.add_cascade(label="Araçlar", menu=tools_menu)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Görünüm(eklencek)", menu=view_menu)
        
        self.root.config(menu=menubar)
    
    def setup_status_bar(self):
        # Status Frame
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Progress Bar
        self.progress = ttk.Progressbar(status_frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Cancel Button
        self.cancel_btn = ttk.Button(status_frame, text="İptal", command=self.cancel_operation, state=tk.DISABLED)
        self.cancel_btn.pack(side=tk.RIGHT, padx=5)
        
        # Status Labels
        self.status_var = tk.StringVar()
        self.status_var.set("Hazır")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, width=30)
        status_label.pack(side=tk.LEFT, padx=5)
        
        # System Monitor Frame
        monitor_frame = ttk.Frame(self.root)
        monitor_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # CPU Usage
        self.cpu_var = tk.StringVar()
        self.cpu_var.set("CPU: 0%")
        ttk.Label(monitor_frame, textvariable=self.cpu_var, width=10).pack(side=tk.LEFT)
        
        # Memory Usage
        self.mem_var = tk.StringVar()
        self.mem_var.set("RAM: 0%")
        ttk.Label(monitor_frame, textvariable=self.mem_var, width=10).pack(side=tk.LEFT)
        
        # Network Usage
        self.net_var = tk.StringVar()
        self.net_var.set("NET: 0K/0K")
        ttk.Label(monitor_frame, textvariable=self.net_var, width=15).pack(side=tk.LEFT)
        
        # Timer
        self.time_var = tk.StringVar()
        self.time_var.set("00:00:00")
        ttk.Label(monitor_frame, textvariable=self.time_var, width=10).pack(side=tk.RIGHT)
        
        # Start monitoring
        self.update_system_stats()
    
    def update_system_stats(self):
        # CPU Usage
        cpu_percent = psutil.cpu_percent()
        self.cpu_var.set(f"CPU: {cpu_percent}%")
        
        # Memory Usage
        mem = psutil.virtual_memory()
        self.mem_var.set(f"RAM: {mem.percent}%")
        
        # Network Usage
        net = psutil.net_io_counters()
        self.net_var.set(f"NET: {net.bytes_sent/1024:.1f}K/{net.bytes_recv/1024:.1f}K")
        
        # Update every 2 seconds
        if self.is_running:
            self.root.after(2000, self.update_system_stats)
    
    def setup_ui(self):
        # Top frame
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        ttk.Label(top_frame, text="Hedef:").pack(side=tk.LEFT)
        self.entry = ttk.Entry(top_frame, width=40)
        self.entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(top_frame, text="Nmap Tara", command=self.start_nmap_scan).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="WHOIS", command=self.start_whois_lookup).pack(side=tk.LEFT)
        
        # Main content frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left panel - Options
        left_panel = ttk.Frame(main_frame, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        
        # Scan options
        options_frame = ttk.LabelFrame(left_panel, text="Tarama Seçenekleri", padding="10")
        options_frame.pack(fill=tk.X, pady=5)
        
        # Port selection
        ttk.Label(options_frame, text="Portlar (örn: 80,443 veya 1-1000):").pack(anchor='w')
        self.port_entry = ttk.Entry(options_frame)
        self.port_entry.pack(fill=tk.X, pady=2)
        
        # Scan type
        ttk.Label(options_frame, text="Temel Tarama Türü:").pack(anchor='w')
        scan_types = [("-sS", "SYN Tarama"), ("-sT", "Connect Tarama"), 
                     ("-sU", "UDP Tarama"), ("-sN", "NULL Tarama")]
        for value, text in scan_types:
            ttk.Radiobutton(options_frame, text=text, variable=self.scan_type, 
                          value=value).pack(anchor='w')
        
        # Additional options
        ttk.Checkbutton(options_frame, text="Servis Versiyonu (-sV)", 
                       variable=self.service_var).pack(anchor='w')
        ttk.Checkbutton(options_frame, text="OS Tanıma (-O)", 
                       variable=self.os_var).pack(anchor='w')
        ttk.Checkbutton(options_frame, text="Ping Atmadan (-Pn)", 
                       variable=self.ping_var).pack(anchor='w')
        ttk.Checkbutton(options_frame, text="Hızlı Tarama (-F)", 
                       variable=self.fast_var).pack(anchor='w')
        ttk.Checkbutton(options_frame, text="Vulnerability Scan (--script vuln)", 
                       variable=self.vuln_var).pack(anchor='w')
        
        # Timing template
        ttk.Label(options_frame, text="Tarama Hızı:").pack(anchor='w')
        ttk.OptionMenu(options_frame, self.speed_var, "3", "0", "1", "2", "3", "4", "5").pack(anchor='w')
        
        # Advanced options
        adv_frame = ttk.LabelFrame(left_panel, text="Gelişmiş Seçenekler", padding="10")
        adv_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(adv_frame, text="Decoy IP'ler (-D):").pack(anchor='w')
        self.decoy_entry = ttk.Entry(adv_frame)
        self.decoy_entry.pack(fill=tk.X, pady=2)
        ttk.Label(adv_frame, text="Örnek: RND:5 veya 1.1.1.1,2.2.2.2", font=('Helvetica', 8)).pack(anchor='w')
        
        ttk.Label(adv_frame, text="MAC Spoofing:").pack(anchor='w')
        mac_options = ["Yok", "Apple", "Cisco", "Realtek", "Microsoft", "Rastgele"]
        self.mac_menu = ttk.OptionMenu(adv_frame, self.mac_var, *mac_options)
        self.mac_menu.pack(fill=tk.X, pady=2)
        
        # Quick Tools Frame
        tools_frame = ttk.LabelFrame(left_panel, text="Hızlı Araçlar", padding="10")
        tools_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(tools_frame, text="Ping", command=self.run_ping).pack(fill=tk.X, pady=2)
        ttk.Button(tools_frame, text="DNS Lookup", command=self.run_dns_lookup).pack(fill=tk.X, pady=2)
        ttk.Button(tools_frame, text="Traceroute", command=self.run_traceroute).pack(fill=tk.X, pady=2)
        
        # Right panel - Output
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Output tabs
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Nmap output tab
        self.nmap_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.nmap_frame, text="Nmap Çıktısı")
        
        self.output_text = tk.Text(self.nmap_frame, wrap=tk.WORD, font=('Courier', 10))
        scrollbar = ttk.Scrollbar(self.nmap_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Tools output tab
        self.tools_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tools_frame, text="Araç Çıktısı")
        
        self.tools_output = tk.Text(self.tools_frame, wrap=tk.WORD, font=('Courier', 10))
        tools_scroll = ttk.Scrollbar(self.tools_frame, orient=tk.VERTICAL, command=self.tools_output.yview)
        self.tools_output.configure(yscrollcommand=tools_scroll.set)
        
        tools_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tools_output.pack(fill=tk.BOTH, expand=True)
        
        # Log tab
        self.log_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.log_frame, text="Sistem Logları")
        
        self.log_text = tk.Text(self.log_frame, wrap=tk.WORD, font=('Courier', 10))
        log_scroll = ttk.Scrollbar(self.log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)
        
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def start_operation(self, tool_name):
        self.is_running = True
        self.start_time = datetime.now()
        self.cancel_btn.config(state=tk.NORMAL)
        self.status_var.set(f"Çalışıyor | Araç: {tool_name}")
        self.progress['value'] = 0
        self.progress['maximum'] = 100
        self.update_timer()
        self.update_system_stats()
        self.add_log(f"{tool_name} işlemi başlatıldı - {self.start_time.strftime('%H:%M:%S')}")
    
    def end_operation(self, tool_name):
        self.is_running = False
        self.cancel_btn.config(state=tk.DISABLED)
        self.progress['value'] = 100
        elapsed = datetime.now() - self.start_time
        self.status_var.set(f"Hazır | Son işlem: {tool_name} ({str(elapsed).split('.')[0]})")
        self.add_log(f"{tool_name} işlemi tamamlandı - Süre: {str(elapsed).split('.')[0]}")
        self.current_process = None
    
    def cancel_operation(self):
        if self.current_process:
            self.current_process.terminate()
        self.is_running = False
        self.status_var.set("İşlem iptal edildi")
        self.add_log("İşlem kullanıcı tarafından iptal edildi")
        self.progress['value'] = 0
        self.cancel_btn.config(state=tk.DISABLED)
    
    def update_timer(self):
        if self.is_running:
            elapsed = datetime.now() - self.start_time
            self.time_var.set(str(elapsed).split('.')[0])
            self.progress['value'] = elapsed.seconds % 100
            self.root.after(1000, self.update_timer)
    
    def add_log(self, message):
        timestamp = datetime.now().strftime('[%H:%M:%S]')
        self.log_text.insert(tk.END, f"{timestamp} {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def export_results(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Sonuçları Kaydet"
        )
        if filename:
            current_tab = self.notebook.tab(self.notebook.select(), "text")
            content = ""
            if current_tab == "Nmap Çıktısı":
                content = self.output_text.get(1.0, tk.END)
            elif current_tab == "Araç Çıktısı":
                content = self.tools_output.get(1.0, tk.END)
            else:
                content = self.log_text.get(1.0, tk.END)
            
            with open(filename, "w") as f:
                f.write(content)
            self.add_log(f"Sonuçlar '{filename}' dosyasına kaydedildi")
    
    def run_port_scan(self):
        target = self.entry.get().strip()
        if not target:
            messagebox.showerror("Hata", "Lütfen bir hedef girin!")
            return
        
        port_input = self.port_entry.get().strip()
        if not port_input:
            messagebox.showerror("Hata", "Lütfen port aralığı girin!")
            return
        
        self.notebook.select(self.tools_frame)
        self.clear_tools_output()
        threading.Thread(target=self._run_port_scan, args=(target, port_input), daemon=True).start()
    
    def _run_port_scan(self, target, ports):
        self.start_operation("Port Tarama")
        
        command = ["nmap", "-p", ports, target]
        self.append_tools_output(f"Port Tarama Başlıyor...\nKomut: {' '.join(command)}\n\n")
        
        try:
            self.current_process = subprocess.Popen(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True, 
                universal_newlines=True
            )
            
            while True:
                output = self.current_process.stdout.readline()
                if output == '' and self.current_process.poll() is not None:
                    break
                if output:
                    self.append_tools_output(output)
            
            stderr = self.current_process.stderr.read()
            if stderr:
                self.append_tools_output(f"\nHatalar:\n{stderr}")
                
        except Exception as e:
            self.append_tools_output(f"Beklenmeyen hata: {str(e)}")
        finally:
            self.end_operation("Port Tarama")
    
    def start_nmap_scan(self):
        target = self.entry.get().strip()
        if not target:
            messagebox.showerror("Hata", "Lütfen bir hedef girin!")
            return
        
        self.notebook.select(self.nmap_frame)
        self.clear_output()
        threading.Thread(target=self.run_nmap_scan_thread, args=(target,), daemon=True).start()
    
    def run_nmap_scan_thread(self, target):
        self.start_operation("Nmap Tarama")
        
        options = [self.scan_type.get()]
        options.append(f"-T{self.speed_var.get()}")
        
        port_input = self.port_entry.get().strip()
        if port_input:
            options.append(f"-p {port_input}")
        
        if self.service_var.get():
            options.append("-sV")
        if self.os_var.get():
            options.append("-O")
        if self.ping_var.get():
            options.append("-Pn")
        if self.fast_var.get():
            options.append("-F")
        if self.vuln_var.get():
            options.append("--script=vuln")
        
        decoy_input = self.decoy_entry.get().strip().replace(" ", "")
        if decoy_input:
            options.append(f"-D{decoy_input}")
        
        mac_choice = self.mac_var.get()
        if mac_choice != "Yok":
            options.append(f"--spoof-mac {mac_choice}")
        
        command = ["nmap"] + options + [target]
        self.append_output(f"Nmap Tarama Başlıyor...\nKomut: {' '.join(command)}\n\n")
        
        try:
            if os.geteuid() != 0 and ("-sS" in options or "-O" in options):
                self.append_output("Uyarı: Bazı tarama seçenekleri root yetkisi gerektirir!\n")
            
            self.current_process = subprocess.Popen(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True, 
                universal_newlines=True
            )
            
            while True:
                output = self.current_process.stdout.readline()
                if output == '' and self.current_process.poll() is not None:
                    break
                if output:
                    self.append_output(output)
            
            stderr = self.current_process.stderr.read()
            if stderr:
                self.append_output(f"\nHatalar:\n{stderr}")
                
        except FileNotFoundError:
            self.append_output("Hata: nmap komutu bulunamadı. Lütfen nmap'in kurulu olduğundan emin olun.")
        except Exception as e:
            self.append_output(f"Beklenmeyen hata: {str(e)}")
        finally:
            self.end_operation("Nmap Tarama")
    
    def start_whois_lookup(self):
        target = self.entry.get().strip()
        if not target:
            messagebox.showerror("Hata", "Lütfen bir hedef girin!")
            return
        
        self.notebook.select(self.nmap_frame)
        self.clear_output()
        threading.Thread(target=self.run_whois_lookup_thread, args=(target,), daemon=True).start()
    
    def run_whois_lookup_thread(self, target):
        self.start_operation("WHOIS Sorgu")
        
        command = ["whois", target]
        self.append_output(f"WHOIS Sorgusu Başlıyor...\nKomut: {' '.join(command)}\n\n")
        
        try:
            self.current_process = subprocess.Popen(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True, 
                universal_newlines=True
            )
            
            while True:
                output = self.current_process.stdout.readline()
                if output == '' and self.current_process.poll() is not None:
                    break
                if output:
                    self.append_output(output)
            
            stderr = self.current_process.stderr.read()
            if stderr:
                self.append_output(f"\nHatalar:\n{stderr}")
                
        except FileNotFoundError:
            self.append_output("Hata: whois komutu bulunamadı.")
        except Exception as e:
            self.append_output(f"Beklenmeyen hata: {str(e)}")
        finally:
            self.end_operation("WHOIS Sorgu")
    
    def run_ping(self):
        target = self.entry.get().strip()
        if not target:
            messagebox.showerror("Hata", "Lütfen bir hedef girin!")
            return
        
        self.notebook.select(self.tools_frame)
        self.clear_tools_output()
        threading.Thread(target=self._run_ping, args=(target,), daemon=True).start()
    
    def _run_ping(self, target):
        self.start_operation("Ping Testi")
        
        command = ["ping", "-c", "4", target] if os.name != 'nt' else ["ping", "-n", "4", target]
        self.append_tools_output(f"Ping Testi Başlıyor...\nKomut: {' '.join(command)}\n\n")
        
        try:
            self.current_process = subprocess.Popen(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True, 
                universal_newlines=True
            )
            
            while True:
                output = self.current_process.stdout.readline()
                if output == '' and self.current_process.poll() is not None:
                    break
                if output:
                    self.append_tools_output(output)
            
            stderr = self.current_process.stderr.read()
            if stderr:
                self.append_tools_output(f"\nHatalar:\n{stderr}")
                
        except Exception as e:
            self.append_tools_output(f"Beklenmeyen hata: {str(e)}")
        finally:
            self.end_operation("Ping Testi")
    
    def run_dns_lookup(self):
        target = self.entry.get().strip()
        if not target:
            messagebox.showerror("Hata", "Lütfen bir hedef girin!")
            return
        
        self.notebook.select(self.tools_frame)
        self.clear_tools_output()
        threading.Thread(target=self._run_dns_lookup, args=(target,), daemon=True).start()
    
    def _run_dns_lookup(self, target):
        self.start_operation("DNS Sorgu")
        
        command = ["nslookup", target] if os.name != 'nt' else ["nslookup", target]
        self.append_tools_output(f"DNS Sorgusu Başlıyor...\nKomut: {' '.join(command)}\n\n")
        
        try:
            self.current_process = subprocess.Popen(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True, 
                universal_newlines=True
            )
            
            while True:
                output = self.current_process.stdout.readline()
                if output == '' and self.current_process.poll() is not None:
                    break
                if output:
                    self.append_tools_output(output)
            
            stderr = self.current_process.stderr.read()
            if stderr:
                self.append_tools_output(f"\nHatalar:\n{stderr}")
                
        except Exception as e:
            self.append_tools_output(f"Beklenmeyen hata: {str(e)}")
        finally:
            self.end_operation("DNS Sorgu")
    
    def run_traceroute(self):
        target = self.entry.get().strip()
        if not target:
            messagebox.showerror("Hata", "Lütfen bir hedef girin!")
            return
        
        self.notebook.select(self.tools_frame)
        self.clear_tools_output()
        threading.Thread(target=self._run_traceroute, args=(target,), daemon=True).start()
    
    def _run_traceroute(self, target):
        self.start_operation("Traceroute")
        
        command = ["traceroute", target] if os.name != 'nt' else ["tracert", target]
        self.append_tools_output(f"Traceroute Başlıyor...\nKomut: {' '.join(command)}\n\n")
        
        try:
            self.current_process = subprocess.Popen(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True, 
                universal_newlines=True
            )
            
            while True:
                output = self.current_process.stdout.readline()
                if output == '' and self.current_process.poll() is not None:
                    break
                if output:
                    self.append_tools_output(output)
            
            stderr = self.current_process.stderr.read()
            if stderr:
                self.append_tools_output(f"\nHatalar:\n{stderr}")
                
        except Exception as e:
            self.append_tools_output(f"Beklenmeyen hata: {str(e)}")
        finally:
            self.end_operation("Traceroute")
    
    def clear_output(self):
        self.output_text.delete(1.0, tk.END)
    
    def clear_tools_output(self):
        self.tools_output.delete(1.0, tk.END)
    
    def append_output(self, text):
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        self.root.update_idletasks()
    
    def append_tools_output(self, text):
        self.tools_output.insert(tk.END, text)
        self.tools_output.see(tk.END)
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = HackerToolboxUltimate(root)
    root.mainloop()

import customtkinter as ctk
from config import load
import threading

settings_window_open = False
_settings_root = None

def open_settings():
    global settings_window_open, _settings_root
    
    if settings_window_open:
        print("[Settings] Window already open")
        try:
            if _settings_root is not None:
                _settings_root.lift()
                _settings_root.focus_force()
        except:
            pass
        return
    
    settings_window_open = True
    
    try:
        config = load()
        
        # Create standalone window (NOT Toplevel)
        root = ctk.CTk()
        root.title("⚡ BatteryGuard Settings")
        root.geometry("450x550")
        root.resizable(False, False)
        
        # Store reference
        _settings_root = root
        
        # CRITICAL: Force focus and grab
        root.focus_force()
        root.grab_set()
        root.lift()
        root.attributes('-topmost', True)
        root.after(100, lambda: root.attributes('-topmost', False))
        
        # Create the UI
        main_frame = ctk.CTkFrame(root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # ---------------- HEADER ----------------
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            header_frame,
            text="⚡ BatteryGuard",
            font=("Segoe UI", 28, "bold"),
            text_color=("#1a8a4a", "#2ecc71")
        )
        title.pack()
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Power Management Settings",
            font=("Segoe UI", 13),
            text_color=("gray60", "gray60")
        )
        subtitle.pack()

        # ---------------- SEPARATOR ----------------
        ctk.CTkFrame(main_frame, height=2, fg_color=("gray30", "gray30")).pack(fill="x", pady=(0, 20))

        # ---------------- ALERT LEVEL ----------------
        alert_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        alert_frame.pack(fill="x", pady=(0, 15))
        
        alert_label = ctk.CTkLabel(
            alert_frame,
            text="🔋 Battery Alert Level",
            font=("Segoe UI", 15, "bold")
        )
        alert_label.pack(anchor="w", pady=(0, 5))
        
        alert_desc = ctk.CTkLabel(
            alert_frame,
            text="Trigger notification when battery reaches this level",
            font=("Segoe UI", 11),
            text_color=("gray60", "gray60")
        )
        alert_desc.pack(anchor="w", pady=(0, 8))
        
        alert_input_frame = ctk.CTkFrame(alert_frame, fg_color="transparent")
        alert_input_frame.pack(fill="x")
        
        alert_entry = ctk.CTkEntry(
            alert_input_frame,
            height=45,
            font=("Segoe UI", 16),
            placeholder_text="Enter percentage",
            width=140,
            border_width=2,
            corner_radius=8
        )
        alert_entry.pack(side="left", padx=(0, 10))
        alert_entry.insert(0, str(config.get("alert_level")))
        
        # CRITICAL: Set focus to alert_entry after window is ready
        root.after(100, lambda: alert_entry.focus_set())
        root.after(100, lambda: alert_entry.select_range(0, 'end'))
        
        alert_percent_label = ctk.CTkLabel(
            alert_input_frame,
            text="%",
            font=("Segoe UI", 18, "bold"),
            text_color=("gray70", "gray70")
        )
        alert_percent_label.pack(side="left")
        
        # Preset buttons
        preset_frame = ctk.CTkFrame(alert_frame, fg_color="transparent")
        preset_frame.pack(anchor="w", pady=(10, 0))
        
        for preset in [20, 40, 60, 80]:
            btn = ctk.CTkButton(
                preset_frame,
                text=f"{preset}%",
                width=50,
                height=32,
                font=("Segoe UI", 12),
                fg_color=("gray50", "gray30"),
                hover_color=("gray60", "gray40"),
                corner_radius=6,
                command=lambda p=preset: alert_entry.delete(0, "end") or alert_entry.insert(0, str(p))
            )
            btn.pack(side="left", padx=(0, 8))

        # ---------------- INTERVAL ----------------
        interval_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        interval_frame.pack(fill="x", pady=(0, 20))
        
        interval_label = ctk.CTkLabel(
            interval_frame,
            text="⏱️ Check Interval",
            font=("Segoe UI", 15, "bold")
        )
        interval_label.pack(anchor="w", pady=(0, 5))
        
        interval_desc = ctk.CTkLabel(
            interval_frame,
            text="How often to check battery status (in seconds)",
            font=("Segoe UI", 11),
            text_color=("gray60", "gray60")
        )
        interval_desc.pack(anchor="w", pady=(0, 8))
        
        interval_input_frame = ctk.CTkFrame(interval_frame, fg_color="transparent")
        interval_input_frame.pack(fill="x")
        
        interval_entry = ctk.CTkEntry(
            interval_input_frame,
            height=45,
            font=("Segoe UI", 16),
            placeholder_text="Enter seconds",
            width=140,
            border_width=2,
            corner_radius=8
        )
        interval_entry.pack(side="left", padx=(0, 10))
        interval_entry.insert(0, str(config.get("check_interval")))
        
        interval_sec_label = ctk.CTkLabel(
            interval_input_frame,
            text="seconds",
            font=("Segoe UI", 18, "bold"),
            text_color=("gray70", "gray70")
        )
        interval_sec_label.pack(side="left")
        
        # Quick interval presets
        interval_preset_frame = ctk.CTkFrame(interval_frame, fg_color="transparent")
        interval_preset_frame.pack(anchor="w", pady=(10, 0))
        
        for preset in [2, 5, 10, 30, 60, 120, 300, 600]:  # Added 600 seconds
            btn = ctk.CTkButton(
                interval_preset_frame,
                text=f"{preset}s",
                width=50,
                height=32,
                font=("Segoe UI", 12),
                fg_color=("gray50", "gray30"),
                hover_color=("gray60", "gray40"),
                corner_radius=6,
                command=lambda p=preset: interval_entry.delete(0, "end") or interval_entry.insert(0, str(p))
            )
            btn.pack(side="left", padx=(0, 8))

        # ---------------- CURRENT STATUS ----------------
        status_frame = ctk.CTkFrame(main_frame, fg_color=("gray90", "gray15"), corner_radius=12)
        status_frame.pack(fill="x", pady=(0, 20))
        
        status_label = ctk.CTkLabel(
            status_frame,
            text="💡 Current Settings",
            font=("Segoe UI", 13, "bold")
        )
        status_label.pack(anchor="w", padx=15, pady=(12, 5))
        
        status_text = ctk.CTkLabel(
            status_frame,
            text=f"Alert at {config.get('alert_level')}% • Check every {config.get('check_interval')}s",
            font=("Segoe UI", 13),
            text_color=("gray60", "gray60")
        )
        status_text.pack(anchor="w", padx=15, pady=(0, 12))

        # ---------------- BUTTONS ----------------
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, 10))
        
        def save():
            try:
                alert_value = int(alert_entry.get())
                interval_value = int(interval_entry.get())
                
                if not (0 <= alert_value <= 100):
                    print("[Settings] Alert level must be between 0-100")
                    save_btn.configure(fg_color=("#e74c3c", "#c0392b"))
                    root.after(500, lambda: save_btn.configure(fg_color=("#2ecc71", "#27ae60")))
                    return
                
                if interval_value < 1:
                    print("[Settings] Interval must be at least 1 second")
                    save_btn.configure(fg_color=("#e74c3c", "#c0392b"))
                    root.after(500, lambda: save_btn.configure(fg_color=("#2ecc71", "#27ae60")))
                    return

                config.set("alert_level", alert_value)
                config.set("check_interval", interval_value)
                
                status_text.configure(text=f"Alert at {alert_value}% • Check every {interval_value}s")
                
                print("[Settings] ✅ Saved successfully")
                
                save_btn.configure(fg_color=("#2ecc71", "#27ae60"))
                save_btn.configure(text="✅ Saved!")
                root.after(500, lambda: save_btn.configure(text="💾 Save & Close"))
                root.after(1500, lambda: close_window())
                
            except ValueError:
                print("[Settings] ❌ Please enter valid numbers")
                save_btn.configure(fg_color=("#e74c3c", "#c0392b"))
                root.after(500, lambda: save_btn.configure(fg_color=("#2ecc71", "#27ae60")))
        
        def close_window():
            global settings_window_open, _settings_root
            settings_window_open = False
            _settings_root = None
            root.destroy()
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Save & Close",
            height=55,
            font=("Segoe UI", 16, "bold"),
            fg_color=("#2ecc71", "#27ae60"),
            hover_color=("#27ae60", "#1e8449"),
            corner_radius=10,
            border_width=0,
            command=save
        )
        save_btn.pack(fill="x", pady=(0, 12))
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            height=40,
            font=("Segoe UI", 14),
            fg_color=("gray60", "gray40"),
            hover_color=("gray50", "gray30"),
            corner_radius=8,
            command=close_window
        )
        cancel_btn.pack(fill="x")

        footer = ctk.CTkLabel(
            main_frame,
            text="Changes will take effect immediately ⚡",
            font=("Segoe UI", 11),
            text_color=("gray50", "gray50")
        )
        footer.pack(pady=(10, 0))

        root.bind('<Return>', lambda e: save())
        root.bind('<Escape>', lambda e: close_window())
        root.protocol("WM_DELETE_WINDOW", close_window)
        
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        root.mainloop()
        
    except Exception as e:
        print(f"[Settings] Error: {e}")
        import traceback
        traceback.print_exc()
        settings_window_open = False
import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, simpledialog, messagebox
from PIL import Image, ImageTk  
from collections import deque
from tkinter import scrolledtext # scrolledtext似乎并是tkinter主模块的一部分，这行是有用的

class NewCanvasDialog(tk.Toplevel):
    """新建画布尺寸和缩放设置对话框"""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("新建画布")
        self.result = None
        self.parent = parent
        vcmd = (self.register(self.validate_number), '%P')
        
        # 尺寸输入
        ttk.Label(self, text="宽度（像素）:").grid(row=0, column=0, padx=5, pady=5)
        self.width_entry = ttk.Entry(self, validate='key', validatecommand=vcmd)
        self.width_entry.grid(row=0, column=1, padx=5, pady=5)
        self.width_entry.insert(0, "32")
        
        ttk.Label(self, text="高度（像素）:").grid(row=1, column=0, padx=5, pady=5)
        self.height_entry = ttk.Entry(self, validate='key', validatecommand=vcmd)
        self.height_entry.grid(row=1, column=1, padx=5, pady=5)
        self.height_entry.insert(0, "32")
        
        # 缩放比例输入
        ttk.Label(self, text="缩放比例:").grid(row=2, column=0, padx=5, pady=5)
        self.zoom_entry = ttk.Entry(self, validate='key', validatecommand=vcmd)
        self.zoom_entry.grid(row=2, column=1, padx=5, pady=5)
        self.zoom_entry.insert(0, "20")
        self.zoom_entry.bind("<KeyRelease>", self.update_zoom_hint)
        
        self.hint_label = ttk.Label(self, text="画面上的一个像素将以屏幕上的 20x20 像素显示")
        self.hint_label.grid(row=3, columnspan=2, pady=5)
        
        # 按钮区域
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=4, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="确定", command=self.on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=self.destroy).pack(side=tk.LEFT)
        
        self.center_window()
        self.grab_set()

    def validate_number(self, value):
        return value.isdigit() or value == ""
    
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = self.parent.winfo_x() + (self.parent.winfo_width() - width) // 2
        y = self.parent.winfo_y() + (self.parent.winfo_height() - height) // 2
        self.geometry(f"+{x}+{y}")
    
    def update_zoom_hint(self, event=None):
        zoom = self.zoom_entry.get()
        if zoom.isdigit() and 1 <= int(zoom) <= 50:
            self.hint_label.config(text=f"画面上的一个像素将以屏幕上的 {zoom}x{zoom} 像素显示")
        else:
            self.hint_label.config(text="请输入有效缩放比例（1-50）")
    
    def on_ok(self):
        try:
            width = int(self.width_entry.get() or 32)
            height = int(self.height_entry.get() or 32)
            zoom = int(self.zoom_entry.get() or 20)
            if not (1 <= width <= 2048 and 1 <= height <= 2048):
                messagebox.showerror("错误", "画布尺寸范围：1-2048像素", parent=self)
                return
            if not (1 <= zoom <= 50):
                messagebox.showerror("错误", "缩放比例范围：1-50", parent=self)
                return
            self.result = (width, height, zoom)
            self.destroy()
        except ValueError:
            messagebox.showerror("错误", "请输入有效数字", parent=self)



class ZoomDialog(tk.Toplevel):
    '''打开已有像素画时设置缩放比例'''
    def __init__(self, parent):
        super().__init__(parent)
        self.title("设置缩放比例")
        self.result = None
        self.parent = parent
        
        vcmd = (self.register(self.validate_number), '%P')
        
        # 缩放比例输入框
        ttk.Label(self, text="缩放比例:").grid(row=0, column=0, padx=5, pady=5)
        self.zoom_entry = ttk.Entry(self, validate='key', validatecommand=vcmd)
        self.zoom_entry.grid(row=0, column=1, padx=5, pady=5)
        self.zoom_entry.insert(0, "20")
        self.zoom_entry.bind("<KeyRelease>", self.update_zoom_hint)
        
        # 动态提示语
        self.hint_label = ttk.Label(self, text="画面上的一个像素将以屏幕上的 20x20 像素显示")
        self.hint_label.grid(row=1, columnspan=2, pady=5)
        
        # 按钮区域
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=2, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="确定", command=self.on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=self.destroy).pack(side=tk.LEFT)
        
        self.center_window()
        self.grab_set()

    def validate_number(self, value):
        return value.isdigit() or value == ""

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = self.parent.winfo_x() + (self.parent.winfo_width() - width) // 2
        y = self.parent.winfo_y() + (self.parent.winfo_height() - height) // 2
        self.geometry(f"+{x}+{y}")

    def update_zoom_hint(self, event=None):
        zoom = self.zoom_entry.get()
        if zoom.isdigit() and 1 <= int(zoom) <= 50:
            self.hint_label.config(text=f"画面上的一个像素将以屏幕上的 {zoom}x{zoom} 像素显示")
        else:
            self.hint_label.config(text="请输入有效缩放比例（1-50）")

    def on_ok(self):
        try:
            zoom = int(self.zoom_entry.get() or 20)
            if 1 <= zoom <= 50:
                self.result = zoom
                self.destroy()
            else:
                messagebox.showerror("错误", "缩放比例范围：1-50", parent=self)
        except ValueError:
            messagebox.showerror("错误", "请输入有效数字", parent=self)



class EnhancedPixelEditor(tk.Tk):
    '''像素编辑'''
    def __init__(self, image=None, zoom=20):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.zoom = zoom
        self.last_color = (255, 255, 255, 255)
        self.recent_colors = deque(maxlen=8)
        self.drawing = False
        self.history = []
        self.current_batch = None
        self.preset_colors = [
            "#FF0000", "#00FF00", "#0000FF",
            "#FFFF00", "#FF00FF", "#00FFFF",
            "#FFFFFF", "#000000"
        ]
        self.transparent_mode = False
        
        self.image = image.convert("RGBA") if image else Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        self.pixels = self.image.load()
        self.width, self.height = self.image.size
        
        self.last_x = None  #检查鼠标位置，应对快速拖动情况
        self.last_y = None
        
        self.brush_size = 1  # 默认笔刷大小（1x1）
        self.brush_sizes = [1, 3, 5, 9]  # 可选笔刷大小

        self.title("Pixetto")
        self.init_ui()
        self.bind_events()

        self.paste_preview = None  # 粘贴预览对象
        self.paste_image = None    # 待粘贴的图片数据
        self.paste_position = (0, 0)
        self.bind_events()
    
    def init_ui(self):
        self.canvas = tk.Canvas(
            self,
            width=self.width * self.zoom,
            height=self.height * self.zoom,
            cursor="crosshair"
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        control_frame = ttk.Frame(self)
        control_frame.pack(side=tk.RIGHT, padx=10, fill=tk.Y)
          
        ttk.Button(control_frame, text="帮助文档", command=self.show_help).pack(pady=5)
        ttk.Button(control_frame, text="保存图片", command=self.save_image).pack(pady=5)
        ttk.Button(control_frame, text="导入颜色", command=self.import_colors).pack(pady=5)
        ttk.Button(control_frame, text="导出颜色", command=self.export_colors).pack(pady=5)
        ttk.Button(control_frame, text="撤销 (Ctrl+Z)", command=self.undo).pack(pady=5)
        self.trans_btn = ttk.Button(control_frame, text="透明模式", command=self.toggle_transparent)
        self.trans_btn.pack(pady=5)
        
        color_panel = ttk.LabelFrame(control_frame, text="颜色面板")
        color_panel.pack(pady=10)
        
        self.preset_panel = ttk.Frame(color_panel)
        self.preset_panel.pack()
        self.init_preset_panel()
        
        self.recent_panel = ttk.Frame(color_panel)
        self.recent_panel.pack(pady=10)
        self.init_recent_panel()
        
        self.rectangles = [[None]*self.height for _ in range(self.width)]
        self.draw_pixels()

        brush_frame = ttk.LabelFrame(control_frame, text="笔刷大小")
        brush_frame.pack(pady=5)
        
        self.brush_var = tk.StringVar()
        self.brush_combobox = ttk.Combobox(
            brush_frame, 
            textvariable=self.brush_var,
            values=["1x1", "3x3", "5x5", "9x9"],
            state="readonly",
            width=8
        )
        self.brush_combobox.current(0)
        self.brush_combobox.pack(pady=5)
        self.brush_combobox.bind("<<ComboboxSelected>>", self.update_brush_size)
    
    def init_preset_panel(self):
        for widget in self.preset_panel.winfo_children():
            widget.destroy()
        
        for idx, color in enumerate(self.preset_colors):
            row, col = divmod(idx, 4)
            btn = tk.Button(
                self.preset_panel,
                bg=color,
                width=3,
                command=lambda c=color: self.set_color(c)
            )
            btn.bind("<Button-3>", lambda e, c=color: self.confirm_delete_color(e, c))
            btn.grid(row=row, column=col, padx=2, pady=2)
        
        total = len(self.preset_colors)
        row, col = divmod(total, 4)
        add_btn = tk.Button(
            self.preset_panel,
            text="+",
            width=3,
            command=self.add_custom_color
        )
        add_btn.grid(row=row, column=col, padx=2, pady=2)
    
    def confirm_delete_color(self, event, color):
        confirm_dlg = tk.Toplevel(self)
        confirm_dlg.wm_overrideredirect(True)
        confirm_dlg.geometry(f"+{event.x_root+10}+{event.y_root+10}")
        
        ttk.Label(confirm_dlg, text="删除该颜色？").pack(padx=10, pady=5)
        btn_frame = ttk.Frame(confirm_dlg)
        btn_frame.pack(pady=5)
        
        def delete_action():
            self.delete_preset_color(color)
            confirm_dlg.destroy()
            
        ttk.Button(btn_frame, text="删除", command=delete_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=confirm_dlg.destroy).pack(side=tk.LEFT)
        
        confirm_dlg.bind("<FocusOut>", lambda e: confirm_dlg.destroy())
        confirm_dlg.focus_force()
    
    def bind_events(self):
        """绑定事件时区分粘贴模式和绘制模式"""
        # 清空所有画布事件绑定
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<Button-3>")
        
        # 绑定基础事件
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Button-3>", self.pick_color)
        self.bind("<Control-z>", self.undo)
        self.bind("<Control-a>", self.start_paste_sticker)
    
    def export_colors(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt")]
        )
        if not path:
            return
        
        try:
            custom_colors = [
                c for c in self.preset_colors 
                if c not in self.preset_colors[:8]
            ]
            
            with open(path, "w") as f:
                for color in custom_colors:
                    f.write(color + "\n")
            messagebox.showinfo("导出成功", f"已导出{len(custom_colors)}个颜色到：\n{path}", parent=self)
        except Exception as e:
            messagebox.showerror("导出失败", f"错误详情：\n{str(e)}", parent=self)
    
    def import_colors(self):
        path = filedialog.askopenfilename(
            filetypes=[("文本文件", "*.txt")],
            parent=self  # 确保对话框层级正确
        )
        if not path:
            return
        try:
            with open(path, "r") as f:
                raw_colors = [line.strip() for line in f.readlines()]
            
            valid_colors = []
            for color in raw_colors:
                if self.is_valid_hex(color):
                    formatted_color = f"#{color.lstrip('#').upper()}"
                    if formatted_color not in self.preset_colors[:8]:
                        valid_colors.append(formatted_color)
                else:
                    messagebox.showwarning("无效颜色", f"跳过无效颜色值：{color}", parent=self)
            
            self.preset_colors = self.preset_colors[:8] + valid_colors
            self.init_preset_panel()
            messagebox.showinfo(
                "导入完成",
                f"成功导入 {len(valid_colors)} 个颜色\n已跳过 {len(raw_colors) - len(valid_colors)} 个无效项",
                parent=self
            )
        except Exception as e:
            messagebox.showerror("导入失败", f"错误详情：\n{str(e)}", parent=self)
    
    @staticmethod
    def is_valid_hex(color):
        color = color.lstrip("#")
        if len(color) != 6:
            return False
        try:
            int(color, 16)
            return True
        except ValueError:
            return False
    
    def init_recent_panel(self):
        self.recent_btns = []
        for i in range(8):
            btn = tk.Button(self.recent_panel, width=3, bg="#FFFFFF")
            btn.grid(row=i//4, column=i%4, padx=2, pady=2)
            # 新增右键事件绑定
            btn.bind("<Button-3>", 
                    lambda e, idx=i: self.on_recent_color_right_click(e, idx))
            self.recent_btns.append(btn)
    
    def draw_pixels(self):
        for x in range(self.width):
            for y in range(self.height):
                color = self.pixels[x, y]
                fill_color = self.rgba_to_hex(color) if color[3] != 0 else ""
                outline = "" if color[3] != 0 else "#CCCCCC"
                
                self.rectangles[x][y] = self.canvas.create_rectangle(
                    x * self.zoom,
                    y * self.zoom,
                    (x+1) * self.zoom,
                    (y+1) * self.zoom,
                    fill=fill_color,
                    outline=outline,
                    width=1
                )
    
    def update_pixel(self, x, y):
        color = self.pixels[x, y]
        fill_color = self.rgba_to_hex(color) if color[3] != 0 else ""
        outline = "" if color[3] != 0 else "#CCCCCC"
        self.canvas.itemconfig(self.rectangles[x][y], fill=fill_color, outline=outline)
    
    def on_click(self, event):
        self.drawing = True
        self.start_batch()
        x = event.x // self.zoom
        y = event.y // self.zoom
        self.last_x, self.last_y = x, y  # 记录起始点
        self.modify_pixel(x, y)
    
    def on_drag(self, event):
        if self.drawing:
            x1 = event.x // self.zoom
            y1 = event.y // self.zoom
            if self.last_x is not None and self.last_y is not None:
                for x, y in self.get_line_pixels(self.last_x, self.last_y, x1, y1):
                    if 0 <= x < self.width and 0 <= y < self.height:  # 边界检查
                        self.modify_pixel(x, y)
            else:
                self.modify_pixel(x1, y1)
            self.last_x, self.last_y = x1, y1
            
    def get_line_pixels(self, x0, y0, x1, y1):
        points = []
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            points.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy
        return points
    
    def on_release(self, event):
        self.drawing = False
        self.end_batch()
    
    def modify_pixel(self, x, y):
        """根据笔刷大小修改周围像素"""
        if 0 <= x < self.width and 0 <= y < self.height:
            radius = self.brush_size // 2
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    target_x = x + dx
                    target_y = y + dy
                    if 0 <= target_x < self.width and 0 <= target_y < self.height:
                        old_color = self.pixels[target_x, target_y]
                        new_color = (0, 0, 0, 0) if self.transparent_mode else self.last_color
                        
                        if new_color != old_color:
                            self.record_pixel_change(target_x, target_y, old_color)
                            self.pixels[target_x, target_y] = new_color
                            self.update_pixel(target_x, target_y)
            self.add_recent_color(new_color)

    def start_batch(self):
        """开始一个操作批次"""
        self.current_batch = {'pixels': {}}

    def record_pixel_change(self, x, y, old_color):
        """记录单个像素的旧颜色"""
        if (x, y) not in self.current_batch['pixels']:
            self.current_batch['pixels'][(x, y)] = old_color
    
    def start_batch(self):
        self.current_batch = {'pixels': {}
                              }
    
    def record_pixel_change(self, x, y, old_color):
        if self.current_batch is None:
            self.start_batch()
        if (x, y) not in self.current_batch['pixels']:
            self.current_batch['pixels'][(x, y)] = old_color
    
    def end_batch(self):
        if self.current_batch and self.current_batch['pixels']:
            self.history.append(self.current_batch)
            self.history = self.history[-100:]
        self.current_batch = None
    
    def undo(self, event=None):
        if self.history:
            last = self.history.pop()
            for (x, y), color in last['pixels'].items():
                self.pixels[x, y] = color
                self.update_pixel(x, y)
    
    def add_custom_color(self):
        try:
            color = colorchooser.askcolor(title="选择新颜色")
            if color and color[1]:
                hex_color = color[1].upper()
                if hex_color not in self.preset_colors:
                    self.preset_colors.append(hex_color)
                    self.init_preset_panel()
                else:
                    messagebox.showinfo("提示", "该颜色已存在！", parent=self)
            else:
                messagebox.showinfo("提示", "未选择颜色", parent=self)
        except Exception as e:
            messagebox.showerror("错误", f"颜色选择失败：{str(e)}", parent=self)
    
    def delete_preset_color(self, color):
        if color in self.preset_colors and len(self.preset_colors) > 8:
            self.preset_colors.remove(color)
            self.init_preset_panel()
    
    def set_color(self, hex_color):
        # 如果当前是透明模式，切换回正常模式
        if self.transparent_mode:
            self.toggle_transparent()
        self.last_color = self.hex_to_rgba(hex_color)
        self.add_recent_color(self.last_color)
        
    
    def add_recent_color(self, color):
        if color[3] == 0:
            return
        
        hex_color = self.rgba_to_hex(color)
        if hex_color in self.recent_colors:
            self.recent_colors.remove(hex_color)
        self.recent_colors.appendleft(hex_color)
        
        for i in range(min(8, len(self.recent_colors))):
            btn = self.recent_btns[i]
            btn.config(
                bg=self.recent_colors[i],
                command=lambda c=self.recent_colors[i]: self.set_color(c)
            )
        
        for i in range(min(8, len(self.recent_colors))):
            btn = self.recent_btns[i]
            btn.config(
                bg=self.recent_colors[i],
                command=lambda c=self.recent_colors[i]: self.set_color(c)
            )
    
    def toggle_transparent(self):
        self.transparent_mode = not self.transparent_mode
        self.trans_btn.config(text="正常模式" if self.transparent_mode else "透明模式")
        self.config(cursor="icon" if self.transparent_mode else "crosshair")
    
    def save_image(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG文件", "*.png"),
                ("JPEG文件", "*.jpg;*.jpeg"),
                ("BMP文件", "*.bmp"),
                ("所有文件", "*.*")
            ]
        )
        if not path:
            return
        
        scale = simpledialog.askinteger(
            "放大设置", "放大倍数（≥1）:", parent=self,
            minvalue=1, initialvalue=1
        )
        if scale is None:
            return
        if scale < 1:
            messagebox.showerror("错误", "放大倍数必须≥1", parent=self)
            return
        
        try:
            img = self.image
            if scale > 1:
                img = img.resize((img.width*scale, img.height*scale), Image.NEAREST)
            
            if path.lower().endswith(('.jpg', '.jpeg')):
                img.convert("RGB").save(path, quality=95)
            else:
                img.save(path)
            messagebox.showinfo("保存成功", f"图片已保存至：\n{path}", parent=self)
        except Exception as e:
            messagebox.showerror("保存失败", f"错误详情:\n{str(e)}", parent=self)
    
    def pick_color(self, event):
        x = event.x // self.zoom
        y = event.y // self.zoom
        if 0 <= x < self.width and 0 <= y < self.height:
            color = self.pixels[x, y]
            if color[3] != 0:
                # 调用 set_color 前确保透明模式已关闭
                if self.transparent_mode:
                    self.toggle_transparent()
                self.set_color(self.rgba_to_hex(color))

    def start_paste_sticker(self, event=None):
        """加载贴纸前强制清理状态"""
        self.cleanup_paste()  # 先清理旧状态
        
        path = filedialog.askopenfilename(
            filetypes=[("图片文件", "*.png;*.jpg;*.jpeg"), ("所有文件", "*.*")],
            parent=self
        )
        if not path:
            self.cleanup_paste()  # 用户取消时清理
            return
        
        try:
            img = Image.open(path).convert("RGBA")
            if img.width > self.width or img.height > self.height:
                messagebox.showerror("尺寸错误", f"贴图尺寸 ({img.width}x{img.height}) 超过画布 ({self.width}x{self.height})", parent=self)
                self.cleanup_paste()
                return
            
            self.paste_image = img
            self.canvas.bind("<Motion>", self.move_paste_preview)
            self.canvas.bind("<Button-1>", self.confirm_paste)
            self.show_paste_preview()
        except Exception as e:
            messagebox.showerror("错误", f"图片加载失败:\n{str(e)}", parent=self)
            self.cleanup_paste()

    def show_paste_preview(self):
        """显示半透明预览（修复边框不移动问题）"""
        if not self.paste_image:  
            return
        
        # 清理旧预览
        if self.paste_preview:
            self.canvas.delete(self.paste_preview)
            self.canvas.delete(self.paste_border)
        
        # 计算初始位置
        preview_x = (self.width * self.zoom - self.paste_image.width * self.zoom) // 2
        preview_y = (self.height * self.zoom - self.paste_image.height * self.zoom) // 2
        self.paste_position = (preview_x, preview_y)
        
        # 创建半透明预览图像
        preview_img = self.paste_image.copy()
        preview_img.putalpha(128)
        self.tk_preview_img = ImageTk.PhotoImage(
            preview_img.resize(
                (self.paste_image.width * self.zoom, 
                self.paste_image.height * self.zoom),
                Image.NEAREST
            )
        )
        
        # 绘制预览图像和动态边框
        self.paste_preview = self.canvas.create_image(
            preview_x, preview_y, 
            image=self.tk_preview_img, 
            anchor=tk.NW,
            tags="paste_preview"
        )
        self.paste_border = self.canvas.create_rectangle(
            preview_x, preview_y,
            preview_x + self.paste_image.width * self.zoom,
            preview_y + self.paste_image.height * self.zoom,
            outline="red", dash=(4,4), 
            tags="paste_preview"
        )


    def move_paste_preview(self, event):
        """拖动预览时同步更新图像和边框位置"""
        if not self.paste_image or not self.paste_preview:
            return
        
        # 计算允许的最大坐标
        max_x = self.width * self.zoom - self.paste_image.width * self.zoom
        max_y = self.height * self.zoom - self.paste_image.height * self.zoom
        
        # 计算新位置（以鼠标为中心点）
        new_x = max(0, min(event.x - self.paste_image.width * self.zoom // 2, max_x))
        new_y = max(0, min(event.y - self.paste_image.height * self.zoom // 2, max_y))
        
        # 同步移动预览图像和边框
        self.canvas.coords(self.paste_preview, new_x, new_y)
        self.canvas.coords(
            self.paste_border,
            new_x, new_y,
            new_x + self.paste_image.width * self.zoom,
            new_y + self.paste_image.height * self.zoom
        )
        self.paste_position = (new_x, new_y)

    def confirm_paste(self, event):
        """执行粘贴前进行三重安全检查"""
        # 三重检查：必须全部有效
        if not (self.paste_preview and self.paste_image and self.paste_position):
            return

        # 转换为像素坐标
        try:
            paste_x = self.paste_position[0] // self.zoom
            paste_y = self.paste_position[1] // self.zoom
        except TypeError:
            return  # 如果 paste_position 为 None 则直接退出

        # 计算贴图右下角坐标
        end_x = paste_x + self.paste_image.width
        end_y = paste_y + self.paste_image.height

        # 位置审查：不能超出画布范围
        if (paste_x < 0 or paste_y < 0 or end_x > self.width or end_y > self.height):
            messagebox.showerror("位置错误", "贴图部分超出画布范围，请调整位置后重试", parent=self)
            return

        # 记录旧像素用于撤销
        self.start_batch()
        for dx in range(self.paste_image.width):
            for dy in range(self.paste_image.height):
                target_x = paste_x + dx
                target_y = paste_y + dy
                if 0 <= target_x < self.width and 0 <= target_y < self.height:
                    old_color = self.pixels[target_x, target_y]
                    self.record_pixel_change(target_x, target_y, old_color)

        # 执行覆盖操作（删除重复代码块）
        for dx in range(self.paste_image.width):
            for dy in range(self.paste_image.height):
                target_x = paste_x + dx
                target_y = paste_y + dy
                if 0 <= target_x < self.width and 0 <= target_y < self.height:
                    src_pixel = self.paste_image.getpixel((dx, dy))
                    if src_pixel[3] > 0:
                        self.pixels[target_x, target_y] = src_pixel
                        self.update_pixel(target_x, target_y)

        self.end_batch()
        self.cleanup_paste()  # 仅保留一次清理调用
        
    def cleanup_paste(self):
        """彻底清理所有粘贴相关状态"""
        # 删除画布上的预览元素
        self.canvas.delete("paste_preview")
        
        # 重置所有变量为初始状态
        self.paste_preview = None
        self.paste_image = None
        self.paste_position = None
        self.paste_border = None
        
        # 强制解除事件绑定
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Button-1>")
        
        # 重新绑定基础绘图事件
        self.bind_events()
        
        # 重置绘制状态
        self.drawing = False
        self.current_batch = None

    def handle_recent_color_right_click(self, event, color):
        """处理历史颜色右键点击事件：弹出对话框询问是否添加到预设面板"""
        if color in self.preset_colors:
            messagebox.showinfo("提示", "该颜色已在预设面板中！", parent=self)
            return

        confirm_dlg = tk.Toplevel(self)
        confirm_dlg.wm_overrideredirect(True)
        confirm_dlg.geometry(f"+{event.x_root+10}+{event.y_root+10}")
        
        ttk.Label(confirm_dlg, text="添加此颜色到预设面板？").pack(padx=10, pady=5)
        btn_frame = ttk.Frame(confirm_dlg)
        btn_frame.pack(pady=5)
        
        def add_action():
            self.preset_colors.append(color)
            self.init_preset_panel()
            confirm_dlg.destroy()
        
        ttk.Button(btn_frame, text="确定", command=add_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=confirm_dlg.destroy).pack(side=tk.LEFT)
        
        confirm_dlg.bind("<FocusOut>", lambda e: confirm_dlg.destroy())
        confirm_dlg.focus_force()

    def on_recent_color_right_click(self, event, index):
        """根据索引获取颜色并触发处理"""
        if index < len(self.recent_colors):
            color = self.recent_colors[index]
            self.handle_recent_color_right_click(event, color)

    def _center_window(self, window):
        """辅助函数：居中窗口"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = self.winfo_x() + (self.winfo_width() - width) // 2
        y = self.winfo_y() + (self.winfo_height() - height) // 2
        window.geometry(f"+{x}+{y}")

    def update_brush_size(self, event=None):
        """根据用户选择更新笔刷大小"""
        size_str = self.brush_var.get()
        self.brush_size = int(size_str.split('x')[0])
    
    @staticmethod
    def rgba_to_hex(rgba):
        if len(rgba) != 4 or any(not (0 <= c <= 255) for c in rgba):
            return ""
        return f"#{rgba[0]:02X}{rgba[1]:02X}{rgba[2]:02X}" if rgba[3] != 0 else ""
    
    @staticmethod
    def hex_to_rgba(hex_color):
        hex_color = hex_color.lstrip("#")
        if len(hex_color) not in (6, 8):
            return (0, 0, 0, 255)
        return (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16),
            255
        )
    
    def on_close(self):
        """关闭程序时强制清理资源"""
        self.cleanup_paste()  # 显式调用清理
        self.image.close()
        self.destroy()
        self.quit()

    def show_help(self):
        """显示帮助文档窗口"""
        help_window = tk.Toplevel(self)
        help_window.title("使用帮助")
        
        # 设置窗口大小并居中
        help_window.geometry("800x400")
        self._center_window(help_window)
        
        # 创建滚动文本框
        help_text = tk.scrolledtext.ScrolledText(
            help_window,
            wrap=tk.WORD,
            font=("宋体", 10),
            padx=10,
            pady=10
        )
        help_text.pack(expand=True, fill=tk.BOTH)

        help_content = """【Pixetto 使用指南】

1. 基本操作                                     ____   __   _  _  ____  ____  ____   __  
- 左键单击画布：绘制像素                        (  _ \ (  ) ( \/ )(  __)(_  _)(_  _) /  \ 
- 右键单击画布：拾取颜色                         ) __/  )(   )  (  ) _)   )(    )(  (  O )
- 按住左键拖动：连续绘制                        (__)   (__) (_/\_)(____) (__)  (__)  \__/ 

2. 颜色管理
- 预设颜色：左键选择，右键删除，数量不限
- 颜色历史（最下方滚动更新）：右键可添加到预设面板
- 透明模式：作为橡皮擦使用，保存为 .png 才可以实现透明像素 !!

3. 高级功能
- 撤销（Ctrl+Z）：最多缓存 100 步，可以撤销黏贴操作
- 导入/导出颜色：支持 .txt 文件，创建并保存自己的预制调色盒，绘制风格相似的作品
- 粘贴图片（Ctrl+A）:选择图片进行黏贴，注意不要超出画布大小
- 笔刷：提供多种大小的笔刷方便大面积上色，可以在脚本中 Ctrl+F 搜索“笔刷”，添加自定义笔刷大小（奇数）

4. 保存选项
- 支持 PNG/JPG/BMP 格式
- 可设置放大倍数导出，原先的一个像素将作为一个边长为 n 的正方形保存

5.其他
- 暂不支持多次打开画布，完成一次编辑之后直接关闭程序再打开即可
- 不支持图像缩小功能，放大前的原始图像建议保存!!
- 为了编辑灵活以及减少卡顿，建议像素画边长不超过128
- 建议打开画布时的缩放比例不要设置过大，可以多次尝试进行调整
- 其他超酷的 bug 等你去发现

一些缩放比例参考（像素画上的一个像素以 nxn 个实际显示屏像素显示）
|像素画大小|选择缩放比例|
|  32x32  |     20    |
|  64x64  |     10    |
| 128x128 |      4    |
|   >256  |寻找专业软件|

-创造你自己的 pixel art 吧 
-我的Github主页:https://github.com/Vertinpy

"""
        help_text.insert(tk.INSERT, help_content)
        help_text.configure(state="disabled")  # 禁止编辑

def main():
    root = EnhancedPixelEditor()
    root.withdraw()
    
    choice = messagebox.askyesnocancel(
        "Pixetto",
        "是否创建新画布？",
        detail="是 - 新建空白画布\n否 - 打开现有图片\n取消 - 退出程序",
        parent=root
    )
    
    if choice is None:
        root.destroy()
        return
    elif choice:
        # 新建画布（含尺寸和缩放设置）
        dlg = NewCanvasDialog(root)
        root.wait_window(dlg)
        if dlg.result:
            width, height, zoom = dlg.result
            img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            root.destroy()
            EnhancedPixelEditor(img, zoom=zoom).mainloop()
        else:
            root.destroy()
    else:
        # 打开图片时使用自定义缩放对话框
        path = filedialog.askopenfilename(
            parent=root,
            filetypes=[("图片文件", "*.png;*.jpg;*.jpeg"), ("所有文件", "*.*")]
        )
        if path:
            # 弹出自定义缩放对话框
            zoom_dlg = ZoomDialog(root)
            root.wait_window(zoom_dlg)
            if zoom_dlg.result:
                try:
                    img = Image.open(path).convert("RGBA")
                    root.destroy()
                    EnhancedPixelEditor(img, zoom=zoom_dlg.result).mainloop()
                except Exception as e:
                    messagebox.showerror("错误", f"图片加载失败:\n{str(e)}", parent=root)
                    root.destroy()
            else:
                root.destroy()
        else:
            root.destroy()

if __name__ == "__main__":
    main()

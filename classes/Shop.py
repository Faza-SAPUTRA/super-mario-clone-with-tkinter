import tkinter as tk

import customtkinter as ctk

from classes.UiAssets import UiAssets


class Shop:
    """Pixel-art companion panel for buying items, inventory, and quests."""

    BG = "#111827"
    PANEL = "#1F2937"
    PANEL_ALT = "#273449"
    BORDER = "#4B5563"
    TEXT = "#F9FAFB"
    MUTED = "#9CA3AF"
    RED = "#DC2626"
    RED_HOVER = "#B91C1C"
    YELLOW = "#FACC15"
    GREEN = "#16A34A"
    GREEN_HOVER = "#15803D"
    DISABLED = "#374151"
    FONT = "Consolas"

    def __init__(self, mario):
        self.mario = mario
        self.assets = UiAssets()
        self.activeSection = "SHOP"
        self.inventoryLabels = {}
        self.inventoryButtons = {}
        self.questLabels = {}
        self.questBars = {}
        self.buyButtons = {}
        self.navButtons = {}
        self.sections = {}

        self.items = [
            {
                "name": "Mushroom",
                "title": "MUSHROOM",
                "description": "Grow before the next hit.",
                "price": 5,
                "color": "#DC2626",
                "command": self.mario.buyMushroom,
            },
            {
                "name": "Star Shield",
                "title": "STAR SHIELD",
                "description": "Ten seconds of enemy immunity.",
                "price": 8,
                "color": "#2563EB",
                "command": self.mario.buyShield,
            },
            {
                "name": "Super Jump",
                "title": "SUPER JUMP",
                "description": "Instant emergency vertical boost.",
                "price": 3,
                "color": "#16A34A",
                "command": self.mario.buySuperJump,
            },
            {
                "name": "Enemy Cleaner",
                "title": "ENEMY CLEANER",
                "description": "Clear nearby enemies in one tap.",
                "price": 10,
                "color": "#7C3AED",
                "command": self.mario.buyEnemyCleaner,
            },
        ]

        ctk.set_appearance_mode("dark")
        self.window = ctk.CTk()
        self.window.title("Toad House - Pixel Supply Shop")
        windowWidth = 960
        windowHeight = 680
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()
        windowX = max(0, (screenWidth - windowWidth) // 2)
        windowY = max(0, (screenHeight - windowHeight) // 2)
        self.window.geometry(
            str(windowWidth)
            + "x"
            + str(windowHeight)
            + "+"
            + str(windowX)
            + "+"
            + str(windowY)
        )
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.closeShop)
        self.window.bind("<Escape>", self.closeShop)
        self.window.bind("<Key-b>", self.closeShop)
        self.window.bind("<Key-B>", self.closeShop)
        self.window.bind("<Key-1>", lambda event: self.showSection("SHOP"))
        self.window.bind("<Key-2>", lambda event: self.showSection("BAG"))
        self.window.bind("<Key-3>", lambda event: self.showSection("QUESTS"))

        self.coinText = tk.StringVar(self.window)
        self.checkpointText = tk.StringVar(self.window)
        self.statusText = tk.StringVar(self.window, value=self.getOpeningMessage())

        self.drawShop()
        self.showSection("SHOP")
        self.refresh()
        self.window.after(100, self.window.focus_force)

    def getOpeningMessage(self):
        if self.mario.shopMessage:
            message = self.mario.shopMessage
            self.mario.shopMessage = ""
            return message
        return "Toad says: pick a tool, prepare your bag, and keep moving!"

    def pixelLabel(self, parent, **kwargs):
        kwargs.setdefault("font", (self.FONT, 12, "bold"))
        return ctk.CTkLabel(parent, **kwargs)

    def drawShop(self):
        backdrop = ctk.CTkLabel(self.window, text="", image=self.assets.shopBackdrop)
        backdrop.place(x=0, y=0, relwidth=1, relheight=1)

        shell = ctk.CTkFrame(
            self.window,
            width=900,
            height=622,
            corner_radius=0,
            fg_color=self.BG,
            border_width=4,
            border_color="#6B4423",
        )
        shell.place(x=30, y=28)
        shell.grid_propagate(False)
        shell.grid_columnconfigure(0, weight=1)
        shell.grid_rowconfigure(1, weight=1)

        self.drawHeader(shell)

        body = ctk.CTkFrame(shell, corner_radius=0, fg_color=self.BG)
        body.grid(row=1, column=0, sticky="nsew", padx=14, pady=(10, 0))

        sidebar = ctk.CTkFrame(
            body,
            width=178,
            corner_radius=0,
            fg_color=self.PANEL,
            border_width=2,
            border_color=self.BORDER,
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        self.drawSidebar(sidebar)

        content = ctk.CTkFrame(
            body,
            corner_radius=0,
            fg_color=self.PANEL,
            border_width=2,
            border_color=self.BORDER,
        )
        content.pack(side="left", fill="both", expand=True, padx=(12, 0))

        for name in ("SHOP", "BAG", "QUESTS"):
            frame = ctk.CTkFrame(content, corner_radius=0, fg_color=self.PANEL)
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.sections[name] = frame

        self.drawShopSection(self.sections["SHOP"])
        self.drawInventorySection(self.sections["BAG"])
        self.drawQuestSection(self.sections["QUESTS"])
        self.drawStatusBar(shell)

    def drawHeader(self, parent):
        header = ctk.CTkFrame(
            parent,
            height=86,
            corner_radius=0,
            fg_color=self.RED,
            border_width=0,
        )
        header.grid(row=0, column=0, sticky="ew", padx=4, pady=4)
        header.grid_propagate(False)

        ctk.CTkLabel(header, text="", image=self.assets.mario).pack(
            side="left", padx=(18, 8), pady=8
        )

        title = ctk.CTkFrame(header, fg_color="transparent")
        title.pack(side="left", pady=12)
        self.pixelLabel(
            title,
            text="TOAD HOUSE",
            text_color="#FFFFFF",
            font=(self.FONT, 28, "bold"),
        ).pack(anchor="w")
        self.pixelLabel(
            title,
            text="PIXEL SUPPLY STATION",
            text_color="#FECACA",
            font=(self.FONT, 11, "bold"),
        ).pack(anchor="w")

        balance = ctk.CTkFrame(
            header,
            corner_radius=0,
            fg_color="#991B1B",
            border_width=2,
            border_color="#FCA5A5",
        )
        balance.pack(side="right", padx=18, pady=17)
        ctk.CTkLabel(balance, text="", image=self.assets.coin).pack(
            side="left", padx=(8, 2), pady=3
        )
        self.pixelLabel(
            balance,
            textvariable=self.coinText,
            text_color=self.YELLOW,
            font=(self.FONT, 17, "bold"),
        ).pack(side="left", padx=(2, 12))

    def drawSidebar(self, parent):
        self.pixelLabel(
            parent,
            text="MENU",
            text_color=self.YELLOW,
            font=(self.FONT, 15, "bold"),
        ).pack(anchor="w", padx=16, pady=(18, 10))

        for index, name in enumerate(("SHOP", "BAG", "QUESTS"), start=1):
            button = ctk.CTkButton(
                parent,
                text=str(index) + "  " + name,
                command=lambda section=name: self.showSection(section),
                height=42,
                corner_radius=0,
                border_width=2,
                border_color=self.BORDER,
                fg_color=self.DISABLED,
                hover_color="#4B5563",
                anchor="w",
                font=(self.FONT, 13, "bold"),
            )
            button.pack(fill="x", padx=12, pady=5)
            self.navButtons[name] = button

        tip = ctk.CTkFrame(
            parent,
            corner_radius=0,
            fg_color=self.BG,
            border_width=2,
            border_color="#374151",
        )
        tip.pack(side="bottom", fill="x", padx=12, pady=12)
        self.pixelLabel(
            tip,
            text="QUICK KEYS",
            text_color=self.YELLOW,
            font=(self.FONT, 11, "bold"),
        ).pack(anchor="w", padx=10, pady=(10, 3))
        self.pixelLabel(
            tip,
            text="1 / 2 / 3  SWITCH\nB or ESC   CLOSE",
            text_color=self.MUTED,
            font=(self.FONT, 10, "bold"),
            justify="left",
        ).pack(anchor="w", padx=10, pady=(0, 10))

    def drawSectionTitle(self, parent, title, subtitle):
        self.pixelLabel(
            parent,
            text=title,
            text_color=self.TEXT,
            font=(self.FONT, 20, "bold"),
        ).pack(anchor="w", padx=18, pady=(16, 2))
        self.pixelLabel(
            parent,
            text=subtitle,
            text_color=self.MUTED,
            font=(self.FONT, 11, "bold"),
        ).pack(anchor="w", padx=18, pady=(0, 10))

    def drawShopSection(self, parent):
        self.drawSectionTitle(
            parent,
            "SUPPLY SHELF",
            "Buy now, activate later from your bag.",
        )

        grid = ctk.CTkFrame(parent, height=188, fg_color="transparent")
        grid.pack(fill="x", padx=12)
        grid.pack_propagate(False)
        grid.grid_columnconfigure((0, 1), weight=1)
        grid.grid_rowconfigure((0, 1), weight=1)

        for index, item in enumerate(self.items):
            self.drawItemCard(grid, index // 2, index % 2, item)

        checkpoint = ctk.CTkFrame(
            parent,
            height=62,
            corner_radius=0,
            fg_color="#173C2A",
            border_width=3,
            border_color=self.GREEN,
        )
        checkpoint.pack(fill="x", padx=18, pady=(8, 14))
        checkpoint.pack_propagate(False)
        ctk.CTkLabel(
            checkpoint,
            text="",
            image=self.assets.itemIcons["Checkpoint"],
        ).pack(side="left", padx=(10, 3))

        info = ctk.CTkFrame(checkpoint, fg_color="transparent")
        info.pack(side="left", fill="y", pady=5)
        self.pixelLabel(
            info,
            text="CHECKPOINT PIPE",
            text_color="#BBF7D0",
            font=(self.FONT, 13, "bold"),
        ).pack(anchor="w")
        self.pixelLabel(
            info,
            textvariable=self.checkpointText,
            text_color="#86EFAC",
            font=(self.FONT, 10, "bold"),
        ).pack(anchor="w")

        self.checkpointButton = ctk.CTkButton(
            checkpoint,
            text="SAVE HERE  |  6 COINS",
            command=lambda: self.runAction(self.mario.buyCheckpoint),
            width=185,
            height=32,
            corner_radius=0,
            border_width=2,
            border_color="#86EFAC",
            fg_color=self.GREEN,
            hover_color=self.GREEN_HOVER,
            font=(self.FONT, 11, "bold"),
        )
        self.checkpointButton.pack(side="right", padx=12)

    def drawItemCard(self, parent, row, column, item):
        card = ctk.CTkFrame(
            parent,
            height=88,
            corner_radius=0,
            fg_color=self.PANEL_ALT,
            border_width=3,
            border_color=item["color"],
        )
        card.grid(row=row, column=column, sticky="nsew", padx=6, pady=6)
        card.pack_propagate(False)

        iconBox = ctk.CTkFrame(
            card,
            width=66,
            corner_radius=0,
            fg_color=self.BG,
            border_width=2,
            border_color=item["color"],
        )
        iconBox.pack(side="left", fill="y", padx=7, pady=7)
        iconBox.pack_propagate(False)
        ctk.CTkLabel(
            iconBox,
            text="",
            image=self.assets.itemIcons[item["name"]],
        ).pack(expand=True)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, padx=(0, 7), pady=7)
        self.pixelLabel(
            info,
            text=item["title"],
            text_color=self.TEXT,
            font=(self.FONT, 13, "bold"),
        ).pack(anchor="w")
        self.pixelLabel(
            info,
            text=item["description"],
            text_color=self.MUTED,
            font=(self.FONT, 10, "bold"),
            wraplength=200,
            justify="left",
        ).pack(anchor="w", pady=(1, 4))

        button = ctk.CTkButton(
            info,
            text="BUY  " + str(item["price"]) + " COINS",
            command=lambda action=item["command"]: self.runAction(action),
            height=25,
            corner_radius=0,
            border_width=2,
            border_color=item["color"],
            fg_color=item["color"],
            hover_color=item["color"],
            font=(self.FONT, 10, "bold"),
        )
        button.pack(anchor="w", fill="x")
        self.buyButtons[item["name"]] = (button, item)

    def drawInventorySection(self, parent):
        self.drawSectionTitle(
            parent,
            "ITEM BAG",
            "Items stay here until you choose to activate them.",
        )

        for item in self.items:
            row = ctk.CTkFrame(
                parent,
                height=78,
                corner_radius=0,
                fg_color=self.PANEL_ALT,
                border_width=2,
                border_color=item["color"],
            )
            row.pack(fill="x", padx=18, pady=6)
            row.pack_propagate(False)
            ctk.CTkLabel(
                row,
                text="",
                image=self.assets.itemIcons[item["name"]],
            ).pack(side="left", padx=(12, 8))

            self.pixelLabel(
                row,
                text=item["title"],
                text_color=self.TEXT,
                width=190,
                anchor="w",
                font=(self.FONT, 12, "bold"),
            ).pack(side="left")

            amount = tk.StringVar(self.window)
            self.inventoryLabels[item["name"]] = amount
            self.pixelLabel(
                row,
                textvariable=amount,
                text_color=self.YELLOW,
                width=70,
                font=(self.FONT, 13, "bold"),
            ).pack(side="left")

            useCommand = {
                "Mushroom": self.mario.useMushroom,
                "Star Shield": self.mario.useShield,
                "Super Jump": self.mario.useSuperJump,
                "Enemy Cleaner": self.mario.useEnemyCleaner,
            }[item["name"]]
            button = ctk.CTkButton(
                row,
                text="USE ITEM",
                command=lambda action=useCommand: self.runAction(action),
                width=125,
                height=34,
                corner_radius=0,
                border_width=2,
                border_color=item["color"],
                fg_color=item["color"],
                hover_color=item["color"],
                font=(self.FONT, 10, "bold"),
            )
            button.pack(side="right", padx=12)
            self.inventoryButtons[item["name"]] = button

    def drawQuestSection(self, parent):
        self.drawSectionTitle(
            parent,
            "TOAD MISSIONS",
            "Optional goals pay bonus coins automatically.",
        )

        for quest in self.mario.quests.getQuests():
            card = ctk.CTkFrame(
                parent,
                height=105,
                corner_radius=0,
                fg_color=self.PANEL_ALT,
                border_width=2,
                border_color="#D97706",
            )
            card.pack(fill="x", padx=18, pady=5)
            card.pack_propagate(False)
            self.pixelLabel(
                card,
                text=quest.title.upper(),
                text_color=self.YELLOW,
                font=(self.FONT, 13, "bold"),
            ).pack(anchor="w", padx=14, pady=(8, 1))
            self.pixelLabel(
                card,
                text=quest.description + "  REWARD: +" + str(quest.reward),
                text_color=self.MUTED,
                font=(self.FONT, 10, "bold"),
            ).pack(anchor="w", padx=14)

            progress = ctk.CTkProgressBar(
                card,
                height=12,
                corner_radius=0,
                fg_color=self.BG,
                progress_color=self.GREEN,
                border_width=1,
                border_color=self.BORDER,
            )
            progress.pack(fill="x", padx=14, pady=(5, 2))
            self.questBars[quest.title] = progress

            progressText = tk.StringVar(self.window)
            self.questLabels[quest.title] = progressText
            self.pixelLabel(
                card,
                textvariable=progressText,
                text_color="#86EFAC",
                font=(self.FONT, 10, "bold"),
            ).pack(anchor="e", padx=14, pady=(0, 6))

    def drawStatusBar(self, parent):
        footer = ctk.CTkFrame(
            parent,
            height=58,
            corner_radius=0,
            fg_color=self.BG,
            border_width=0,
        )
        footer.grid(row=2, column=0, sticky="ew", padx=14, pady=(8, 12))
        footer.grid_propagate(False)

        self.statusPanel = ctk.CTkFrame(
            footer,
            corner_radius=0,
            fg_color=self.PANEL,
            border_width=2,
            border_color=self.BORDER,
        )
        self.statusPanel.pack(side="left", fill="both", expand=True)
        self.statusLabel = self.pixelLabel(
            self.statusPanel,
            textvariable=self.statusText,
            text_color=self.TEXT,
            font=(self.FONT, 10, "bold"),
            anchor="w",
        )
        self.statusLabel.pack(fill="both", expand=True, padx=12)

        ctk.CTkButton(
            footer,
            text="CONTINUE LEVEL  [B]",
            command=self.closeShop,
            width=200,
            height=42,
            corner_radius=0,
            border_width=2,
            border_color="#86EFAC",
            fg_color=self.GREEN,
            hover_color=self.GREEN_HOVER,
            font=(self.FONT, 11, "bold"),
        ).pack(side="right", padx=(10, 0), pady=7)

    def showSection(self, section):
        self.activeSection = section
        self.sections[section].lift()

        for name, button in self.navButtons.items():
            if name == section:
                button.configure(
                    fg_color=self.RED,
                    hover_color=self.RED_HOVER,
                    border_color="#FCA5A5",
                )
            else:
                button.configure(
                    fg_color=self.DISABLED,
                    hover_color="#4B5563",
                    border_color=self.BORDER,
                )

    def runAction(self, command):
        message = command()
        self.statusText.set(message)

        failure = (
            message.startswith("Not enough")
            or message.startswith("You do not")
            or message.startswith("Cannot")
        )
        if failure:
            self.statusPanel.configure(border_color="#EF4444")
            self.statusLabel.configure(text_color="#FCA5A5")
        else:
            self.statusPanel.configure(border_color=self.GREEN)
            self.statusLabel.configure(text_color="#86EFAC")

        self.refresh()

    def refresh(self):
        coins = self.mario.dashboard.coins
        self.coinText.set(str(coins).zfill(2) + " COINS")
        self.checkpointText.set("STATUS: " + self.mario.checkpoints.getStatus())

        for itemName, label in self.inventoryLabels.items():
            amount = self.mario.inventory.getAmount(itemName)
            label.set("x" + str(amount))
            state = "normal" if amount > 0 else "disabled"
            self.inventoryButtons[itemName].configure(state=state)

        for itemName, buttonData in self.buyButtons.items():
            button, item = buttonData
            state = "normal" if coins >= item["price"] else "disabled"
            button.configure(state=state)

        checkpointState = "normal" if coins >= 6 else "disabled"
        self.checkpointButton.configure(state=checkpointState)

        for quest in self.mario.quests.getQuests():
            progress = min(1, quest.progress / quest.target)
            self.questBars[quest.title].set(progress)
            if quest.completed:
                self.questLabels[quest.title].set("COMPLETE  +" + str(quest.reward) + " COINS")
            else:
                self.questLabels[quest.title].set(
                    str(quest.progress) + " / " + str(quest.target)
                )

    def closeShop(self, event=None):
        self.window.destroy()

    def open(self):
        self.window.mainloop()

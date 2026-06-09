import sys

import pygame


class PygameShop:
    """In-game shop overlay used when the Pygame display is fullscreen."""

    BG = (17, 24, 39)
    PANEL = (31, 41, 55)
    PANEL_ALT = (39, 52, 73)
    BORDER = (75, 85, 99)
    TEXT = (249, 250, 251)
    MUTED = (156, 163, 175)
    RED = (220, 38, 38)
    YELLOW = (250, 204, 21)
    GREEN = (22, 163, 74)
    DISABLED = (55, 65, 81)
    DANGER = (248, 113, 113)

    def __init__(self, mario):
        self.mario = mario
        self.screen = mario.screen
        self.background = self.screen.copy()
        self.section = 0
        self.selectedAction = 0
        self.actionButtons = []
        self.tabButtons = []
        self.running = True
        self.status = self.getOpeningMessage()
        self.statusColor = self.TEXT
        self.clock = pygame.time.Clock()

        self.items = [
            ("MUSHROOM", "Grow before the next hit.", 5, self.RED, mario.buyMushroom),
            ("STAR SHIELD", "10 seconds of immunity.", 8, (37, 99, 235), mario.buyShield),
            ("SUPER JUMP", "Emergency vertical boost.", 3, self.GREEN, mario.buySuperJump),
            ("ENEMY CLEANER", "Clear nearby enemies.", 10, (124, 58, 237), mario.buyEnemyCleaner),
        ]
        self.useActions = [
            ("MUSHROOM", "Mushroom", self.RED, mario.useMushroom),
            ("STAR SHIELD", "Star Shield", (37, 99, 235), mario.useShield),
            ("SUPER JUMP", "Super Jump", self.GREEN, mario.useSuperJump),
            ("ENEMY CLEANER", "Enemy Cleaner", (124, 58, 237), mario.useEnemyCleaner),
        ]

    def getOpeningMessage(self):
        if self.mario.shopMessage:
            message = self.mario.shopMessage
            self.mario.shopMessage = ""
            return message
        return "Pick a tool, prepare your bag, then continue the level."

    def open(self):
        pygame.key.set_repeat(250, 90)
        while self.running:
            self.draw()
            pygame.display.flip()
            self.handleEvents()
            self.clock.tick(30)
        pygame.key.set_repeat()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_b):
                    self.running = False
                elif event.key in (pygame.K_1, pygame.K_KP1):
                    self.changeSection(0)
                elif event.key in (pygame.K_2, pygame.K_KP2):
                    self.changeSection(1)
                elif event.key in (pygame.K_3, pygame.K_KP3):
                    self.changeSection(2)
                elif event.key in (pygame.K_TAB, pygame.K_RIGHT):
                    self.changeSection((self.section + 1) % 3)
                elif event.key == pygame.K_LEFT:
                    self.changeSection((self.section - 1) % 3)
                elif event.key == pygame.K_DOWN and self.actionButtons:
                    self.selectedAction = (self.selectedAction + 1) % len(self.actionButtons)
                elif event.key == pygame.K_UP and self.actionButtons:
                    self.selectedAction = (self.selectedAction - 1) % len(self.actionButtons)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.activateSelected()

            if event.type == pygame.MOUSEMOTION:
                for index, button in enumerate(self.actionButtons):
                    if button["rect"].collidepoint(event.pos):
                        self.selectedAction = index

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for index, rect in enumerate(self.tabButtons):
                    if rect.collidepoint(event.pos):
                        self.changeSection(index)
                        break
                else:
                    for index, button in enumerate(self.actionButtons):
                        if button["rect"].collidepoint(event.pos):
                            self.selectedAction = index
                            self.activateSelected()
                            break

    def changeSection(self, section):
        self.section = section
        self.selectedAction = 0

    def activateSelected(self):
        if not self.actionButtons:
            return

        button = self.actionButtons[self.selectedAction]
        if not button["enabled"]:
            self.status = button["disabledMessage"]
            self.statusColor = self.DANGER
            return

        message = button["command"]()
        self.status = message
        if (
            message.startswith("Not enough")
            or message.startswith("You do not")
            or message.startswith("Cannot")
        ):
            self.statusColor = self.DANGER
        else:
            self.statusColor = (134, 239, 172)

    def draw(self):
        width, height = self.screen.get_size()
        self.screen.blit(self.background, (0, 0))

        shade = pygame.Surface((width, height), pygame.SRCALPHA)
        shade.fill((3, 7, 18, 205))
        self.screen.blit(shade, (0, 0))

        scale = min(width / 640, height / 480)
        panelWidth = min(width - 24, int(610 * scale))
        panelHeight = min(height - 20, int(456 * scale))
        panel = pygame.Rect(
            (width - panelWidth) // 2,
            (height - panelHeight) // 2,
            panelWidth,
            panelHeight,
        )

        pygame.draw.rect(self.screen, self.BG, panel)
        pygame.draw.rect(self.screen, (107, 68, 35), panel, max(2, int(4 * scale)))

        headerHeight = int(60 * scale)
        header = pygame.Rect(panel.x + 4, panel.y + 4, panel.w - 8, headerHeight)
        pygame.draw.rect(self.screen, self.RED, header)
        self.text("TOAD HOUSE", header.x + int(16 * scale), header.y + int(8 * scale), int(25 * scale))
        self.text(
            "FULLSCREEN SUPPLY OVERLAY",
            header.x + int(17 * scale),
            header.y + int(38 * scale),
            int(9 * scale),
            (254, 202, 202),
        )
        self.text(
            str(self.mario.dashboard.coins).zfill(2) + " COINS",
            header.right - int(112 * scale),
            header.y + int(21 * scale),
            int(14 * scale),
            self.YELLOW,
        )

        tabsY = header.bottom + int(8 * scale)
        tabHeight = int(30 * scale)
        tabGap = int(6 * scale)
        tabWidth = (panel.w - int(24 * scale) - tabGap * 2) // 3
        self.tabButtons = []
        for index, label in enumerate(("1  SHOP", "2  BAG", "3  QUESTS")):
            rect = pygame.Rect(
                panel.x + int(12 * scale) + index * (tabWidth + tabGap),
                tabsY,
                tabWidth,
                tabHeight,
            )
            self.tabButtons.append(rect)
            color = self.RED if index == self.section else self.PANEL_ALT
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, self.BORDER, rect, max(1, int(2 * scale)))
            self.centerText(label, rect, int(11 * scale), self.TEXT)

        content = pygame.Rect(
            panel.x + int(12 * scale),
            tabsY + tabHeight + int(7 * scale),
            panel.w - int(24 * scale),
            panel.h - headerHeight - tabHeight - int(104 * scale),
        )
        pygame.draw.rect(self.screen, self.PANEL, content)
        pygame.draw.rect(self.screen, self.BORDER, content, max(1, int(2 * scale)))

        self.actionButtons = []
        if self.section == 0:
            self.drawShop(content, scale)
        elif self.section == 1:
            self.drawBag(content, scale)
        else:
            self.drawQuests(content, scale)

        if self.actionButtons:
            self.selectedAction %= len(self.actionButtons)
            selected = self.actionButtons[self.selectedAction]["rect"].inflate(
                int(4 * scale), int(4 * scale)
            )
            pygame.draw.rect(self.screen, self.YELLOW, selected, max(2, int(2 * scale)))

        footer = pygame.Rect(
            panel.x + int(12 * scale),
            panel.bottom - int(47 * scale),
            panel.w - int(24 * scale),
            int(34 * scale),
        )
        pygame.draw.rect(self.screen, self.PANEL_ALT, footer)
        pygame.draw.rect(self.screen, self.BORDER, footer, max(1, int(2 * scale)))
        self.text(
            self.truncate(self.status, 58),
            footer.x + int(9 * scale),
            footer.y + int(8 * scale),
            int(9 * scale),
            self.statusColor,
        )
        self.text(
            "B / ESC  CLOSE",
            footer.right - int(105 * scale),
            footer.y + int(8 * scale),
            int(9 * scale),
            (134, 239, 172),
        )

    def drawShop(self, area, scale):
        padding = int(10 * scale)
        gap = int(7 * scale)
        cardWidth = (area.w - padding * 2 - gap) // 2
        cardHeight = int(70 * scale)

        for index, item in enumerate(self.items):
            row = index // 2
            column = index % 2
            rect = pygame.Rect(
                area.x + padding + column * (cardWidth + gap),
                area.y + padding + row * (cardHeight + gap),
                cardWidth,
                cardHeight,
            )
            name, description, price, color, command = item
            enabled = self.mario.dashboard.coins >= price
            pygame.draw.rect(self.screen, self.PANEL_ALT, rect)
            pygame.draw.rect(self.screen, color, rect, max(2, int(2 * scale)))
            self.drawPixelIcon(name, rect.x + int(12 * scale), rect.y + int(14 * scale), scale, color)
            self.text(name, rect.x + int(50 * scale), rect.y + int(10 * scale), int(11 * scale))
            self.text(
                description,
                rect.x + int(50 * scale),
                rect.y + int(29 * scale),
                int(8 * scale),
                self.MUTED,
            )
            button = pygame.Rect(
                rect.x + int(50 * scale),
                rect.bottom - int(22 * scale),
                rect.w - int(60 * scale),
                int(16 * scale),
            )
            pygame.draw.rect(self.screen, color if enabled else self.DISABLED, button)
            self.centerText("BUY " + str(price), button, int(8 * scale))
            self.addAction(
                button,
                command,
                enabled,
                "Not enough coins for " + name + ".",
            )

        checkpoint = pygame.Rect(
            area.x + padding,
            area.y + padding + (cardHeight + gap) * 2,
            area.w - padding * 2,
            int(46 * scale),
        )
        enabled = self.mario.dashboard.coins >= 6
        pygame.draw.rect(self.screen, (23, 60, 42), checkpoint)
        pygame.draw.rect(self.screen, self.GREEN, checkpoint, max(2, int(2 * scale)))
        self.text("CHECKPOINT PIPE", checkpoint.x + int(12 * scale), checkpoint.y + int(7 * scale), int(11 * scale))
        self.text(
            "STATUS: " + self.mario.checkpoints.getStatus(),
            checkpoint.x + int(12 * scale),
            checkpoint.y + int(25 * scale),
            int(8 * scale),
            (134, 239, 172),
        )
        button = pygame.Rect(
            checkpoint.right - int(140 * scale),
            checkpoint.y + int(10 * scale),
            int(128 * scale),
            int(26 * scale),
        )
        pygame.draw.rect(self.screen, self.GREEN if enabled else self.DISABLED, button)
        self.centerText("SAVE HERE - 6", button, int(8 * scale))
        self.addAction(button, self.mario.buyCheckpoint, enabled, "Not enough coins for a Checkpoint.")

    def drawBag(self, area, scale):
        padding = int(10 * scale)
        rowHeight = int(48 * scale)
        gap = int(7 * scale)

        for index, item in enumerate(self.useActions):
            title, inventoryName, color, command = item
            amount = self.mario.inventory.getAmount(inventoryName)
            rect = pygame.Rect(
                area.x + padding,
                area.y + padding + index * (rowHeight + gap),
                area.w - padding * 2,
                rowHeight,
            )
            pygame.draw.rect(self.screen, self.PANEL_ALT, rect)
            pygame.draw.rect(self.screen, color, rect, max(2, int(2 * scale)))
            self.drawPixelIcon(title, rect.x + int(12 * scale), rect.y + int(10 * scale), scale, color)
            self.text(title, rect.x + int(50 * scale), rect.y + int(8 * scale), int(11 * scale))
            self.text("x" + str(amount), rect.x + int(50 * scale), rect.y + int(27 * scale), int(10 * scale), self.YELLOW)
            button = pygame.Rect(
                rect.right - int(104 * scale),
                rect.y + int(11 * scale),
                int(92 * scale),
                int(27 * scale),
            )
            pygame.draw.rect(self.screen, color if amount > 0 else self.DISABLED, button)
            self.centerText("USE ITEM", button, int(8 * scale))
            self.addAction(
                button,
                command,
                amount > 0,
                "You do not have a " + inventoryName + " in your bag.",
            )

    def drawQuests(self, area, scale):
        padding = int(10 * scale)
        quests = self.mario.quests.getQuests()
        cardHeight = int(63 * scale)
        gap = int(8 * scale)

        for index, quest in enumerate(quests):
            rect = pygame.Rect(
                area.x + padding,
                area.y + padding + index * (cardHeight + gap),
                area.w - padding * 2,
                cardHeight,
            )
            pygame.draw.rect(self.screen, self.PANEL_ALT, rect)
            pygame.draw.rect(self.screen, (217, 119, 6), rect, max(2, int(2 * scale)))
            self.text(quest.title.upper(), rect.x + int(10 * scale), rect.y + int(7 * scale), int(11 * scale), self.YELLOW)
            self.text(
                quest.description + "  +" + str(quest.reward),
                rect.x + int(10 * scale),
                rect.y + int(25 * scale),
                int(8 * scale),
                self.MUTED,
            )
            bar = pygame.Rect(
                rect.x + int(10 * scale),
                rect.y + int(43 * scale),
                rect.w - int(72 * scale),
                int(10 * scale),
            )
            pygame.draw.rect(self.screen, self.BG, bar)
            progress = min(1, quest.progress / quest.target)
            fill = bar.copy()
            fill.w = int(bar.w * progress)
            pygame.draw.rect(self.screen, self.GREEN, fill)
            pygame.draw.rect(self.screen, self.BORDER, bar, 1)
            progressText = "DONE" if quest.completed else str(quest.progress) + "/" + str(quest.target)
            self.text(
                progressText,
                rect.right - int(52 * scale),
                rect.y + int(42 * scale),
                int(9 * scale),
                (134, 239, 172),
            )

    def addAction(self, rect, command, enabled, disabledMessage):
        self.actionButtons.append(
            {
                "rect": rect,
                "command": command,
                "enabled": enabled,
                "disabledMessage": disabledMessage,
            }
        )

    def drawPixelIcon(self, name, x, y, scale, color):
        pixel = max(2, int(4 * scale))
        patterns = {
            "MUSHROOM": ((1, 0, 4, 1), (0, 1, 6, 3), (2, 4, 4, 2)),
            "STAR SHIELD": ((1, 0, 4, 5), (0, 1, 6, 3)),
            "SUPER JUMP": ((2, 0, 2, 6), (0, 2, 6, 2)),
            "ENEMY CLEANER": ((2, 0, 2, 4), (0, 4, 6, 2)),
        }
        for px, py, pw, ph in patterns.get(name, patterns["MUSHROOM"]):
            pygame.draw.rect(
                self.screen,
                color,
                pygame.Rect(x + px * pixel, y + py * pixel, pw * pixel, ph * pixel),
            )

    def text(self, value, x, y, size, color=None):
        font = pygame.font.SysFont("consolas", max(8, size), bold=True)
        surface = font.render(str(value), False, color or self.TEXT)
        self.screen.blit(surface, (x, y))

    def centerText(self, value, rect, size, color=None):
        font = pygame.font.SysFont("consolas", max(8, size), bold=True)
        surface = font.render(str(value), False, color or self.TEXT)
        self.screen.blit(surface, surface.get_rect(center=rect.center))

    @staticmethod
    def truncate(value, limit):
        if len(value) <= limit:
            return value
        return value[: limit - 3] + "..."

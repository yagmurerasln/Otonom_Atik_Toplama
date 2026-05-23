import pygame
import random
from environment import WasteCollectionEnvironment


class WasteCollectionVisualizer:
    def __init__(self, env):
        pygame.init()

        self.env = env

        self.grid_size = self.env.grid_size
        self.cell_size = 58

        self.margin_left = 55
        self.margin_top = 35

        self.grid_width = self.grid_size * self.cell_size
        self.grid_height = self.grid_size * self.cell_size

        self.right_panel_width = 330
        self.bottom_panel_height = 120

        self.screen_width = (
            self.margin_left
            + self.grid_width
            + self.right_panel_width
            + 25
        )

        self.screen_height = (
            self.margin_top
            + self.grid_height
            + self.bottom_panel_height
            + 20
        )

        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height),
            pygame.RESIZABLE
        )

        pygame.display.set_caption("Akıllı Şehir - Q-Learning Çöp Toplama Ajanı")

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 15)
        self.tiny_font = pygame.font.SysFont("Arial", 12)

        self.training = False
        self.episode = 1
        self.epsilon = 1.00

        self.reward_history = []
        self.episode_rewards = []
        self.route = [self.env.truck_position]

        panel_x = self.margin_left + self.grid_width + 15

        self.start_button = pygame.Rect(panel_x + 20, 430, 245, 38)
        self.reset_button = pygame.Rect(panel_x + 20, 480, 245, 38)
        self.exit_button = pygame.Rect(panel_x + 20, 530, 245, 38)

    # -------------------------------------------------
    # KOORDİNAT DÖNÜŞÜMÜ
    # -------------------------------------------------
    # Mantıksal koordinat sistemi:
    # (0, 0) = sol alt köşe
    #
    # Pygame ekran koordinatı:
    # (0, 0) = sol üst köşe
    #
    # Bu yüzden y ekseni ters çevrilir.
    def logical_to_screen(self, x, y):
        screen_x = self.margin_left + x * self.cell_size
        screen_y = self.margin_top + (self.grid_size - 1 - y) * self.cell_size
        return screen_x, screen_y

    def cell_rect(self, x, y):
        screen_x, screen_y = self.logical_to_screen(x, y)
        return pygame.Rect(
            screen_x,
            screen_y,
            self.cell_size,
            self.cell_size
        )

    def cell_center(self, x, y):
        screen_x, screen_y = self.logical_to_screen(x, y)
        return (
            screen_x + self.cell_size // 2,
            screen_y + self.cell_size // 2
        )

    # -------------------------------------------------
    # GENEL ÇİZİM
    # -------------------------------------------------
    def draw_background(self):
        self.screen.fill((18, 24, 28))

    def draw_city_grid(self):
        road_columns = [2, 5, 8]
        road_rows = [3, 6]

        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = self.cell_rect(x, y)

                if x in road_columns or y in road_rows:
                    color = (58, 63, 67)
                else:
                    color = (78, 120, 45)

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (20, 25, 25), rect, 2)

                if x in road_columns:
                    line_x = rect.centerx
                    pygame.draw.line(
                        self.screen,
                        (220, 220, 220),
                        (line_x, rect.top + 8),
                        (line_x, rect.bottom - 8),
                        2
                    )

                if y in road_rows:
                    line_y = rect.centery
                    pygame.draw.line(
                        self.screen,
                        (220, 220, 220),
                        (rect.left + 8, line_y),
                        (rect.right - 8, line_y),
                        2
                    )

    def draw_coordinates(self):
        # X koordinatları: soldan sağa 0,1,2...
        for x in range(self.grid_size):
            text = self.small_font.render(str(x), True, (230, 230, 230))

            text_x = (
                self.margin_left
                + x * self.cell_size
                + self.cell_size // 2
                - 4
            )

            text_y = self.margin_top + self.grid_height + 6

            self.screen.blit(text, (text_x, text_y))

        # Y koordinatları: alttan üste 0,1,2...
        for y in range(self.grid_size):
            text = self.small_font.render(str(y), True, (230, 230, 230))

            text_x = self.margin_left - 26

            text_y = (
                self.margin_top
                + (self.grid_size - 1 - y) * self.cell_size
                + self.cell_size // 2
                - 8
            )

            self.screen.blit(text, (text_x, text_y))

    # -------------------------------------------------
    # ŞEHİR OBJELERİ
    # -------------------------------------------------
    def draw_static_objects(self):
        buildings = [
            (3, 9),
            (4, 9),
            (1, 5),
            (7, 5),
            (9, 7),
            (9, 2),
            (7, 1),
            (4, 4),
        ]

        trees = [
            (4, 7),
            (7, 7),
            (0, 4),
            (8, 4),
            (4, 2),
            (9, 0),
        ]

        rocks = [
            (3, 5),
            (5, 5),
            (1, 2),
            (9, 4),
        ]

        occupied_positions = set(self.env.containers.keys())
        occupied_positions.add(self.env.depot)
        occupied_positions.add(self.env.truck_position)

        for x, y in buildings:
            if (x, y) in occupied_positions:
                continue

            rect = self.cell_rect(x, y)

            building_rect = pygame.Rect(
                rect.left + 10,
                rect.top + 10,
                self.cell_size - 20,
                self.cell_size - 20
            )

            pygame.draw.rect(self.screen, (45, 45, 45), building_rect)
            pygame.draw.rect(self.screen, (15, 15, 15), building_rect, 4)

        for x, y in trees:
            if (x, y) in occupied_positions:
                continue

            cx, cy = self.cell_center(x, y)

            pygame.draw.rect(
                self.screen,
                (95, 55, 25),
                (cx - 4, cy + 8, 8, 18)
            )

            pygame.draw.circle(
                self.screen,
                (35, 120, 35),
                (cx - 8, cy),
                13
            )

            pygame.draw.circle(
                self.screen,
                (45, 150, 45),
                (cx + 8, cy),
                13
            )

            pygame.draw.circle(
                self.screen,
                (40, 135, 40),
                (cx, cy - 10),
                13
            )

        for x, y in rocks:
            if (x, y) in occupied_positions:
                continue

            cx, cy = self.cell_center(x, y)

            pygame.draw.circle(
                self.screen,
                (130, 130, 125),
                (cx, cy),
                14
            )

            pygame.draw.circle(
                self.screen,
                (95, 95, 90),
                (cx + 5, cy + 3),
                9
            )

    def draw_depot(self):
        x, y = self.env.depot
        rect = self.cell_rect(x, y)

        depot_rect = pygame.Rect(
            rect.left + 6,
            rect.top + 10,
            self.cell_size - 12,
            self.cell_size - 18
        )

        pygame.draw.rect(
            self.screen,
            (125, 70, 25),
            depot_rect,
            border_radius=5
        )

        pygame.draw.rect(
            self.screen,
            (60, 30, 10),
            depot_rect,
            3,
            border_radius=5
        )

        label = self.tiny_font.render("MERKEZ", True, (255, 255, 255))
        self.screen.blit(label, (depot_rect.left + 4, depot_rect.top + 6))

        door = pygame.Rect(
            depot_rect.centerx - 8,
            depot_rect.bottom - 14,
            16,
            14
        )

        pygame.draw.rect(self.screen, (10, 10, 10), door)

    def draw_containers(self):
        for position, fullness in self.env.containers.items():
            x, y = position
            cx, cy = self.cell_center(x, y)

            if position in self.env.collected_containers:
                color = (110, 110, 110)
                lid_color = (80, 80, 80)
                label = "X"
            elif fullness >= 80:
                color = (230, 85, 25)
                lid_color = (255, 120, 40)
                label = str(fullness)
            elif fullness >= 60:
                color = (220, 190, 30)
                lid_color = (245, 220, 60)
                label = str(fullness)
            else:
                color = (45, 170, 80)
                lid_color = (80, 210, 110)
                label = str(fullness)

            body = pygame.Rect(cx - 13, cy - 8, 26, 28)
            lid = pygame.Rect(cx - 15, cy - 16, 30, 9)

            pygame.draw.rect(self.screen, color, body, border_radius=4)
            pygame.draw.rect(self.screen, lid_color, lid, border_radius=4)

            pygame.draw.rect(self.screen, (20, 20, 20), body, 2)
            pygame.draw.rect(self.screen, (20, 20, 20), lid, 2)

            text = self.tiny_font.render(label, True, (255, 255, 255))
            self.screen.blit(text, (cx - 8, cy + 1))

    def draw_route(self):
        if len(self.route) < 2:
            return

        points = []

        for x, y in self.route:
            points.append(self.cell_center(x, y))

        pygame.draw.lines(
            self.screen,
            (0, 220, 255),
            False,
            points,
            3
        )

    def draw_truck(self):
        x, y = self.env.truck_position
        cx, cy = self.cell_center(x, y)

        body = pygame.Rect(cx - 18, cy - 8, 36, 22)
        cabin = pygame.Rect(cx - 12, cy - 18, 24, 14)

        pygame.draw.rect(
            self.screen,
            (35, 110, 230),
            body,
            border_radius=5
        )

        pygame.draw.rect(
            self.screen,
            (65, 145, 255),
            cabin,
            border_radius=5
        )

        pygame.draw.circle(
            self.screen,
            (10, 10, 10),
            (cx - 10, cy + 15),
            5
        )

        pygame.draw.circle(
            self.screen,
            (10, 10, 10),
            (cx + 10, cy + 15),
            5
        )

        recycle_text = self.tiny_font.render("RL", True, (255, 255, 255))
        self.screen.blit(recycle_text, (cx - 7, cy - 7))

    # -------------------------------------------------
    # PANEL VE BUTONLAR
    # -------------------------------------------------
    def draw_button(self, rect, text, color):
        mouse_pos = pygame.mouse.get_pos()

        draw_color = color

        if rect.collidepoint(mouse_pos):
            draw_color = (
                min(color[0] + 25, 255),
                min(color[1] + 25, 255),
                min(color[2] + 25, 255)
            )

        pygame.draw.rect(self.screen, draw_color, rect, border_radius=8)
        pygame.draw.rect(
            self.screen,
            (230, 230, 230),
            rect,
            2,
            border_radius=8
        )

        label = self.small_font.render(text, True, (255, 255, 255))
        label_rect = label.get_rect(center=rect.center)
        self.screen.blit(label, label_rect)

    def draw_info_panel(self):
        panel_x = self.margin_left + self.grid_width + 15
        panel_y = self.margin_top
        panel_width = self.right_panel_width - 20
        panel_height = 570

        panel_rect = pygame.Rect(
            panel_x,
            panel_y,
            panel_width,
            panel_height
        )

        pygame.draw.rect(self.screen, (28, 35, 39), panel_rect)
        pygame.draw.rect(self.screen, (60, 70, 75), panel_rect, 2)

        title = self.font.render("DURUM BİLGİLERİ", True, (40, 220, 40))
        self.screen.blit(title, (panel_x + 18, panel_y + 18))

        if self.training:
            mode_text = "Eğitim"
        else:
            mode_text = "Beklemede"

        infos = [
            ("Mod", mode_text),
            ("Episode", self.episode),
            ("Adım", self.env.step_count),
            ("Toplam Ödül", self.env.total_reward),
            (
                "Toplanan",
                f"{self.env.get_collected_count()} / "
                f"{self.env.get_total_container_count()}"
            ),
            ("Epsilon", f"{self.epsilon:.2f}"),
            ("Konum", str(self.env.truck_position)),
        ]

        info_start_y = panel_y + 60

        for index, (key, value) in enumerate(infos):
            key_text = self.small_font.render(
                f"{key}:",
                True,
                (220, 220, 220)
            )

            value_text = self.small_font.render(
                str(value),
                True,
                (255, 255, 255)
            )

            y = info_start_y + index * 32

            self.screen.blit(key_text, (panel_x + 18, y))
            self.screen.blit(value_text, (panel_x + 130, y))

        if self.training:
            start_text = "Öğrenmeyi Durdur"
            start_color = (180, 70, 50)
        else:
            start_text = "Öğrenmeyi Başlat"
            start_color = (50, 150, 80)

        self.draw_button(self.start_button, start_text, start_color)
        self.draw_button(self.reset_button, "Reset", (70, 100, 180))
        self.draw_button(self.exit_button, "Çıkış", (150, 60, 60))

        help_title = self.font.render("AÇIKLAMA", True, (0, 220, 220))
        self.screen.blit(help_title, (panel_x + 18, panel_y + 585))

        help_lines = [
            "Bu ekranda ok tuşu yok.",
            "Ajan butona basınca eğitim",
            "modunda kendi hareket eder.",
            "Şu an rastgele hareket var.",
            "Sonraki adımda agent.py ile",
            "Q-Learning + epsilon-greedy",
            "buraya bağlanacak."
        ]

        help_start_y = panel_y + 620

        for index, line in enumerate(help_lines):
            text = self.tiny_font.render(line, True, (220, 220, 220))
            self.screen.blit(text, (panel_x + 18, help_start_y + index * 18))

    def draw_legend_panel(self):
        panel_x = self.margin_left + self.grid_width + 15
        panel_y = self.margin_top + 650
        panel_width = self.right_panel_width - 20
        panel_height = 170

        # Ekran küçükse bu panel taşabilir, o yüzden çizim güvenli.
        if panel_y + panel_height > self.screen_height:
            return

        panel_rect = pygame.Rect(
            panel_x,
            panel_y,
            panel_width,
            panel_height
        )

        pygame.draw.rect(self.screen, (28, 35, 39), panel_rect)
        pygame.draw.rect(self.screen, (60, 70, 75), panel_rect, 2)

        title = self.font.render("LEJAND", True, (40, 220, 40))
        self.screen.blit(title, (panel_x + 18, panel_y + 15))

        items = [
            ((35, 110, 230), "Çöp Aracı"),
            ((45, 170, 80), "Az Dolu Kutu"),
            ((220, 190, 30), "Orta Dolu Kutu"),
            ((230, 85, 25), "Çok Dolu Kutu"),
            ((125, 70, 25), "Atık Merkezi"),
        ]

        start_y = panel_y + 50

        for index, (color, label) in enumerate(items):
            y = start_y + index * 23

            pygame.draw.rect(
                self.screen,
                color,
                (panel_x + 20, y, 18, 18),
                border_radius=4
            )

            text = self.tiny_font.render(label, True, (230, 230, 230))
            self.screen.blit(text, (panel_x + 50, y))

    def draw_reward_graph(self):
        x = self.margin_left
        y = self.margin_top + self.grid_height + 35
        w = self.grid_width
        h = 90

        pygame.draw.rect(self.screen, (28, 35, 39), (x, y, w, h))
        pygame.draw.rect(self.screen, (60, 70, 75), (x, y, w, h), 2)

        title = self.small_font.render(
            "Toplam Ödül Grafiği",
            True,
            (0, 220, 220)
        )

        self.screen.blit(title, (x + 10, y + 8))

        graph_x = x + 10
        graph_y = y + 30
        graph_w = w - 20
        graph_h = h - 40

        pygame.draw.line(
            self.screen,
            (90, 90, 90),
            (graph_x, graph_y + graph_h),
            (graph_x + graph_w, graph_y + graph_h),
            1
        )

        pygame.draw.line(
            self.screen,
            (90, 90, 90),
            (graph_x, graph_y),
            (graph_x, graph_y + graph_h),
            1
        )

        if len(self.reward_history) > 1:
            history = self.reward_history[-100:]

            min_reward = min(history)
            max_reward = max(history)

            if min_reward == max_reward:
                max_reward += 1

            points = []

            for index, value in enumerate(history):
                px = graph_x + int(
                    index * graph_w / max(1, len(history) - 1)
                )

                py = graph_y + graph_h - int(
                    (value - min_reward)
                    * graph_h
                    / (max_reward - min_reward)
                )

                points.append((px, py))

            if len(points) > 1:
                pygame.draw.lines(
                    self.screen,
                    (70, 220, 45),
                    False,
                    points,
                    2
                )

    # -------------------------------------------------
    # EĞİTİM AKIŞI
    # -------------------------------------------------
    def choose_training_action(self):
        """
        Geçici action seçimi.

        Şimdilik rastgele hareket seçiyor.
        Sonraki adımda buraya agent.py içindeki
        epsilon-greedy action seçimi bağlanacak.
        """
        return random.choice(self.env.get_available_actions())

    def training_step(self):
        if not self.training:
            return

        action = self.choose_training_action()

        state, reward, done = self.env.move(action)

        self.reward_history.append(self.env.total_reward)
        self.route.append(self.env.truck_position)

        if done:
            self.episode_rewards.append(self.env.total_reward)

            self.episode += 1
            self.env.reset()
            self.route = [self.env.truck_position]

            # Şimdilik temsili epsilon azaltma.
            # Gerçek epsilon değerini agent.py yönetecek.
            self.epsilon = max(0.05, self.epsilon * 0.995)

    # -------------------------------------------------
    # EVENT YÖNETİMİ
    # -------------------------------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if self.start_button.collidepoint(mouse_pos):
                    self.training = not self.training

                elif self.reset_button.collidepoint(mouse_pos):
                    self.env.reset()
                    self.reward_history.clear()
                    self.episode_rewards.clear()
                    self.route = [self.env.truck_position]
                    self.episode = 1
                    self.epsilon = 1.00
                    self.training = False

                elif self.exit_button.collidepoint(mouse_pos):
                    return False

        return True

    # -------------------------------------------------
    # ANA ÇİZİM VE ÇALIŞTIRMA
    # -------------------------------------------------
    def draw(self):
        self.draw_background()

        self.draw_city_grid()
        self.draw_static_objects()
        self.draw_route()
        self.draw_depot()
        self.draw_containers()
        self.draw_truck()
        self.draw_coordinates()

        self.draw_info_panel()
        self.draw_reward_graph()
        self.draw_legend_panel()

        pygame.display.flip()

    def run(self):
        running = True

        while running:
            running = self.handle_events()

            self.training_step()

            self.draw()

            if self.training:
                self.clock.tick(15)
            else:
                self.clock.tick(30)

        pygame.quit()


if __name__ == "__main__":
    env = WasteCollectionEnvironment(grid_size=10)
    visualizer = WasteCollectionVisualizer(env)
    visualizer.run()
class WasteCollectionEnvironment:
    def __init__(self, grid_size=10):
        self.grid_size = grid_size

        # Koordinat sistemi:
        # (0, 0) = sol alt köşe
        self.depot = (0, 0)
        self.truck_position = self.depot

        # Konteynerler: konum -> doluluk oranı
        # Depoya çok yakın çöp kutusu koymadım.
        self.containers = {
            (2, 2): 45,
            (4, 3): 70,
            (5, 1): 50,
            (7, 2): 40,
            (7, 8): 85,
            (1, 8): 65,
            (1, 1): 90
        }

        self.actions = ["up", "down", "left", "right"]

        self.collected_containers = set()
        self.total_reward = 0
        self.step_count = 0
        self.done = False

    def reset(self):
        self.truck_position = self.depot
        self.collected_containers = set()
        self.total_reward = 0
        self.step_count = 0
        self.done = False
        return self.get_state()

    def get_state(self):
        """
        Q-Learning için kullanılacak state.

        State:
        - Araç x konumu
        - Araç y konumu
        - Her konteynerin toplanıp toplanmadığı bilgisi

        Örnek:
        (0, 0, 0, 1, 0, 0, 0, 0, 0)
        """
        collected_status = []

        for position in self.containers.keys():
            if position in self.collected_containers:
                collected_status.append(1)
            else:
                collected_status.append(0)

        x, y = self.truck_position

        return (x, y, *collected_status)

    def get_available_actions(self):
        return self.actions

    def is_inside_grid(self, position):
        x, y = position
        return 0 <= x < self.grid_size and 0 <= y < self.grid_size

    def move(self, action):
        """
        Action değerleri:
        up, down, left, right

        Sol alt koordinat sistemi:
        up    -> y + 1
        down  -> y - 1
        left  -> x - 1
        right -> x + 1
        """
        if self.done:
            return self.get_state(), 0, self.done

        x, y = self.truck_position

        if action == "up":
            new_position = (x, y + 1)
        elif action == "down":
            new_position = (x, y - 1)
        elif action == "left":
            new_position = (x - 1, y)
        elif action == "right":
            new_position = (x + 1, y)
        else:
            raise ValueError("Geçersiz action. up, down, left, right kullan.")

        reward = self.calculate_reward(new_position)

        self.total_reward += reward
        self.step_count += 1

        return self.get_state(), reward, self.done

    def calculate_reward(self, new_position):
        # Grid dışına çıkmaya çalışırsa konum değişmez.
        if not self.is_inside_grid(new_position):
            return -10

        self.truck_position = new_position

        # Her hareket küçük ceza.
        reward = -1

        # Konteyner varsa ve daha önce toplanmadıysa topla.
        if new_position in self.containers:
            fullness = self.containers[new_position]

            if new_position not in self.collected_containers:
                self.collected_containers.add(new_position)

                if fullness >= 80:
                    reward += 50
                elif fullness >= 60:
                    reward += 35
                else:
                    reward += 20
            else:
                reward -= 5

        # Tüm konteynerler toplandıysa ve araç merkeze döndüyse episode biter.
        if self.all_containers_collected() and self.truck_position == self.depot:
            reward += 200
            self.done = True

        # Çok uzun episode olmasın diye sınır.
        if self.step_count >= 300:
            self.done = True

        return reward

    def all_containers_collected(self):
        return set(self.containers.keys()).issubset(self.collected_containers)

    def get_collected_count(self):
        return len(self.collected_containers)

    def get_total_container_count(self):
        return len(self.containers)
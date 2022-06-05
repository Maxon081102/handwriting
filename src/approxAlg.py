def s(a, b, c, d, e, g):
    return (a - b) * (c - d) - (e - d) * (g - b)


def pr(a, b, c, d, e, f, g, z):
    e1, e2, e3, e4 = s(g, e, b, f, z, a), s(g, e, d, f, z, c), s(c, a, f, b, d, e), s(c, a, z, b, d, g)
    if (e1 * e2 < 0) and (e3 * e4 < 0):
        sign = True
    else:
        sign = False
    return sign


class area(object):
    def __init__(self, file_name):
        file = open(file_name, 'r')
        self.border = []
        self.left = -1
        self.right = -1
        self.type = file.readline()[:-1]
        while True:
            pair = file.readline()
            if pair is None:
                break
            x, y = pair.split()
            self.border.append([x, y])

        file.close()

    def expand_border(self, width, height):
        rectangle_width = int(width / 768) + 1
        rectangle_height = int(height / 1024) + 1
        left = 0
        right = 0
        for i in range(len(self.border)):
            self.border[i][0] = int(self.border[i][0] * width / 768)
            self.border[i][1] = int(self.border[i][1] * height / 1024)

        for i in range(len(self.border)):
            if self.border[i][0] < self.border[left][0]:
                left = i

        for i in range(len(self.border)):
            if self.border[i][0] > self.border[right][0]:
                right = i

        self.left = left
        self.right = right

        incr = 1
        if self.border[(left + 1) % len(self.border)][1] > self.border[left][1]:
            incr = -1

        length_to_right = 0
        if (left < right and incr == 1) or (left > right and incr == -1):
            length_to_right = right - left
        else:
            length_to_right = left + len(self.border) - right

        length_to_left = len(self.border) - length_to_right

        self.border[left][0] -= rectangle_width
        self.border[right][0] += rectangle_width
        if length_to_right < 6:
            self.border[(left + incr) % len(self.border)][0] -= rectangle_width
            self.border[(left + incr) % len(self.border)][1] += rectangle_height
            self.border[(right - incr) % len(self.border)][0] += rectangle_width
            self.border[(right - incr) % len(self.border)][1] += rectangle_height
            for i in range(2, length_to_right - 1):
                self.border[(left + i * incr) % len(self.border)][1] += rectangle_height
        else:
            prev_y = self.border[(left + 2 * incr) % len(self.border)][1]
            for i in range(1, 3):
                self.border[(left + i * incr) % len(self.border)][0] -= rectangle_width
                self.border[(left + i * incr) % len(self.border)][1] += rectangle_height

            for i in range(3, length_to_right - 2):
                y = self.border[(left + i * incr) % len(self.border)][1]
                next_y = self.border[(left + (i + 1) * incr) % len(self.border)][1]
                if prev_y < y and y < next_y:
                    self.border[(left + i * incr) % len(self.border)][1] += rectangle_height
                    self.border[(left + i * incr) % len(self.border)][0] -= rectangle_width // 2 + 1
                elif prev_y > y and y > next_y:
                    self.border[(left + i * incr) % len(self.border)][1] += rectangle_height
                    self.border[(left + i * incr) % len(self.border)][0] += rectangle_width // 2 + 1
                else:
                    self.border[(left + i * incr) % len(self.border)][1] += rectangle_height

                prev_y = y

            for i in range(1, 3):
                self.border[(right - i * incr) % len(self.border)][0] += rectangle_width
                self.border[(right - i * incr) % len(self.border)][1] += rectangle_height

        if length_to_left < 6:
            self.border[(left - incr) % len(self.border)][0] -= rectangle_width
            self.border[(left - incr) % len(self.border)][1] -= rectangle_height
            self.border[(right + incr) % len(self.border)][0] += rectangle_width
            self.border[(right + incr) % len(self.border)][1] -= rectangle_height
            for i in range(2, length_to_left - 1):
                self.border[(right + i * incr) % len(self.border)][1] -= rectangle_height

        else:
            prev_y = self.border[(right + 2 * incr) % len(self.border)][1]
            for i in range(1, 3):
                self.border[(right + i * incr) % len(self.border)][0] += rectangle_width
                self.border[(right + i * incr) % len(self.border)][1] -= rectangle_height

            for i in range(3, length_to_left - 2):
                y = self.border[(right + i * incr) % len(self.border)][1]
                next_y = self.border[(right + (i + 1) * incr) % len(self.border)][1]
                if prev_y < y and y < next_y:
                    self.border[(right + i * incr) % len(self.border)][1] -= rectangle_height
                    self.border[(right + i * incr) % len(self.border)][0] += rectangle_width // 2 + 1
                elif prev_y > y and y > next_y:
                    self.border[(right + i * incr) % len(self.border)][1] -= rectangle_height
                    self.border[(right + i * incr) % len(self.border)][0] -= rectangle_width // 2 + 1
                else:
                    self.border[(right + i * incr) % len(self.border)][1] -= rectangle_height

                prev_y = y

            for i in range(1, 3):
                self.border[(left - i * incr) % len(self.border)][0] -= rectangle_width
                self.border[(left - i * incr) % len(self.border)][1] -= rectangle_height

    def get_all_pixels(self):
        up = 0
        down = 0

        pixels = []
        for i in range(len(self.border)):
            if self.border[i][1] < self.border[up][1]:
                up = i

        for i in range(len(self.border)):
            if self.border[i][1] > self.border[down][1]:
                down = i

        for i in range(self.border[up][1], self.border[down][1] + 1):
            for j in range(self.border[self.left][0], self.border[self.right][0] + 1):
                count = 0
                for k in range(len(self.border)):
                    x_1 = self.border[k][0]
                    y_1 = self.border[k][1]
                    x_2 = self.border[(k + 1) % len(self.border)][0]
                    y_2 = self.border[(k + 1) % len(self.border)][1]
                    if pr(j, i, j + 30001, i + 1, x_1, y_1, x_2, y_2):
                        count += 1

                if count % 2 != 0:
                    pixels.append([j, i])

        return pixels

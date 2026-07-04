from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.clock import Clock
import random

class BallWidget(Widget):
    """自定义画布：绘制一个圆球（左蓝 / 右红）"""
    def __init__(self, color=(0,0,1,1), **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.text = "?"
        self.bind(pos=self.redraw, size=self.redraw)
        # 初始化绘图
        with self.canvas:
            self.color_instruction = Color(*color)
            self.ellipse = Ellipse(pos=self.pos, size=self.size)
            # 文字用 Label 在布局中叠加，更简单，我们直接用另一个 Label 覆盖
        # 单独添加一个 Label 用于显示数字（放在上层）
        self.label = Label(text="?", font_size=80, color=(1,1,1,1), halign='center', valign='middle')
        self.add_widget(self.label)
        self.label.bind(pos=self.update_label_pos, size=self.update_label_pos)

    def redraw(self, *args):
        self.ellipse.pos = self.pos
        self.ellipse.size = self.size

    def update_label_pos(self, *args):
        self.label.pos = self.pos
        self.label.size = self.size

    def set_text(self, text):
        self.label.text = str(text)

class LotteryLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        # 顶部标题（可忽略）
        self.add_widget(Label(text="随机摇号", size_hint_y=0.1, font_size=30))

        # 中间：两个球 + 顶部标签
        balls_box = BoxLayout(orientation='horizontal', spacing=20, padding=20)
        # 左侧：标签28 + 蓝色球
        left_box = BoxLayout(orientation='vertical')
        left_box.add_widget(Label(text="28", font_size=40, size_hint_y=0.2))
        self.ball1 = BallWidget(color=(0, 0.3, 1, 1))  # 蓝色
        left_box.add_widget(self.ball1)
        # 右侧：标签3D + 红色球
        right_box = BoxLayout(orientation='vertical')
        right_box.add_widget(Label(text="3D", font_size=40, size_hint_y=0.2))
        self.ball2 = BallWidget(color=(1, 0, 0, 1))   # 红色
        right_box.add_widget(self.ball2)

        balls_box.add_widget(left_box)
        balls_box.add_widget(right_box)
        self.add_widget(balls_box)

        # 底部：摇号按钮
        self.btn = Button(text="摇号", font_size=30, size_hint_y=0.15)
        self.btn.bind(on_press=self.start_lottery)
        self.add_widget(self.btn)

        # 动画控制
        self.running = False
        self.step = 0
        self.total_steps = 40

    def _generate_two_distinct(self):
        a = random.randint(0, 9)
        b = random.randint(0, 9)
        while b == a:
            b = random.randint(0, 9)
        return a, b

    def start_lottery(self, instance):
        if self.running:
            return
        self.running = True
        self.btn.disabled = True
        self.step = 0
        Clock.schedule_interval(self.animate, 0.05)  # 50ms

    def animate(self, dt):
        a, b = self._generate_two_distinct()
        self.ball1.set_text(a)
        self.ball2.set_text(b)

        self.step += 1
        if self.step >= self.total_steps:
            # 停止动画，显示最终结果
            a, b = self._generate_two_distinct()
            self.ball1.set_text(a)
            self.ball2.set_text(b)
            self.running = False
            self.btn.disabled = False
            return False  # 取消定时器

class LotteryApp(App):
    def build(self):
        return LotteryLayout()

if __name__ == "__main__":
    LotteryApp().run()